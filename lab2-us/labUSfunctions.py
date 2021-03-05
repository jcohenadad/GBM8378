# Title: Ultrasound Forward Simulator
# Filename: ussimforward.py
# Authors: Jonathan Poree, Samuel Desmarais --- Provost Ultrasound Lab
# Inspired from work in: Section 2.3 of https://doi.org/10.1088/1361-6560/aae3c3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from tqdm.notebook import tqdm


def ussimforward(xgrid, ygrid, zgrid, delays, apod, prm):
    if prm['useprobeheight']:
        neleh = int(2 * np.floor(prm['height'] / prm['lbd']) + 1)
    else:
        neleh = 1

    rscat = np.stack((np.reshape(xgrid, [-1]), np.reshape(ygrid, [-1]), np.reshape(zgrid, [-1])), axis=1)
    delays = np.transpose(np.tile(delays, reps=neleh)[:, None])
    apod = np.transpose(np.tile(apod, reps=neleh)[:, None])

    floatprecision = np.float32
    complexprecision = np.complex64
    delays = delays.astype(floatprecision)
    apod = apod.astype(floatprecision)
    rscat = rscat.astype(floatprecision)
    prm['pulse'] = prm['pulse'].astype(floatprecision)

    xele = np.arange(prm['nele'], dtype=floatprecision) * prm['pitch'] - (prm['nele'] - 1) * prm['pitch'] / 2
    yele = np.arange(neleh, dtype=floatprecision) * prm['height'] / neleh - (neleh - 1) * prm['height'] / neleh / 2
    xele, yele = np.meshgrid(xele, yele)
    zele = prm['elevfocus'] - np.sqrt(prm['elevfocus'] ** 2 - yele ** 2)

    xele = np.reshape(xele, [-1])
    yele = np.reshape(yele, [-1])
    zele = np.reshape(zele, [-1])
    re = np.stack((xele, yele, zele), axis=1)

    delaysMax = np.max(xele * np.sin(np.deg2rad(45)) / prm['c'])

    dmax = np.sqrt((np.max(xele) - np.min(xele)) ** 2 + (np.max(yele) - np.min(yele)) ** 2 + np.max(rscat[:, 2]) ** 2)
    tmax = dmax / prm['c'] + 2 * delaysMax
    nscat = rscat.shape[0]

    nt = int(8 * np.ceil(tmax * prm['fs'] / 8))
    fi = np.linspace(0, prm['fs'] / 2, num=int(nt / 2), endpoint=True, dtype=floatprecision)
    nf = fi.size
    wi = 2 * np.pi * fi
    ki = wi / prm['c']
    wc = 2 * np.pi * prm['fc']
    # misses t, kc and df from matlab

    PULSE = np.fft.fft(prm['pulse'], int(np.ceil(nt * prm['fspulse'] / prm['fs']))).astype(complexprecision)
    PULSE = PULSE[:int(nt / 2)]

    hele = np.sin(
        2 * np.pi * prm['fc'] * np.arange(0, 1 / prm['BW'] / prm['fc'] + 1 / prm['fspulse'], 1 / prm['fspulse']))
    HELE = np.fft.fft(hele * np.hanning(hele.size), int(np.ceil(nt * prm['fspulse'] / prm['fs']))).astype(
        complexprecision)
    HELE = HELE[:int(nt / 2)]

    rff = np.empty([nf, nscat], dtype=complexprecision)

    rscat = np.transpose(rscat[:, :, None], axes=[0, 2, 1])
    re = np.transpose(re[:, :, None], axes=[2, 0, 1])

    dtx = rscat - re
    rtx = np.sqrt(np.sum(dtx ** 2, axis=2))

    sintxx = dtx[:, :, 0] / rtx
    sintxy = dtx[:, :, 1] / rtx
    costx = dtx[:, :, 2] / rtx

    stx = apod * np.exp(1j * delays * wi[:, None])
    stx = np.transpose(stx[:, :, None], axes=[2, 1, 0])

    for ik in tqdm(np.arange(ki.size - 1, 0 - 1, -1), desc='Simulating the US wave'):

        sincargwidth = prm['width'] / 2 / np.pi * sintxx * ki[ik]
        sincargheigth = prm['height'] / 2 / np.pi * sintxy * ki[ik]
        if prm['hardbaffle']:
            dtx = costx ** 2 * np.sinc(sincargwidth) * np.sinc(sincargheigth)
        else:
            dtx = np.sinc(sincargwidth) * np.sinc(sincargheigth)

        if prm['useprobeheight']:
            dtx = dtx * np.exp(1j * rtx * ki[ik]) / rtx
        else:
            dtx = dtx * np.exp(1j * rtx * ki[ik]) / np.sqrt(rtx)

        TX = np.sum(dtx * stx[:, :, ik], 1)
        TX = PULSE[ik] * HELE[ik] * TX

        rff[ik, :] = TX

    RF = np.imag(np.fft.ifft(rff, n=nt, axis=0))
    idxmax = int(np.ceil(tmax - 2 * delaysMax) * prm['fs'])
    RF = RF[:idxmax, :]
    RF = np.reshape(np.transpose(RF), [xgrid.shape[0], xgrid.shape[1], -1])
    RF = RF[:, :, ::-1]
    RF = RF[:, :, :-100]
    return RF


def prepare_animation(RF, fovx, fovz):
    print('Preparing the animation...')
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(14, 5)
    fov = [0, fovz * 1000, -fovx * 500, fovx * 500]

    def animate(i, RF):
        ampl_max = abs(RF).max()
        ax[0].imshow(RF[:, :, i], extent=fov, vmin=-ampl_max, vmax=ampl_max, cmap='bwr')
        ax[0].set_title("Ultrasound wave propagation", fontsize=15)
        ax[0].set_xlabel('Distance (mm)')
        ax[0].set_ylabel('Distance (mm)')

    anim = animation.FuncAnimation(fig, animate, frames=range(0, RF.shape[2], 20), interval=100, fargs=(RF,))
    plt.close()
    ampl_max = abs(RF[:, :, RF.shape[2] // 2]).max()
    im1 = ax[1].imshow(RF[:, :, RF.shape[2] // 2], extent=fov, vmin=-ampl_max, vmax=ampl_max, cmap='bwr')
    ax[1].set_xlabel('Distance (mm)')
    ax[1].set_ylabel('Distance (mm)')
    fig.colorbar(im1, ax=ax[1], orientation="horizontal")

    im2 = ax[2].imshow(np.abs(RF).sum(axis=2), extent=fov, cmap='inferno')
    ax[2].set_title('Intégration temporelle \ndu champ de propagation', fontsize=15)
    ax[2].set_xlabel('Distance (mm)')
    ax[2].set_ylabel('Distance (mm)')
    fig.colorbar(im2, ax=ax[2], orientation="horizontal")
    return anim
