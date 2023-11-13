import cv2
import numpy as np

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

def hole_filling_color(image, kernel_size):
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
            # Vérifiez si le pixel actuel est noir (0, 0, 0) et si oui, remplissez-le
            if np.all(image[i, j] == [0, 0, 0]):
                neighborhood = image[i - k:i + k + 1, j - k:j + k + 1]
                
                 # Remplacez le pixel noir par la valeur médiane des pixels voisins non noirs
                non_zero_values = neighborhood[~np.all(neighborhood == [0, 0, 0], axis=2)]
                if non_zero_values.size > 0:
                    result[i, j] = np.median(non_zero_values, axis=0)
    
    return result
    
def gaussian_filter(image, kernel_size, sigma):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    
# Charger une image depuis un fichier
image = cv2.imread("ShotNoise.png", cv2.IMREAD_COLOR)

# Appliquer le filtre médian avec une taille de noyau de 3x3
kernel_size = 3
filtered_image = median_filter_color(image, kernel_size)
filled_image = hole_filling_color(image, kernel_size)

kernel_size = 5
sigma = 1.5
smoothed_image = gaussian_filter(image, kernel_size, sigma)

# Afficher l'image originale et l'image filtrée
#cv2.imshow('Image Originale', image)
#cv2.imshow('Image_medianFiltre', filtered_image)
#cv2.imshow('Image avec Trous Remplis', filled_image)
#cv2.imshow('Image_Gaussien', smoothed_image)
cv2.imwrite("Median_Filtre.png", filtered_image)
cv2.imwrite("Trous_Remplis_Filtre.png", filled_image)
cv2.imwrite("Gaussian_Filtre.png", smoothed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

