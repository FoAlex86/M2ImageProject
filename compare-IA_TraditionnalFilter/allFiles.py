import shutil
import os
import sys

def copy_and_rename_image_by_index(source_folder, index, destination_folder, new_filename):
    # Récupérer la liste triée des fichiers dans le dossier source
    files = sorted(os.listdir(source_folder))

    # Vérifier que l'index est valide
    if index < 0 or index >= len(files):
        print(f"L'index {index} n'est pas valide pour le dossier source.")
        return

    # Sélectionner le fichier à copier en utilisant l'index
    filename_to_copy = files[index]

    # Construire les chemins source et destination
    source_path = os.path.join(source_folder, filename_to_copy)
    destination_path = os.path.join(destination_folder, new_filename)

    # Copier et renommer le fichier
    shutil.copyfile(source_path, destination_path)

    print(f"Image copiée et renommée avec succès : {new_filename}")

if __name__ == "__main__":
    # Vérifier le nombre d'arguments
    if len(sys.argv) != 2:
        print("Utilisation : python script.py index")
        sys.exit(1)

    # Récupérer l'index depuis la ligne de commande
    index_to_copy = int(sys.argv[1])
# base

target_folder = os.getcwd()  # Dossier courant


####################################################
# Original
source_folder = "./original"
new_image_name = "0.png"

copy_and_rename_image_by_index(source_folder, index_to_copy, target_folder, new_image_name)

####################################################
# Gaussian noise
source_folder = "./noisy/gaussian"
new_image_name = "1.png"

copy_and_rename_image_by_index(source_folder, index_to_copy, target_folder, new_image_name)

####################################################
# Poisson noise
source_folder = "./noisy/poisson"
new_image_name = "2.png"

copy_and_rename_image_by_index(source_folder, index_to_copy, target_folder, new_image_name)

####################################################
# Gaussian
source_folder = "./gaussian"
new_image_name = "3.png"

copy_and_rename_image_by_index(source_folder, index_to_copy, target_folder, new_image_name)

####################################################
# Poisson
source_folder = "./poisson"
new_image_name = "4.png"

copy_and_rename_image_by_index(source_folder, index_to_copy, target_folder, new_image_name)
