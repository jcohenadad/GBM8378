# Title: Ultrasound Forward Simulator
# Filename: ussimforward.py
# Authors: Jonathan Poree, Samuel Desmarais --- Provost Ultrasound Lab
# Inspired from work in: Section 2.3 of https://doi.org/10.1088/1361-6560/aae3c3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from tqdm.notebook import tqdm


def ussimforward(xgrid, ygrid, zgrid, delays, apod, prm):

    # Define Aperture
    aperturex = (prm['nele']-1) * prm['pitch']
    xele = np.arange(prm['nele'], dtype=prm['floatprecision']) * prm['pitch'] - aperturex/2

    if prm['useprobeheight']:
        neleh = int(2 * np.floor(prm['height'] / prm['lbd']) + 1)
        aperturey = prm['height']
        pitchy = aperturey/(neleh-1)
        yele = np.arange(neleh, dtype=prm['floatprecision']) * pitchy - aperturey/2
    else:
        neleh = 1
        aperturey = prm['width']
        yele = np.arange(neleh, dtype=prm['floatprecision'])  # 0

    xele, yele = np.meshgrid(xele, yele)

    zele = prm['elevfocus'] - np.sqrt(prm['elevfocus']**2 - yele**2)

    # Vectorize Aperture
    xele = np.reshape(xele, [-1])
    yele = np.reshape(yele, [-1])
    zele = np.reshape(zele, [-1])
    re = np.stack((xele, yele, zele), axis=1)

    delays = delays.astype(prm['floatprecision'])
    apod = apod.astype(prm['floatprecision'])

    delays = np.transpose(np.tile(delays, reps=neleh)[:, None])
    apod = np.transpose(np.tile(apod, reps=neleh)[:, None])

    # Define Medium
    rscat = np.stack((np.reshape(xgrid, [-1]),
                      np.reshape(ygrid, [-1]),
                      np.reshape(zgrid, [-1])), axis=1)
    rscat = rscat.astype(prm['floatprecision'])
    nscat = rscat.shape[0]

    prm['pulse'] = prm['pulse'].astype(prm['floatprecision'])

    delaysMax = np.max(xele * np.sin(np.deg2rad(45)) / prm['c'])

    DepthMax = np.max(rscat[:, 2])
    dmax = np.sqrt(aperturex**2 + aperturey**2 + DepthMax**2)
    tmax = dmax/prm['c'] + 2*delaysMax

    nt = int(8 * np.ceil(tmax * prm['fs'] / 8))
    fi = np.linspace(0, prm['fs']/2, num=int(nt/2), endpoint=True, dtype=prm['floatprecision'])
    nf = fi.size
    wi = 2 * np.pi * fi
    ki = wi / prm['c']

    Tpulse = len(prm['pulse'])/prm['fspulse']
    PULSE = np.fft.fft(prm['pulse'], int(np.ceil(nt*prm['fspulse']/prm['fs']))).astype(prm['complexprecision'])
    PULSE = PULSE[:int(nt/2)]

    tele = np.arange(0, 1/prm['eleBW']/prm['fc']+1/prm['fspulse'], 1/prm['fspulse'])
    hele = np.sin(2*np.pi*prm['fc']*tele)
    Tele = np.max(tele)
    HELE = np.fft.fft(hele*np.hanning(hele.size), int(np.ceil(nt*prm['fspulse']/prm['fs'])))\
        .astype(prm['complexprecision'])
    HELE = HELE[:int(nt/2)]

    rff = np.empty([nf, nscat], dtype=prm['complexprecision'])

    rscat = np.transpose(rscat[:, :, None], axes=[0, 2, 1])
    re = np.transpose(re[:, :, None], axes=[2, 0, 1])

    dtx = rscat - re
    rtx = np.sqrt(np.sum(dtx**2, axis=2))

    sintxx = dtx[:, :, 0]/rtx
    sintxy = dtx[:, :, 1]/rtx
    costx = dtx[:, :, 2]/rtx

    stx = apod*np.exp(1j * (delays + Tpulse + Tele) * wi[:, None])
    stx = np.transpose(stx[:, :, None], axes=[2, 1, 0])

    for ik in tqdm(np.arange(ki.size - 1, 0 - 1, -1), desc='Simulating the US wave'):

        sincarg1 = prm['width']/2/np.pi * sintxx * ki[ik]
        sincarg2 = prm['lbd']/2/np.pi * sintxy * ki[ik]

        if prm['hardbaffle']:
            dtx = costx**2 * np.sinc(sincarg1) * np.sinc(sincarg2)
        else:
            dtx = np.sinc(sincarg1) * np.sinc(sincarg2)

        if prm['useprobeheight']:
            dtx = dtx * np.exp(1j * rtx * ki[ik]) / rtx
        else:
            dtx = dtx * np.exp(1j * rtx * ki[ik]) / np.sqrt(rtx)

        TX = np.sum(dtx * stx[:, :, ik], 1)
        TX = PULSE[ik] * HELE[ik] * TX

        rff[ik, :] = TX

    RF = np.imag(np.fft.ifft(rff, n=nt, axis=0))
    idxmax = int(np.ceil(tmax - 2*delaysMax) * prm['fs'])
    RF = RF[:idxmax, :]
    RF = np.reshape(np.transpose(RF), [xgrid.shape[0], xgrid.shape[1], -1])
    RF = RF[:, :, ::-1]
    RF = np.transpose(RF, axes=[1, 0, 2])

    return RF


def prepare_animation(RF, fovx, fovz):
    print('Preparing the animation...')
    fig, ax = plt.subplots(1, 3)
    fig.set_size_inches(14, 5)
    fov = [-fovx * 500, fovx * 500, fovz * 1000, 0]

    def animate(i, RF):
        ampl_max = abs(RF).max()
        ax[0].imshow(RF[:, :, i], extent=fov, vmin=-ampl_max, vmax=ampl_max, cmap='bwr')
        ax[0].set_title("Ultrasound wave propagation", fontsize=15)
        ax[0].set_xlabel('Distance (mm)')
        ax[0].set_ylabel('Distance (mm)')

    anim = animation.FuncAnimation(fig, animate, frames=range(0, RF.shape[2], 20), interval=100, fargs=(RF,))
    plt.close()
    ampl_max1 = abs(RF[:, :, RF.shape[2] // 2]).max()
    im1 = ax[1].imshow(RF[:, :, RF.shape[2] // 2], extent=fov, vmin=-ampl_max1, vmax=ampl_max1, cmap='bwr')
    ax[1].set_xlabel('Distance (mm)')
    ax[1].set_ylabel('Distance (mm)')
    fig.colorbar(im1, ax=ax[1], orientation="horizontal")

    im2 = ax[2].imshow(np.abs(RF).sum(axis=2), extent=fov, cmap='inferno')
    ax[2].set_title('Intégration temporelle \ndu champ de propagation', fontsize=15)
    ax[2].set_xlabel('Distance (mm)')
    ax[2].set_ylabel('Distance (mm)')
    fig.colorbar(im2, ax=ax[2], orientation="horizontal")
    return anim
