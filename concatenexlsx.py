import os
import pandas as pd
# import openpyxl
import shutil
from maskSigma import Mask

""" create or replace a plages_'atom'.xlsx file for a given atom and store its plages= ranges inside
Parameters
        ----------
        reponse : 2D numpy array
            a range (plage)
        path : str
            where store the created file
        indice_nom  : str
            name of the atom 
        """
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

    split_strings =path.split("/")
    
    destination_directory = os.path.join(current_directory, split_strings[0], split_strings[1])

    # Remove the file if it already exists in the destination directory
    file_path = os.path.join(destination_directory, nom_fichier)
    if os.path.exists(file_path):
        os.remove(file_path)

    shutil.move(nom_fichier, destination_directory)

""" create or replace the combined_file.xlsx file from all the existing plages_'atom'.xlsx 
Parameters
        ----------
        relative_path : str
            relative path, where the plages_'atom'.xlsx come from and where combined_file.xlsx is placed
        """
def createSynthesisFile (relative_path):

    """ adding all atomic data into a single . xls file """
    split_strings =relative_path.split("/")
    current_directory= os.getcwd()

        # Specify the target directory
    target_directory = os.path.join(current_directory, relative_path)
           
    # List the .xlsx files beginning by 'plages' in the current directory
    xlsx_files = [file for file in  os.listdir(target_directory) if file.startswith('plages')]
    
    # Create an empty DataFrame to store the combined lines
    combined_data = pd.DataFrame()

    # Iterate over the .xlsx files
    for file in xlsx_files:
        # Read the file and extract the single column
        file_path = os.path.join(target_directory, file)  # Full file path
        data = pd.read_excel(file_path, header=None).iloc[:, 0]
            
        # Append the column to the combined_data DataFrame
        combined_data = pd.concat([combined_data, data], axis=1)

    data_transposed = pd.DataFrame(combined_data).transpose()

    # Export the combined data to a new file
    combined_file = 'combined_file.xlsx'  # Specify the name of the combined file
    combined_file_path = os.path.join(target_directory, combined_file)
    
    # Remove the existing combined file if it exists
    if os.path.exists(combined_file_path):
        os.remove(combined_file_path)

    # Export the transposed combined data to a new file
    combined_file = 'combined_file.xlsx'  # Specify the name of the combined file
    data_transposed.to_excel(combined_file, index=False, header=False)

    
    # Move the file to the destination directory
    current_directory = os.getcwd()

    split_strings =relative_path.split('/')
    destination_directory = os.path.join(current_directory, split_strings[0], split_strings[1])
    shutil.move(combined_file, destination_directory)
