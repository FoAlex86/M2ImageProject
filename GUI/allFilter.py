import numpy as np
from PIL import Image, ImageFilter
import scipy.ndimage as ndimage


def median_filter_color(image, kernel_size):
    if kernel_size % 2 == 0:
        raise ValueError("La taille du noyau doit être impaire.")

    image_array = np.array(image)
    result = image_array.copy()

    k = kernel_size // 2

    for channel in range(image_array.shape[2]):
        channel_array = image_array[..., channel].astype(float)

        # Créer des fenêtres glissantes en utilisant des opérations de découpage
        rows, cols = channel_array.shape
        windows = np.zeros((rows - kernel_size + 1, cols - kernel_size + 1, kernel_size, kernel_size))
        for i in range(rows - kernel_size + 1):
            for j in range(cols - kernel_size + 1):
                windows[i, j] = channel_array[i:i + kernel_size, j:j + kernel_size]

        # Calculer le filtre médian pour chaque fenêtre
        median_values = np.median(windows, axis=(2, 3))

        # Mettre à jour le résultat avec les valeurs médianes calculées
        result[k:-k, k:-k, channel] = median_values

    return Image.fromarray(result.astype('uint8'))


from PIL import Image
import numpy as np


def hole_filling_color(image, kernel_size):
    # Assurez-vous que la taille du noyau est impaire
    if kernel_size % 2 == 0:
        raise ValueError("La taille du noyau doit être impaire.")

    # Copiez l'image pour ne pas modifier l'original
    result = image.copy()

    image_array = np.array(image)

    # Obtenez la moitié de la taille du noyau
    k = kernel_size // 2

    # Parcourez l'image en laissant un cadre de k pixels autour
    for i in range(k, image_array.shape[0] - k):
        for j in range(k, image_array.shape[1] - k):
            # Vérifiez si le pixel actuel est noir (0, 0, 0) et si oui, remplissez-le
            if np.all(image_array[i, j] == [0, 0, 0]):
                neighborhood = image_array[i - k:i + k + 1, j - k:j + k + 1]

                # Remplacez le pixel noir par la valeur médiane des pixels voisins non noirs
                non_zero_values = neighborhood[~np.all(neighborhood == [0, 0, 0], axis=2)]
                if non_zero_values.size > 0:
                    median_value = tuple(np.median(non_zero_values, axis=0).astype(int))
                    result.putpixel((j, i), median_value)

    return result


def gaussian_filter(image, kernel_size, sigma):
    # Convertir l'image en mode L (niveaux de gris) si ce n'est pas déjà le cas
    if image.mode != 'L':
        image = image.convert('L')

    # Convertir l'image en tableau NumPy
    img_array = np.array(image)

    # Appliquer le filtre gaussien avec la méthode ImageFilter.GaussianBlur
    pil_image = Image.fromarray(img_array)
    filtered_image = pil_image.filter(ImageFilter.GaussianBlur(radius=kernel_size))

    return filtered_image

# # Charger une image depuis un fichier
# image = cv2.imread("ShotNoise.png", cv2.IMREAD_COLOR)
#
# # Appliquer le filtre médian avec une taille de noyau de 3x3
# kernel_size = 3
# filtered_image = median_filter_color(image, kernel_size)
# filled_image = hole_filling_color(image, kernel_size)
#
# kernel_size = 5
# sigma = 1.5
# smoothed_image = gaussian_filter(image, kernel_size, sigma)
#
# # Afficher l'image originale et l'image filtrée
# #cv2.imshow('Image Originale', image)
# #cv2.imshow('Image_medianFiltre', filtered_image)
# #cv2.imshow('Image avec Trous Remplis', filled_image)
# #cv2.imshow('Image_Gaussien', smoothed_image)
# cv2.imwrite("Median_Filtre.png", filtered_image)
# cv2.imwrite("Trous_Remplis_Filtre.png", filled_image)
# cv2.imwrite("Gaussian_Filtre.png", smoothed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

