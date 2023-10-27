# -*- coding: utf-8 -*-

#ce programme prend en argument un nom de dossier avec des fichiers PDF dans le dossier
#puis convertit les fichiers PDF en plain text dans un sous dossier de celui des fichiers PDF
#avec la methode convert_txt, pour apres a partir des fichiers plain text cree un sous-dossier dans celui-ci 
#pour creer les fichiers texte avec pour donnee : le nom du fichier d'origine , le titre du document et l'abstract de l'auteur 

import PyPDF2
import os
import sys
import shutil

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


def donne_txt(input_folder):
    output_folder = os.path.join(input_folder, "output")  #CORPUS_CONV/output
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Utilisation: python convert_txt.py <chemin_dossier>")
    else:
        input_folder = sys.argv[1]
        convert_txt(input_folder)
        donne_txt(input_folder + "/filetxt")