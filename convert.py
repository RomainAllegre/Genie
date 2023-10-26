#fonction nécessite avoir telechargé PyPDF2

import PyPDF2
import os

# Nom du sous-dossier pour les fichiers convertis
output_folder = "filetxt"

# Créer le sous-dossier s'il n'existe pas déjà
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Obtenir la liste des fichiers PDF dans le répertoire courant
pdf_files = [filename for filename in os.listdir() if filename.endswith(".pdf")]

for pdf_filename in pdf_files:
    # Extraction du nom du fichier sans extension
    base_name = os.path.splitext(pdf_filename)[0]
    txt_filename = os.path.join(output_folder, f"{base_name}.txt")  # Chemin du fichier texte

    # Ouvrir le fichier PDF en mode lecture binaire
    with open(pdf_filename, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Créer un nouveau fichier texte pour écrire le texte extrait
        with open(txt_filename, "w", encoding="utf-8") as txt_file:
            # Parcourir chaque page du PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extraire le texte de la page
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # Écrire le texte extrait dans le fichier texte
                txt_file.write(text)



print(f"Conversion des fichiers PDF en fichiers txt terminée.")
