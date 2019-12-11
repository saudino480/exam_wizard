# NYC DSA Exam Anonimizer helper file
# Created 12-04-2019 by Sam Audino
import pandas as pd
import zipfile as zp
import numpy as np
import glob
import random
import os
import re
import json

def label_processor(filename):
    '''
    Accepts file name, extracts student's name based on the enforced naming format:
    "Test_Student_exam.file"
    filename: name of the file to extract the student's name.

    Returns:
    student_name: Student Name in the following format: "Student Name"
    '''
    temp = filename.split("/")[-1]

    temp = re.findall("[A-Z][a-z]+", temp)

    try:
        return temp[0] + " " + temp[1]
    except:
        return temp[0]


def load_json_to_df(file, json_type = "student"):
    '''
    Loads a json file and handles the processing to dataframe. Returns a dataframe.
    file: filepath to the JSON file wishing to be processed.

    Returns:
    linking_df: a Dataframe constructed from the JSON file.
    '''
    if json_type.lower() == "student":
        # attempting to preserve JSON format order.
        linking_df = pd.DataFrame(columns = ["name", "perm_id", "temp_id", "rm", "email", "slack"])
    elif json_type.lower() == 'exam':
        # will be written later
        pass
    else:
        linking_df = pd.DataFrame()

    with open(file) as f:
        students = json.load(f)
        for student in students:
            linking_df = linking_df.append(student, ignore_index = True)

    return linking_df

def json_format_preserver(df, json_filename):
    '''
    A shortcut way to make sure that the JSON file has its format preserved.
    Takes:
    df: a dataframe that wants to be converted to JSON format.
    json_filename: the filename of the JSON file. If it is not in the PWD, please
                   include the absolute filepath.

    Returns:
    None
    '''

    formatter = json.loads(df.to_json(orient='records'))

    with open(json_filename, 'w') as f:
        json.dump(formatter, f, indent=4)

def create_key_df(filepath, student_filepath, filetype, exam_name, output_filename, decrypt):
    '''
    Takes a filepath and creates a dataframe containing a conversion key between the
    encoded values and the main value passed. It also saves a CSV version.
    filepath: location of the files you'd like to make into a conversion matrix.
    student_filepath: where the student_id JSON is saved.
    filetype: filetype of the exam.
    exam_name: the exam name to be encoded.
    output_filename: name of the conversion CSV to be saved as.
    decrypt: whether to encrypt or decrypt.

    Returns:
    encoded_df: a dataframe where the index is the anonymized ID, and the columns are
    ['orig_file_name', 'encoded_file_name']
    '''

    if decrypt:
        try:
            return pd.read_csv(filepath+output_filename)
        except:
            try:
                return pd.read_csv(output_filename)
            except:
                raise ValueError("The conversion csv could not be found.")

    exam_desc = "_"+exam_name+filetype

    exams = [x for x in glob.glob(filepath+"*"+filetype) if ("solution" not in x.lower()) and \
                                               ("anonomizer" not in x.lower())]
    student_names = [label_processor(x) for x in exams]

    file_df = pd.DataFrame({"orig_file": exams, "name": student_names})

    linking_df = load_json_to_df(student_filepath)

    left_overs = [student for student in file_df['name'].values if student not in linking_df['name'].values]
    unsubmitted = [student for student in linking_df['name'].values if student not in file_df['name'].values]

    # generate temp_ids
    masked_df = linking_df[linking_df['name'].isin(student_names)]
    masked_df['temp_id'] = random.sample(range(1000,9999), masked_df.shape[0])

    # make sure that users that did not submit an exam have a unique temp_id code.
    unsubmitted_df = linking_df[~linking_df['name'].isin(student_names)]
    unsubmitted_df['temp_id'] = '0000'

    # clean up a little bit, save the result
    linking_df = pd.concat([masked_df, unsubmitted_df], axis = 0)
    linking_df.sort_values('perm_id', inplace = True)
    json_format_preserver(df = linking_df, json_filename = student_filepath)

    # don't need everything moving on, just the name
    reduced_df = linking_df[['name', 'temp_id']]

    # only want to encrypt exams that have names we know!! (a better way to do this would be
    # if we could possible get the email tagged onto the file when we download this; so the user
    # account would be the thing we link on, not if they spelled their name correctly (reduce
    # user error)).
    file_df = pd.merge(reduced_df, file_df, how = 'inner', on='name')
    file_df['encrypt_file'] = [filepath+str(ID)+exam_desc for ID in file_df['temp_id'].values]
    file_df.set_index('temp_id', inplace=True)
    file_df.to_csv(filepath+output_filename)

    if left_overs != []:
        print("The following students are not in the database:")
        for student in left_overs:
            print("\n", student)

    if unsubmitted != []:
        print("\n The following students have not submitted exams, and have been assigned a temporary ID of 0000:")
        for student in unsubmitted:
            print("\n", student)

    return file_df[['orig_file', 'encrypt_file']]


def renameinator(df, decrypt = False):
    '''
    Takes an encoded_df and renames all files within the directory.
    A filepath should not be needed here, as it should be already in the titles from
    the "create_key_df" function.
    df: The dataframe containing the encoding information.
    decrypt: whether to encrypt or decrypt

    Returns:
    nothing, just renames files
    '''
    if decrypt:
        print(df)
        for old_name, new_name in zip(df.orig_file.values, df.encrypt_file.values):
            os.rename(new_name, old_name)
    else:
        for old_name, new_name in zip(df.orig_file.values, df.encrypt_file.values):
            os.rename(old_name, new_name)


def file_checker(filepath):
    '''
    Makes sure the filepath exists before continuing. Fixes typical encoding error
    where the final slash is forgotten.
    Takes:
    filepath: File path to check.

    Returns:
    filepath: A corrected filepath
    '''
    if filepath[-1] != "/":
        filepath += "/"

    try:
        os.listdir(path=filepath)
        return filepath
    except:
        raise ValueError("File Path does not Exist")

def encryptor(filepath = "./", student_file = "./student_ids.txt", filetype = ".ipynb",
              exam_name = "default", output_filename = "conversion.csv", decrypt = False):
    '''
    This function accepts:
    filepath: a path to where the exams are held, default is PWD
    student_filepath: where the student_id JSON is saved, default is student_ids.txt in PWD.
    filetype: the type of file that should be searched for
    exam_name: the name of the exam so the anonomized files aren't just 1,2,3... etc.
    output_filename: the name that they conversion key csv will be saved as.
    decrypt: whether to reverse the effect of the encryption on the files. When this is
             set to True, the output_filename will instead be the file you read in to
             decrypt the data.

    and returns:
    encoded_df: A dataframe of the file name conversions.

    The function will rename the files in that directory, so please be careful using this!
    It will also "save" a CSV of what has been converted. If a CSV with the default name
    has already been made it will throw an error. This choice was made in order to prevent
    people from encrypting their data twice, by accident.
    '''
    override_decrypt = False
    filepath = file_checker(filepath)

    # make sure the user doesn't accidentially overwrite your encryption file.
    if ((output_filename in os.listdir(path=filepath)) and (not decrypt)):
        temp = input("Do you want to use the old conversion schema saved at: "+output_filename+"? [y/[n]]\n")
        if 'y' in temp.lower():
            override_decrypt = True
            pass
        else:
            temp = input("Are you sure you would like to overwrite: "+output_filename+"? [y/[n]")
            if 'y' in temp.lower():
                pass
            else:
                raise ValueError("A file with that name already exists, and cannot be created. Please check that the files \
                                 are not already encoded.")

    if override_decrypt:
        encoded_df = create_key_df(filepath=filepath, student_filepath = student_file, filetype=filetype,
                                   exam_name=exam_name, output_filename = output_filename,
                                   decrypt=override_decrypt)
    else:
        encoded_df = create_key_df(filepath=filepath, student_filepath = student_file, filetype=filetype,
                                   exam_name=exam_name, output_filename = output_filename,
                                   decrypt=decrypt)

    renameinator(df=encoded_df, decrypt=decrypt)

    if decrypt:
        file_check = glob.glob(filepath+"*"+filetype)

        missing = [file for file in file_check if file not in encoded_df.orig_file.values]

        if missing != []:
            print("The following files have not been processed:")
            for m in missing:
                print("\n", m)

    return encoded_df

def distributor(ta_json, file_df):
    '''
    Take a JSON and a dataframe of encrypted exam files and distributes them amongst the TAs.
    Eventually will include a method that automatically emails them to each TA. Until then,
    we output a DF of the TA's emails, and the files that they should be grading.
    ta_json: Filepath of the TA_json.
    file_df: a DF of encoded exams.

    returns
    TA_df: a reduced TA_df containing only the email and exams to grade.
    '''

    TA_df = load_json_to_df('TA_data.txt', json_type='ta')

    exams_per_ta = 1 if file_df.shape[0] // TA_df.shape[0] == 0 else file_df.shape[0] // TA_df.shape[0]

    exams_to_send = file_df['encrypt_file'].values

    # have to shuffle bc knowing the order of the students would allow you to guess whose exam you are grading.
    np.random.shuffle(exams_to_send)

    exams_to_send = np.array_split(exams_to_send, TA_df.shape[0])
    np.random.shuffle(exams_to_send)
    exams_to_send = [list(sub_array) for sub_array in exams_to_send]
    TA_df['exams_to_grade'] = exams_to_send

    for TA, exams in zip(TA_df['name'].values, TA_df['exams_to_grade'].values):
        if exams == []:
            print("TA ", TA, "does not have any exams to grade.")
            continue
        print("Creating zip file for TA", TA+"'s", "exam(s).")
        with zp.ZipFile(TA+'.zip', 'w') as zipper:
            if type(exams) == str:
                print("Writing exam: ", exams)
                zipper.write(exams)
            else:
                for exam in exams:
                    print("Writing exam: ", exam)
                    zipper.write(exam)


    return TA_df[['email', 'exams_to_grade']]
