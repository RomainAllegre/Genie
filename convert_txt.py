# -*- coding: utf-8 -*-

#ce programme prend en argument un nom de dossier avec des fichiers PDF dans le dossier
#puis convertit les fichiers PDF en plain text dans un sous dossier de celui des fichiers PDF
#avec la methode convert_txt, pour apres a partir des fichiers plain text cree un sous-dossier dans celui-ci 
#pour creer les fichiers texte avec pour donnee : le nom du fichier d'origine , le titre du document et l'abstract de l'auteur 

import os
import PyPDF2
import shutil
import re
import xml.etree.ElementTree as ET
import sys

def afficher_liste_fichiers(dossier):
    print("Liste des fichiers dans le dossier:")
    
    fichiers = get_txt_files_in_folder(dossier)
    for i, fichier in enumerate(fichiers, start=1):
        print(f"{i}. {fichier}")

    return fichiers
    
def demander_fichiers_a_convertir():
    fichiers_a_convertir = []
    
    while True:
        choix = input("Entrez le numéro du fichier à convertir (ou 'end'/'exit'/'fin' pour terminer) : ")
        
        if choix.lower() in ['end', 'exit', 'fin']:
            break
        
        try:
            choix = int(choix)
            if 1 <= choix <= len(fichiers):
                fichier_selectionne = fichiers[choix - 1]
                fichiers_a_convertir.append(fichier_selectionne)
                print(f"{fichier_selectionne} ajouté à la liste.")
            else:
                print("Veuillez entrer un numéro valide.")
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    return fichiers_a_convertir
    
def get_txt_files_in_folder(input_folder):
    files = []
    for file in os.listdir(input_folder):
        if os.path.isfile(os.path.join(input_folder, file)) and file.endswith(".txt"):
            files.append(file)
    return files

def convert_txt(input_folder, uniq=None) :
        output_folder = os.path.join(input_folder, "filetxt")

        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        os.mkdir(output_folder)

        if uniq:  # Si uniq est spécifié, convertir uniquement ce fichier (ou liste de fichiers)
            if isinstance(uniq, str):  # Si uniq est une chaîne (un fichier)
                filenames_to_convert = [uniq]
            elif isinstance(uniq, list):  # Si uniq est une liste de fichiers
                filenames_to_convert = uniq
            else:
                raise ValueError("uniq doit être une chaîne (fichier) ou une liste de fichiers.")
        else:  # Sinon, convertir tous les fichiers PDF dans le dossier
            filenames_to_convert = [filename for filename in os.listdir(input_folder) if filename.endswith(".pdf")]

        for filename in filenames_to_convert:
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



def extract_abstract_author(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)

            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                author = metadata.author

                if author is not None:
                    return author.strip()

    return None  

        

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


def extract_corps_from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            corps_start = False
            corps = ""
            
            for line in lines:
                if any(keyword in line for keyword in ['2.', 'II', '2 Related' , 'RELATED', '2 Method', 'METHOD', '2Previous Work', 'Performance Measure', '2 Previous Work']):
                    corps_start = True
                    corps += line.strip()
                
                if any(word in line for word in ["Conclusions", "References", "Discussion", "Conclusion", "CONCLUSIONS"]):
                    break
                
                if corps_start:
                    corps += line.strip()

        return corps.strip()



def extract_intro_from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            intro_started = False
            intro = ""
            for line in lines:
                if "introduction" in line.lower() or "ntroduction" in line.lower():
                    intro_started = True
                
                if intro_started:
                    if any(word in line.upper() for word in ['II.', '2.', 'Related Work', 'related work', '2 Related Work', "concluding"]):
                        break
                    elif line.strip() and line.strip()[0] == '2' and (line.strip()[1].isupper() or line.strip()[1].isdigit()) :
                        break
                    intro += line.strip()
                    
            return intro.strip()

def extract_conclusion_from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            conclu_started = False
            conclu = ""
            for line in lines:
                if "Conclusions" in line.lower():
                    conclu_started = True
                
                if conclu_started:
                    if any(word in line.upper() for word in ["REFERENCES", "REFERENCE", "DISCUSSION", "DISCUSSIONS"]):
                        break
                    conclu += line.strip()
                    
            return conclu.strip()

def extract_discussion_from_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            discu_started = False
            discu = ""
            for line in lines:
                if "Discussion" in line.lower():
                    discu_started = True
                
                if discu_started:
                    if any(word in line.upper() for word in ["REFERENCES", "REFERENCE", "CONCLUSIONS", "CONCLUSION"]):
                        break
                    discu += line.strip()
                    
            return discu.strip()

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


def donne_xml(input_folder):
        output_folder = os.path.join(input_folder, "output_xml")  # CORPUS_TRAIN/filetxt/output_xml
        
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)

        os.makedirs(output_folder, exist_ok=True)
        corpus_train_folder =  os.path.abspath(os.path.join(input_folder, os.pardir))

        for filename in os.listdir(input_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(input_folder, filename)
                title = extract_title_from_file(file_path)
                abstract = extract_abstract_from_file(file_path)
                autor = extract_abstract_author(corpus_train_folder)
                biblio = extract_biblio_from_file(file_path)
                crps = extract_corps_from_file(file_path)
                intro = extract_intro_from_file(file_path)
                discu = extract_discussion_from_file(file_path)
                conclu = extract_conclusion_from_file(file_path)
                
                filename_without_extension = os.path.splitext(filename)[0]
                output_file_name = "{}.xml".format(filename_without_extension)
                output_file_path = os.path.join(output_folder, output_file_name)
                print(output_file_path)

                root = ET.Element("article")
                
                preamble= ET.SubElement(root, "preamble")
                preamble.text = filename_without_extension
                title_element = ET.SubElement(root, "titre")
                title_element.text = title
                auteur = ET.SubElement(root, "auteur")
                auteur.text = autor
                abstract_element = ET.SubElement(root, "abstract")
                abstract_element.text = abstract
                intro_element = ET.SubElement(root, "introduction")
                intro_element.text = intro
                corps_element = ET.SubElement(root, "corps")
                corps_element.text = crps
                discu_element = ET.SubElement(root, "discussion")
                discu_element.text = discu
                conclu_element = ET.SubElement(root, "conclusion")
                conclu_element.text = conclu
                bibi = ET.SubElement(root, "biblio")
                bibi.text = biblio

                tree = ET.ElementTree(root)
                
                with open(output_file_path, 'wb') as output_file:
                    tree.write(output_file)


def get_txt_files_in_folder(input_folder):
        files = []
        for file in os.listdir(input_folder):
            if os.path.isfile(os.path.join(input_folder, file)):
                files.append(file)
        return files
        
if __name__ == "__main__":

        if len(sys.argv) != 3:
            print("Utilisation: python3 convert_txt.py <chemin_dossier> [-t | -x]")
        else:
            input_folder = sys.argv[1]
            fichiers = afficher_liste_fichiers(input_folder)
            fichiers_a_convertir = demander_fichiers_a_convertir()
            
            if fichiers_a_convertir:
                convert_txt(input_folder, fichiers_a_convertir)
                if len(sys.argv) == 3:
                    option = sys.argv[2]
                    if option == "-t":
                        print("Option -t détectée")
                        donne_txt(os.path.join(input_folder, "filetxt"))
                    elif option == "-x":
                        print("Option -x détectée")
                        donne_xml(os.path.join(input_folder, "filetxt"))
                    else:
                        print("Option non reconnue")
