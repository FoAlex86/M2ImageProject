# Denoizingz : Application de débruitage d'images avec la méthode Noise2Noise

Denoizingz est une application capable de débruiter des images bruitées par des bruits de Gauss ou de poisson avec la méthode Noise2Noise. Mais il est aussi possible de débruiter du bruits impulsionnel avec un filtre bilatéral a trou. Tout ceci dans une interface graphique.

# Installation : 

- ## Installer Noise2Noise

    Noise2Noise => https://github.com/NVlabs/noise2noise

    ### Installer l'environnement conda :

    - conda create -n n2n python=3.6
    - conda activate n2n
    - conda install tensorflow-gpu=1.14.0
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt
    - pip install numpy==1.16.4

    ### Pour la suite suivre les instruction du git Noise2Noise

    ### Pour utiliser notre interface graphique :
    - importer les fichier main.py et allFilter.py depuis le dossier GUI vers la racine du projet Noise2Noise préalablement téléchargé
    - Éxecuter main.py

Méthode Noise2Noise : https://arxiv.org/abs/1803.04189