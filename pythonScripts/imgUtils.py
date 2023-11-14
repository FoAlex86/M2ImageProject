import cv2
import matplotlib.pyplot as plt

def writeHistoRGB(image, channel, name):

    # Calculer l'histogramme
    hist = cv2.calcHist([image], [channel], None, [256], [0, 256])

    # Dessiner l'histogramme
    plt.figure()
    plt.title('Histogramme de l\'image')
    plt.xlabel('Niveau de gris')
    plt.ylabel('Nombre de pixels')
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.savefig('dat/' + name + '.png')

def showHistoRGB(image, channel):

    # Calculer l'histogramme
    hist = cv2.calcHist([image], [channel], None, [256], [0, 256])

    # Dessiner l'histogramme
    plt.figure()
    plt.title('Histogramme de l\'image')
    plt.xlabel('Niveau de gris')
    plt.ylabel('Nombre de pixels')
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()

def writeHistoRGB_allChannels(image, name):
    # Séparation des canaux RVB
    b, g, r = cv2.split(image)

    # Calcul des histogrammes pour chaque canal
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])

    # Création d'une seule figure pour l'histogramme combiné
    plt.figure()
    plt.title('Histogramme des canaux RVB de l\'image')
    plt.xlabel('Niveau de couleur')
    plt.ylabel('Nombre de pixels')

    # Tracer les histogrammes combinés des canaux RVB
    plt.plot(hist_r, color='red', label='Rouge')
    plt.plot(hist_g, color='green', label='Vert')
    plt.plot(hist_b, color='blue', label='Bleu')

    # Définition des légendes et des limites
    plt.legend()
    plt.xlim([0, 256])

    # Enregistrement de l'histogramme combiné dans un fichier
    plt.savefig('dat/histoAllChannels ' + name + '.png')

def show_image(image, window_name='Image'):
    """
    Affiche une image avec OpenCV.

    :param image: Image à afficher.
    :param window_name: Nom de la fenêtre (par défaut 'Image').
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()