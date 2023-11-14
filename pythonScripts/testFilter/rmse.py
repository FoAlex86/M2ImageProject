import cv2
import numpy as np
from math import sqrt

def rmse(original, reconstructed):
    # Assurez-vous que les images ont la même taille
    if original.shape != reconstructed.shape:
        raise ValueError("Les dimensions des images ne correspondent pas.")

    # Normaliser les valeurs de pixels entre 0 et 1
    original_norm = original / 255.0
    reconstructed_norm = reconstructed / 255.0

    # Calculer la RMSE pour chaque canal de couleur
    rmse_values = np.sqrt(np.mean((original_norm - reconstructed_norm)**2, axis=(0, 1)))

    # Calculer la RMSE moyenne sur tous les canaux
    rmse_mean = np.mean(rmse_values)

    return rmse_mean

   
# Charger l'image originale et l'image filtrée depuis des fichiers (assurez-vous que les chemins sont corrects)
original_image = cv2.imread("original_2048.png", cv2.IMREAD_COLOR)
noise_image = cv2.imread("ShotNoise.png", cv2.IMREAD_COLOR)
gaussian_filtered_image = cv2.imread("Gaussian_Filtre.png", cv2.IMREAD_COLOR)
median_filtered_image = cv2.imread("Median_Filtre.png", cv2.IMREAD_COLOR)
atrou_filtered_image = cv2.imread("Trous_Remplis_Filtre.png", cv2.IMREAD_COLOR)


# Calculer la RMSE entre les deux images
rmse_noiseImage_value = rmse(original_image, noise_image)
rmse_gaussianFiltered_value = rmse(original_image, gaussian_filtered_image)
rmse_medianFiltered_value = rmse(original_image, median_filtered_image)
rmse_atrouFiltered_value = rmse(original_image, atrou_filtered_image)

# Afficher le résultat
print(f"La valeur RMSE entre l'image originale et l'image bruitée est : {rmse_noiseImage_value}")
print(f"La valeur RMSE entre l'image originale et l'image filtrée gaussian est : {rmse_gaussianFiltered_value}")
print(f"La valeur RMSE entre l'image originale et l'image filtrée median est : {rmse_medianFiltered_value}")
print(f"La valeur RMSE entre l'image originale et l'image filtrée atrou est : {rmse_atrouFiltered_value}")

