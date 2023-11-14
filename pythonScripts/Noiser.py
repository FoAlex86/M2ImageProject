import random

import numpy as np
import cv2
import sys
from datetime import datetime

def add_poisson_noise(image, intensity, intensityCorrection = False):

    if intensityCorrection:
        pixelMoyen = cv2.mean(image)
        intensiteMoyenne = (pixelMoyen[0] + pixelMoyen[1] + pixelMoyen[2]) / 3

    noise = np.random.poisson(intensity, image.shape)

    # Ajouter le bruit à l'image
    noisy_image = image + noise

    # Assurer que les valeurs restent dans la plage [0, 255]
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    if intensityCorrection:
        pixelMoyen = cv2.mean(noisy_image)
        newintensiteMoyenne = (pixelMoyen[0] + pixelMoyen[1] + pixelMoyen[2]) / 3

        intensityDiff = intensiteMoyenne - newintensiteMoyenne

        noisy_image = noisy_image + intensityDiff
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    return noisy_image

def add_gaussian_noise(image, mean=0, sigma=25):
    """
    Ajoute du bruit gaussien à une image.

    Parameters:
    - image: NumPy array représentant l'image (format BGR).
    - mean: Moyenne de la distribution gaussienne.
    - sigma: Écart-type de la distribution gaussienne.

    Returns:
    - Image avec bruit gaussien ajouté.
    """
    # Générer le bruit gaussien
    gaussian_noise = np.random.normal(mean, sigma, image.shape).astype(np.int8)

    # Ajouter le bruit à l'image
    noisy_image = image + gaussian_noise

    # Assurer que les valeurs restent dans la plage [0, 255]
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    return noisy_image

# freq : [0,100] la frequence d'apparition d'un pixel bruité
def addBlackNoise(image, freq):
    hauteur, largeur, _ = image.shape

    for y in range(hauteur):
        for x in range(largeur):
            if random.randint(0,100) < freq:
                image[y,x] = 0

    return image

def add_white_noiseRGB(image, scale=0.1):
    # Générer le bruit blanc
    white_noise = np.random.rand(*image.shape) * scale

    # Ajouter le bruit à l'image
    noisy_image = image + white_noise * 255

    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)

    return noisy_image

def addBlackNoiseInDarkArea(image, freq):
    hauteur, largeur, _ = image.shape

    for y in range(hauteur):
        for x in range(largeur):
            if random.randint(0,100) < freq:
                image[y,x] = 0

    return image

def addSaltPepperNoise(image, freq):
    hauteur, largeur, _ = image.shape

    for y in range(hauteur):
        for x in range(largeur):
            if random.randint(0,100) < freq:
                if random.randint(0,1) == 0:
                    image[y,x] = 0
                else:
                    image[y, x] = (255,255,255)

    return image


def process(image_path):
    # Charger une image à partir du chemin spécifié
    image = cv2.imread(image_path)

    if image is None:
        print("Impossible de charger l'image. Assurez-vous que le chemin est correct.")
        sys.exit(1)

    # Ajouter le bruit à l'image
    #noisy_image = addBlackNoise(image, 10)
    #noisy_image = addSaltPepperNoise(image, 5)
    noisy_image = add_white_noiseRGB(image, 0.4)
    #noisy_image = add_gaussian_noise(image, 0, 20)
    #noisy_image = add_poisson_noise(image, 50, True)

    now = datetime.now()
    date_time_string = now.strftime("%Y_%m_%d_%H%M%S")

    cv2.imwrite('out/noisy_img' + date_time_string + '.png', noisy_image)


image_path = "./in/50000.png"

process(image_path)