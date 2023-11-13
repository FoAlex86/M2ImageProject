import cv2
import numpy as np
from math import log10, sqrt

def psnr(original, filtered):
    # Assurez-vous que les images ont la même taille
    if original.shape != filtered.shape:
        raise ValueError("Les dimensions des images ne correspondent pas.")

    # Calculez la différence quadratique moyenne entre les pixels pour chaque canal
    mse = np.mean((original - filtered) ** 2, axis=(0, 1))

    # Si la MSE est proche de zéro pour tous les canaux, le PSNR est indéfini, retournez des valeurs élevées
    if np.all(mse == 0):
        return float('inf')

    # Calculez le PSNR pour chaque canal en utilisant la formule standard
    max_pixel_value = 255.0
    psnr_values = 20 * np.log10(max_pixel_value / np.sqrt(mse))

    # Moyenne des valeurs PSNR pour chaque canal
    psnr_value = np.mean(psnr_values)

    return psnr_value

# Charger l'image originale et l'image filtrée depuis des fichiers (assurez-vous que les chemins sont corrects)
original_image = cv2.imread("original_2048.png", cv2.IMREAD_COLOR)
noise_image = cv2.imread("ShotNoise.png", cv2.IMREAD_COLOR)
gaussian_filtered_image = cv2.imread("Gaussian_Filtre.png", cv2.IMREAD_COLOR)
median_filtered_image = cv2.imread("Median_Filtre.png", cv2.IMREAD_COLOR)
atrou_filtered_image = cv2.imread("Trous_Remplis_Filtre.png", cv2.IMREAD_COLOR)


# Calculer le PSNR entre les deux images
psnr_noiseImage_value = psnr(original_image, noise_image)
psnr_gaussianFiltered_value = psnr(original_image, gaussian_filtered_image)
psnr_medianFiltered_value = psnr(original_image, median_filtered_image)
psnr_atrouFiltered_value = psnr(original_image, atrou_filtered_image)

# Afficher le résultat
print(f"La valeur PSNR entre l'image originale et l'image bruitée est : {psnr_noiseImage_value} dB")
print(f"La valeur PSNR entre l'image originale et l'image filtrée gaussian est : {psnr_gaussianFiltered_value} dB")
print(f"La valeur PSNR entre l'image originale et l'image filtrée median est : {psnr_medianFiltered_value} dB")
print(f"La valeur PSNR entre l'image originale et l'image filtrée atrou est : {psnr_atrouFiltered_value} dB")

