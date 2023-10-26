# -*- coding: utf-8 -*-

import os
import sys
import shutil

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
        print("Utilisation: python donne_txt.py <chemin_dossier>")
    else:
        input_folder = sys.argv[1]
        donne_txt(input_folder)
