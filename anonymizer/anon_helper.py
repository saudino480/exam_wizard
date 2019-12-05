# NYC DSA Exam Anonimizer helper file
# Created 12-04-2019 by Sam Audino
import pandas as pd
import glob
import random
import os

def file_checker(filepath):
    '''
    Makes sure the filepath exists before continuing.

    filepath: File path to check.
    '''
    if filepath[-1] != "/":
        filepath += "/"

    try:
        os.listdir(path=filepath)
        return filepath
    except:
        raise ValueError("File Path does not Exist")

def anonomizer(filepath = "./", filetype = ".ipynb", exam_name = "default", output_filename = "conversion.csv"):
    '''
    This function accepts:
    filepath: a path to where the exams are held, default is PWD
    filetype: the type of file that should be searched for
    exam_name: the name of the exam so the anonomized files aren't just 1,2,3... etc.
    output_filename: the name that the conversion key csv will be saved as.

    and returns:
    file_dict: A dictonary of the file name conversions.

    The function will rename the files in that directory, so please be careful using this!
    It will also "save" a CSV of what has been converted. If a CSV with the default name
    has already been made it will throw an error.
    '''
    if filepath[-1] != "/":
        filepath+= "/"

    if output_filename in os.listdir(path=filepath):
        print("error goes here (listdir)")

        return ""

    exam_desc = "_"+exam_name+filetype
    exams = [x for x in glob.glob(filepath+"*"+filetype) if ("solution" not in x.lower()) and \
                                                   ("anonomizer" not in x.lower())]
    values = [filepath+str(x)+exam_desc for x in random.sample(range(len(exams)), len(exams))]
#    print(exams, values)
    file_dict = dict(zip(exams, values))

    for x,y in file_dict.items():
        os.rename(x, y)

    key_csv = pd.DataFrame.from_dict(file_dict, orient="index")
    key_csv.columns = ['Anonomized']
    key_csv.index.name = "Original File"
    key_csv.to_csv(filepath+output_filename)

    return file_dict

def decrypter(filepath = "./", filetype = ".ipynb", key_csv = "conversion.csv"):
    '''
    Partner function to anonomizer. Takes anonomized files and decrypts them.
    filepath: path to the directory
    filetype: type of file, or list of file types
    key_csv: the CSV containing the keys in which to convert the data back to CSV.

    If the files are successfully converted back, the key CSV will be deleted.
    '''

    if filepath[-1] != "/":
        filepath += "/"

    if key_csv not in os.listdir(path=filepath):
        print("error goes here (listdir)")

        return ""


    key_df = pd.read_csv(filepath+key_csv, index_col = "Original File")
#     print(key_csv)
    key_dict = key_df.to_dict(orient = "index")

    for x,y in key_dict.items():
#         print("old_name: ", y[key_csv.columns[0]], "\nnew_name: ", x)
        os.rename(y[key_df.columns[0]], x)

    left_overs = [y[key_df.columns[0]] for y in key_dict.values() if y[key_df.columns[0]] in glob.glob(filepath+"*"+filetype)]

    if left_overs != []:
        print("Unconverted files! Cannot delete the conversion table.")
        return key_dict
    else:
        print("Deleting conversion table.")
        os.remove(filepath+key_csv)

    return key_dict
