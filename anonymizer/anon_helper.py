# NYC DSA Exam Anonimizer helper file
# Created 12-04-2019 by Sam Audino
import pandas as pd
import glob
import random
import os
import re

def label_processor(filename):
    '''
    Accepts file name, extracts student's name based on the enforced naming format:
    "Test_Student_exam.file"
    filename: name of the file to extract the student's name.

    Returns:
    student_name: Student Name in the following format: "Student Name"
    '''

    temp = re.findall("[A-Za-z]+", filename)

    try:
        return temp[0] + " " + temp[1]
    except:
        return temp[0]

def create_key_df(filepath, filetype, exam_name, output_filename, decrypt):
    '''
    Takes a filepath and creates a dataframe containing a conversion key between the
    encoded values and the main value passed. It also saves a CSV version.
    filepath: location of the files you'd like to make into a conversion matrix.

    Returns:
    encoded_df: a dataframe where the index is the anonymized ID, and the columns are
    ['student_name', 'orig_file_name', 'encoded_file_name']
    '''

    if decrypt:
        try:
            return pd.read_csv(filepath+output_filename)
        except:
            raise ValueError("The conversion csv could not be found.")

    exam_desc = "_"+exam_name+filetype

    exams = [x for x in glob.glob(filepath+"*"+filetype) if ("solution" not in x.lower()) and \
                                                   ("anonomizer" not in x.lower())]
    student_id = random.sample(range(len(exams)), len(exams))
    encrypted_file = [filepath+str(x)+desc for id in student_id]
    student_names = [label_processor(x) for x in exams]

    temp_dict = {'id' : student_id,
                 'student_name': student_names,
                 'orig_file_name': exams,
                 'encoded_file_name': encryped_file}

    temp_df = pd.DataFrame.from_dict(temp_dict)
    temp_df.set_index('id')

    temp_df.to_csv(output_filename)

    return temp_df[['orig_file_name', 'encoded_file_name']]

def renameinator(df, decrypt = False):
    '''
    Takes an encoded_df and renames all files within the directory.
    A filepath should not be needed here, as it should be already in the titles from
    the "create_key_df" function.
    df: The dataframe containing the encoding information.

    Returns:
    nothing, just renames files
    '''
    if decrypt:
        for old_name, new_name in zip(df.orig_file_name.values, df.encoded_file_name.values):
            os.rename(new_name, old_name)
    else:
        for old_name, new_name in zip(df.orig_file_name.values, df.encoded_file_name.values):
            os.rename(old_name, new_name)


def file_checker(filepath):
    '''
    Makes sure the filepath exists before continuing. Fixes typical encoding error
    where

    filepath: File path to check.
    '''
    if filepath[-1] != "/":
        filepath += "/"

    try:
        os.listdir(path=filepath)
        return filepath
    except:
        raise ValueError("File Path does not Exist")

def encryptor(filepath = "./", filetype = ".ipynb", exam_name = "default",
              output_filename = "conversion.csv", decrypt = False):
    '''
    This function accepts:
    filepath: a path to where the exams are held, default is PWD
    filetype: the type of file that should be searched for
    exam_name: the name of the exam so the anonomized files aren't just 1,2,3... etc.
    output_filename: the name that they conversion key csv will be saved as.
    decrypt: whether to reverse the effect of the encryption on the files. When this is
             set to True, the output_filename will instead be the file you read in to
             decrypt the data.

    and returns:
    file_dict: A dictonary of the file name conversions.

    The function will rename the files in that directory, so please be careful using this!
    It will also "save" a CSV of what has been converted. If a CSV with the default name
    has already been made it will throw an error.
    '''

    filepath = file_checker(filepath)

    if ((output_filename in os.listdir(path=filepath)) and (not decrypt)):
        raise ValueError("A file with that name already exists, and cannot be created. Please check that the files \
                          are not already encoded.")

    encoded_df = create_key_df(filepath, decrypt=decrypt)

    renameinator(df=encoded_df, decrypt=decrypt)

    return encoded_df

def anonomizer(filepath = "./", filetype = ".ipynb", exam_name = "default", output_filename = "conversion.csv"):
    '''
    This function accepts:
    filepath: a path to where the exams are held, default is PWD
    filetype: the type of file that should be searched for
    exam_name: the name of the exam so the anonomized files aren't just 1,2,3... etc.
    output_filename: the name that they conversion key csv will be saved as.

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
    student_names = [label_processor(x) for x in glob.glob(filepath+"*"+filetype)]
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
