import cv2
import numpy as np

def gaussian_filter(image, kernel_size, sigma):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)

# Charger une image depuis un fichier
image = cv2.imread("classroom_512_100.png", cv2.IMREAD_COLOR)

# Appliquer le filtre gaussien avec une taille de noyau de 5x5 et un écart-type de 1.5
kernel_size = 5
sigma = 1.5
smoothed_image = gaussian_filter(image, kernel_size, sigma)

# Afficher l'image originale et l'image lissée
cv2.imshow('Image Originale', image)
cv2.imshow('Image_Gaussien', smoothed_image)
cv2.imwrite("Gaussian_Filtre.png", smoothed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

