# -*- coding: utf-8 -*-

#ce programme prend en argument un nom de dossier avec des fichiers PDF dans le dossier
#puis convertit les fichiers PDF en plain text dans un sous dossier de celui des fichiers PDF
#avec la methode convert_txt, pour apres a partir des fichiers plain text cree un sous-dossier dans celui-ci 
#pour creer les fichiers texte avec pour donnee : le nom du fichier d'origine , le titre du document et l'abstract de l'auteur 

import PyPDF2
import os
import sys
import shutil
import re
import xml.etree.ElementTree as ET

def convert_txt(input_folder) :
    output_folder = os.path.join(input_folder, "filetxt")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
        
    os.mkdir(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf") :
            base_name = os.path.splitext(filename)[0]
            txt_filename = os.path.join(output_folder, f"{base_name}.txt")

            with open(os.path.join(input_folder, filename), "rb") as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)

                with open(txt_filename, "w") as txt_file:
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        txt_file.write(text)

def extract_title_from_file(file_path):
    with open(file_path, 'r') as file:
        title = file.readline().strip()
    return title

def extract_abstract_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        abstract_started = False
        abstract = ""
        for line in lines:
            if abstract_started or "abstract" in line.lower():
                if any(word in line.upper() for word in ["I.","1.","INTRODUCTION","Introduction"]):
                    break
                abstract_started = True
                abstract += line.strip()
        if not abstract_started :
            for line in lines:
                if any(word in line.upper() for word in ["I.","1."]):
                    break
                abstract_started = True
                abstract += line.strip()
        return abstract.strip()


def extract_abstract_author(pdf_path):
	 with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Obtenez les métadonnées du document PDF
            metadata = pdf_reader.getDocumentInfo()
            
            # Récupérez l'auteur du document s'il est disponible
            author = metadata.author
            
            if author:
                return author
            else:
                return "Auteur non spécifié"
	

def extract_biblio_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        biblio_started = False
        biblio = ""
        for line in lines:
            match = re.search(r'\breferences\b', line, flags=re.IGNORECASE)
            if match:
                biblio_started = True
            if biblio_started:
                biblio += line.strip()
        return biblio.strip()



def donne_txt(input_folder):
    output_folder = os.path.join(input_folder, "output_txt")  #CORPUS_CONV/output_txt
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    
    os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            title = extract_title_from_file(file_path)
            abstract = extract_abstract_from_file(file_path)

            output_file_name = "{}.txt".format(title)
            output_file_path = os.path.join(output_folder, filename)
            print(output_file_path)
            
            with open(output_file_path, 'w') as output_file:
                output_file.write(filename + '\n')
                output_file.write(title + '\n')
                output_file.write(abstract)

"""
def donne_xml(input_folder):
    output_folder = os.path.join(input_folder, "output_xml")
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            title = extract_title_from_file(file_path)
            abstract = extract_abstract_from_file(file_path)

            output_file_name = "{}.xml".format(title)
            output_file_path = os.path.join(output_folder, output_file_name)

            root = ET.Element("article")
            ET.SubElement(root, "preambule").text = filename
            ET.SubElement(root, "titre").text = title
            ET.SubElement(root, "abstract").text = abstract

            tree = ET.ElementTree(root)
            
            # Ensure the directory structure exists
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            with open(output_file_path, 'wb') as output_file:
                tree.write(output_file, encoding="utf-8")
"""

def donne_xml(input_folder):
    output_folder = os.path.join(input_folder, "output_xml")  # CORPUS_TRAIN/filetxt/output_xml
    
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            title = extract_title_from_file(file_path)
            abstract = extract_abstract_from_file(file_path)
            #autor = extract_abstract_author(file_path)
            biblio = extract_biblio_from_file(file_path)
            filename_without_extension = os.path.splitext(filename)[0]
            output_file_name = "{}.xml".format(filename_without_extension)
            output_file_path = os.path.join(output_folder, output_file_name)
            print(output_file_path)

            root = ET.Element("article")
            
            preamble= ET.SubElement(root, "preamble")
            preamble.text = filename_without_extension
            title_element = ET.SubElement(root, "titre")
            title_element.text = title
            #auteur = ET.SubElement(root, "auteur")
            #auteur.text = autor
            abstract_element = ET.SubElement(root, "abstract")
            abstract_element.text = abstract
            bibi = ET.SubElement(root, "biblio")
            bibi.text = biblio

            tree = ET.ElementTree(root)
            
            with open(output_file_path, 'wb') as output_file:
                tree.write(output_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation: python convert_txt.py <chemin_dossier> [-t | -x]")
    else:
        input_folder = sys.argv[1]
        convert_txt(input_folder)

        if len(sys.argv) == 3:
            option = sys.argv[2]
            if option == "-t":
                print("Option -t détectée")
                donne_txt(input_folder + "/filetxt")
            elif option == "-x":
                print("Option -x détectée")
                donne_xml(input_folder + "/filetxt")
            else:
                print("Option non reconnue")
