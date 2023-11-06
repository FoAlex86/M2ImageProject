import cv2
import numpy as np
import argparse

def extract_noise(clean_image_path, noisy_image_path, intensite_max, mult, output_noise_image_path):
    # Charger les images
    clean_image = cv2.imread(clean_image_path, cv2.IMREAD_COLOR)
    noisy_image = cv2.imread(noisy_image_path, cv2.IMREAD_COLOR)

    if clean_image is None or noisy_image is None:
        print("Erreur : Impossible de charger les images.")
        return

    # S'assurer que les images ont la même taille
    if clean_image.shape != noisy_image.shape:
        print("Erreur : Les images n'ont pas la même taille.")
        return


    hauteur, largeur, _ = clean_image.shape
    image_noire = np.zeros((hauteur, largeur, 3), dtype=np.uint8)

    # Soustraire l'image propre de l'image bruitée pour obtenir le bruit
    noise = cv2.absdiff(noisy_image, clean_image)

    # Parcourez l'image pixel par pixel
    for y in range(hauteur):
        for x in range(largeur):

            pixel = noise[y,x]
            intensite = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3

            if(intensite > intensite_max):
                image_noire[y,x] = pixel*mult

    cv2.imwrite(output_noise_image_path, image_noire)

    print("Bruit extrait et enregistré dans", output_noise_image_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de soustraction de bruit entre deux images.")
    parser.add_argument("image1", help="Chemin de l'image propre")
    parser.add_argument("image2", help="Chemin de l'image bruitée")
    parser.add_argument("intensite_max", help="intensité_max")
    parser.add_argument("mult", help="multiplier")
    parser.add_argument("output", help="Chemin de sortie de l'image du bruit")

    args = parser.parse_args()
    extract_noise(args.image1, args.image2, float(args.intensite_max), float(args.mult), args.output)
    #extract_noise(args.image1, "", 4, 30, "noise.png")