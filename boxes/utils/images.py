# import the necessary packages
from skimage.measure import structural_similarity as ssim
import numpy as np
import cv2


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def is_similar_by_mse(imageA, imageB):
    # mais similar quanto mais próximo de 0
    ret = mse(imageA, imageB)
    return (1 - ret) / 100


def is_similar_by_ssim(imageA, imageB):
    # mais similar quanto mais próximo de 1.0
    ret = ssim(imageA, imageB)
    return ret


def image(file_path):
    return cv2.imread(file_path)


def gray_scale_image(image):
    # convert the images to grayscale
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
