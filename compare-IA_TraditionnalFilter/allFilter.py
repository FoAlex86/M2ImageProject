import cv2
import numpy as np
from math import log10, sqrt
from skimage.metrics import structural_similarity as ssim

##################################################################
###########Filter##############
# filtre médian
def median_filter_color(image, kernel_size):
    # Assurez-vous que la taille du noyau est impaire
    if kernel_size % 2 == 0:
        raise ValueError("La taille du noyau doit être impaire.")

    # Copiez l'image pour ne pas modifier l'original
    result = image.copy()
    
    # Obtenez la moitié de la taille du noyau
    k = kernel_size // 2
    
    # Parcourez l'image en laissant un cadre de k pixels autour
    for i in range(k, image.shape[0] - k):
        for j in range(k, image.shape[1] - k):
            # Sélectionnez la région du noyau pour chaque canal de couleur
            for channel in range(image.shape[2]):
                neighborhood = image[i - k:i + k + 1, j - k:j + k + 1, channel]
                
                # Appliquez le filtre médian et mettez à jour le résultat
                result[i, j, channel] = np.median(neighborhood)
    
    return result


# filtre gaussien    
def gaussian_filter(image, kernel_size, sigma):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
 
##########apply filter############    
# Charger une image depuis un fichier
imageG = cv2.imread("1.png", cv2.IMREAD_COLOR)
imageP = cv2.imread("2.png", cv2.IMREAD_COLOR)

# Appliquer le filtre médian avec une taille de noyau de 3x3
kernel_size = 3
filtered_image = median_filter_color(imageP, kernel_size)

# Appliquer le filtre Gaussien avec une taille de noyau de 5x5
kernel_size = 5
sigma = 1.5
smoothed_image = gaussian_filter(imageG, kernel_size, sigma)

# Ecrire l'image originale et l'image filtrée
cv2.imwrite("5.png", smoothed_image)
cv2.imwrite("6.png", filtered_image)

#####################################################################
#########PSNR############
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
print(f"------------------------------------New Image----------------")
original_image = cv2.imread("0.png", cv2.IMREAD_COLOR)

gaussian_filtered_ia_image = cv2.imread("3.png", cv2.IMREAD_COLOR)
median_filtered_ia_image = cv2.imread("4.png", cv2.IMREAD_COLOR)

gaussian_filtered_cl_image = cv2.imread("5.png", cv2.IMREAD_COLOR)
median_filtered_cl_image = cv2.imread("6.png", cv2.IMREAD_COLOR)

# Calculer le PSNR entre les deux images
psnr_noiseG_value = psnr(original_image, imageG)
psnr_noiseP_value = psnr(original_image, imageP)

psnr_gaussianFiltered_ia_value = psnr(original_image, gaussian_filtered_ia_image)
psnr_gaussianFiltered_cl_value = psnr(original_image, gaussian_filtered_cl_image)

psnr_medianFiltered_ia_value = psnr(original_image, median_filtered_ia_image)
psnr_medianFiltered_cl_value = psnr(original_image, median_filtered_cl_image)

######################################################################
#########RMSE############

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


# Calculer la RMSE entre les deux images
rmse_noiseG_value = rmse(original_image, imageG)
rmse_noiseP_value = rmse(original_image, imageP)

rmse_gaussianFiltered_ia_value = rmse(original_image, gaussian_filtered_ia_image)
rmse_gaussianFiltered_cl_value = rmse(original_image, gaussian_filtered_cl_image)

rmse_medianFiltered_ia_value = rmse(original_image, median_filtered_ia_image)
rmse_medianFiltered_cl_value = rmse(original_image, median_filtered_cl_image)

######################################################################
#########SSIM############
# Convertir les images en RGB (scikit-image utilise des images RGB)
original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

imageG = cv2.cvtColor(imageG, cv2.COLOR_BGR2RGB)
imageP = cv2.cvtColor(imageP, cv2.COLOR_BGR2RGB)

gaussian_filtered_ia_image = cv2.cvtColor(gaussian_filtered_ia_image, cv2.COLOR_BGR2RGB)
gaussian_filtered_cl_image = cv2.cvtColor(gaussian_filtered_cl_image, cv2.COLOR_BGR2RGB)

median_filtered_ia_image = cv2.cvtColor(median_filtered_ia_image, cv2.COLOR_BGR2RGB)
median_filtered_cl_image = cv2.cvtColor(median_filtered_cl_image, cv2.COLOR_BGR2RGB)


# Calculer le SSIM entre les deux images
ssim_noiseG_value = ssim(original_image, imageG, win_size=3, channel_axis=None)
ssim_noiseP_value = ssim(original_image, imageP, win_size=3, channel_axis=None)

ssim_gaussianFiltered_ia_value = ssim(original_image, gaussian_filtered_ia_image, win_size=3, channel_axis=None)

ssim_gaussianFiltered_cl_value = ssim(original_image, gaussian_filtered_cl_image, win_size=3, channel_axis=None)



ssim_medianFiltered_ia_value = ssim(original_image, median_filtered_ia_image, win_size=3, channel_axis=None)

ssim_medianFiltered_cl_value = ssim(original_image, median_filtered_cl_image, win_size=3, channel_axis=None)


# Afficher le résultat
print(f"-------------------------GAUSSIAN------------------------")
print(f"-----bruitGpsnr : {psnr_noiseG_value} dB---------")
print(f"-----bruitGrmse : {rmse_noiseG_value}---------")
print(f"-----bruitGssim : {ssim_noiseG_value}---------")

print(f"-------------------Gaussien_IA------------------")
print(f"La valeur PSNR pour ia Gaussian : {psnr_gaussianFiltered_ia_value - psnr_noiseG_value} dB")
print(f"La valeur RSME pour ia Gaussian : {rmse_gaussianFiltered_ia_value - rmse_noiseG_value}")
print(f"La valeur SSIM pour ia Gaussian : {ssim_gaussianFiltered_ia_value - ssim_noiseG_value}")

print(f"-------------------Gaussien_CL------------------")
print(f"La valeur PSNR pour cl Gaussian : {psnr_gaussianFiltered_cl_value - psnr_noiseG_value} dB")
print(f"La valeur RSME pour cl Gaussian : {rmse_gaussianFiltered_cl_value - rmse_noiseG_value}")
print(f"La valeur SSIM pour cl Gaussian : {ssim_gaussianFiltered_cl_value - ssim_noiseG_value}")

print(f"-------------------------POISSON------------------------")
print(f"-----bruitP : {psnr_noiseP_value} dB---------")
print(f"-----bruitP : {rmse_noiseP_value}---------")
print(f"-----bruitP : {ssim_noiseP_value}---------")

print(f"-------------------Poisson_IA------------------")
print(f"La valeur PSNR pour ia Poisson : {psnr_medianFiltered_ia_value - psnr_noiseP_value} dB")
print(f"La valeur RSME pour ia Poisson : {rmse_medianFiltered_ia_value - rmse_noiseP_value}")
print(f"La valeur SSIM pour ia Poisson : {ssim_medianFiltered_ia_value - ssim_noiseP_value}")

print(f"-------------------Poisson_CL------------------")
print(f"La valeur PSNR pour cl Poisson : {psnr_medianFiltered_cl_value - psnr_noiseP_value} dB")
print(f"La valeur RSME pour cl Poisson : {rmse_medianFiltered_cl_value - rmse_noiseP_value}")
print(f"La valeur SSIM pour cl Poisson : {ssim_medianFiltered_cl_value - ssim_noiseP_value}")


print(f"--------------------------------------------------------------")
