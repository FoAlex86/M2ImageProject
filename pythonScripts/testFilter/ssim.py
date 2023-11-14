from skimage.metrics import structural_similarity as ssim
import cv2

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
noise_image = cv2.imread("blackNoise.png", cv2.IMREAD_COLOR)
gaussian_filtered_image = cv2.imread("Gaussian_Filtre.png", cv2.IMREAD_COLOR)
median_filtered_image = cv2.imread("Median_Filtre.png", cv2.IMREAD_COLOR)
atrou_filtered_image = cv2.imread("Trous_Remplis_Filtre.png", cv2.IMREAD_COLOR)

# Convertir les images en RGB (scikit-image utilise des images RGB)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
noise_image = cv2.cvtColor(noise_image, cv2.COLOR_BGR2RGB)
gaussian_filtered_image = cv2.cvtColor(gaussian_filtered_image, cv2.COLOR_BGR2RGB)
median_filtered_image = cv2.cvtColor(median_filtered_image, cv2.COLOR_BGR2RGB)
atrou_filtered_image = cv2.cvtColor(atrou_filtered_image, cv2.COLOR_BGR2RGB)

# Calculer le SSIM entre les deux images
ssim_noiseImage_value, _ = ssim(original_image, noise_image, multichannel=True)
ssim_gaussianFiltered_value, _ = ssim(original_image, gaussian_filtered_image, multichannel=True)
ssim_medianFiltered_value, _ = ssim(original_image, median_filtered_image, multichannel=True)
ssim_atrouFiltered_value, _ = ssim(original_image, atrou_filtered_image, multichannel=True)

# Afficher le résultat
print(f"La valeur SSIM entre l'image originale et l'image bruitée est : {ssim_noiseImage_value}")
print(f"La valeur SSIM entre l'image originale et l'image filtrée gaussian est : {ssim_gaussianFiltered_value}")
print(f"La valeur SSIM entre l'image originale et l'image filtrée median est : {ssim_medianFiltered_value}")
print(f"La valeur SSIM entre l'image originale et l'image filtrée atrou est : {ssim_atrouFiltered_value}")

