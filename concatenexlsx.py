import os
import pandas as pd
import openpyxl
import shutil
from maskSigma import Mask

def createAtomFile(reponse, path, indice_nom):
    """ exportation des plages en . xlsx"""
    flattened_data = [' - '.join(map(str, pair)) for pair in reponse]

    df= pd.DataFrame(flattened_data)
    new_row= pd.DataFrame([[indice_nom]])
    df = pd.concat([new_row, df]).reset_index(drop=True)
    
    nom_fichier = "plages__" + indice_nom + ".xlsx"
            
    #  export the dataframe  into a single column
    df.to_excel(nom_fichier, index=False, header=False)

    # Move the file to the destination directory
    current_directory = os.getcwd()

    split_strings =path.split("\\")
    # first_string = split_strings[0]
    # second_string = split_strings[1]

    destination_directory = os.path.join(current_directory, split_strings[0], split_strings[1])

    # Remove the file if it already exists in the destination directory
    file_path = os.path.join(destination_directory, nom_fichier)
    if os.path.exists(file_path):
        os.remove(file_path)

    shutil.move(nom_fichier, destination_directory)

def createSynthesisFile (relative_path):


    """ adding all atomic data into a single . xls file """
    # Create a new folder
    # folder_name = "lines_folder"
    # os.makedirs(folder_name, exist_ok=True)
    split_strings =relative_path.split("/")
    directory = '/'.join(split_strings)
    current_directory= os.getcwd()

    print(os.getcwd())

    # Specify the target directory
    target_directory = os.path.join(current_directory, relative_path)
    print("Target directory:", target_directory)

    # List the files in the target directory
    file_list = os.listdir(target_directory)
    print("Files in the target directory:")
    for file_name in file_list:
        print(file_name)

    # List the .xlsx files beginning by 'plages' in the current directory
    # xlsx_files = [file for file in  os.listdir(directory) if file.endswith('.xlsx')]
    xlsx_files = [file for file in  os.listdir(target_directory) if file.startswith('plages')]
    print("Filtered XLSX files:")
    print(xlsx_files)
    # xlsx_files = [file for file in  os.listdir(directory) if file.endswith('.xlsx') and file.startswith('plages')]
    # xlsx_files = [file for file in  os.listdir(split_strings[0]+'/'+split_strings[1]) if file.endswith('.xlsx') and file.startswith('plages')]
    # Create an empty DataFrame to store the combined lines
    combined_data = pd.DataFrame()

    # Iterate over the .xlsx files
    for file in xlsx_files:
        # Read the file and extract the single column
        file_path = os.path.join(target_directory, file)  # Full file path
        data = pd.read_excel(file_path, header=None).iloc[:, 0]
        # Read the file and extract the single column
        # data = pd.read_excel(file, header=None).iloc[:, 0]
    
        # Append the column to the combined_data DataFrame
        combined_data = pd.concat([combined_data, data], axis=1)

    data_transposed = pd.DataFrame(combined_data).transpose()

    # Export the combined data to a new file
    combined_file = 'combined_file.xlsx'  # Specify the name of the combined file
    # combined_data.to_excel(combined_file, index=False, header=False)
    combined_file_path = os.path.join(target_directory, combined_file)
    
    # Remove the existing combined file if it exists
    if os.path.exists(combined_file_path):
        os.remove(combined_file_path)

    # if os.path.exists(combined_file):
    #     os.remove(combined_file)
    # Export the transposed combined data to a new file
    combined_file = 'combined_file.xlsx'  # Specify the name of the combined file
    data_transposed.to_excel(combined_file, index=False, header=False)

    
    # Move the file to the destination directory
    current_directory = os.getcwd()

    split_strings =relative_path.split('\\')
    destination_directory = os.path.join(current_directory, split_strings[0], split_strings[1])
    shutil.move(combined_file, destination_directory)

    # data_transposed.to_excel(combined_file, index=False, header=False, mode='w')