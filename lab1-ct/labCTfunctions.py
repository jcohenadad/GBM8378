'''
This is a pytphon version of GBM8378 Lab 1 toolbox.

Dependencies
    - numpy
    - scipy
    - skimage

Guillaume Sheehy
2020-01-29
'''

# %% Imports
import numpy as np
import skimage.data
from scipy.ndimage.interpolation import rotate
from skimage.transform import radon

# %% Tools
def load_sinogram():
    '''
    Generates the sinogram of the Sheep Logan Phantom first loaded from skimage.data.

        - Ouput:

            sinogram - numpy.array that contains the contains the sinogram of the Shepp Logan Phantom.

                NOTE - the shape is [angle, position]
    '''
    # Load the shepp logan phantom data
    slp_image = skimage.data.shepp_logan_phantom()
    # create the sinogram of the sheep logan phantom loaded from skimage
    sinogram = radon(slp_image)
    return sinogram


def retroprojection(sinogram, angles):
    '''
    Reconstruct the original image using retroprojection of a sinogram.

        - Inputs:

            sinogram - numpy.array that contains a sinogram

                NOTE - the shape should be [position, angle]

            angles - LIST contains the angles used in the construction of the sinogram.
    '''
    s = sinogram.shape[0]
    image = np.zeros((s, s))
    for angle in angles:
        angle = int(angle)
        retro_projection = np.array([sinogram[:, angle]
                                     for _ in range(sinogram.shape[0])])
        image += rotate(retro_projection, angle, reshape=False)
    return image


def do_sinogram(image, angles):
    """
    Construct a sinogram from an image

        - Inputs:
            image - numpy.array that contains a image

            angles - LIST that contains the angles used in the construction of the sinogram.
    """
    sinogram = np.zeros([len(image), len(angles)])
    for i in range(len(angles)):
        projection = rotate(image, -angles[i], reshape=None)
        sinogram[:, i] = np.sum(projection, axis=0)
    return sinogram
