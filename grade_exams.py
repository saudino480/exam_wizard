import pandas as pd
import numpy as np
import csv, json, sys, os
from tabulate import tabulate
from datetime import datetime


def input_grade(studentID, examID):

    # Pull Exam Structure
    try:
        with open("./exam_structure.txt", 'r') as e:
            exams = json.load(e)
        exam = exams['itms'][next((index for (index, d) in enumerate(exams['itms']) if d["id"] == examID), None)]
    except TypeError:
        print('Exam ID not found.')
        return None
    except FileNotFoundError:
        print('exam_structure.txt not found in project directory.\nAsk the System Administrator.')
        return None
    except:
        print("Unexpected Error:", sys.exc_info()[0])
        return None

    # Check Student Exists
    try:
        with open("./student_ids.txt") as s:
            students = json.load(s)
            student = students[next((index for (index, d) in enumerate(students) if d["id"] == studentID), None)]
    except TypeError:
        print('Student ID not found.')
        return None
    except FileNotFoundError:
        print('student_ids.txt not found in project directory.\nAsk the System Administrator.')
        return None
    except:
        print("Unexpected Error:", sys.exc_info()[0])
        raise

    # Check if student has been graded and user wants to overwrite.
    try:
        g = pd.read_csv(exam['path'], converters={'SID': lambda x: str(x)}).set_index('SID')
        if studentID in g.index.values:
            print('Student is already graded')
            print(g[g.index == studentID].T)
            overwrite = ""
            while overwrite != 'Y':
                overwrite = input("Overwrite student grade? (Y/N)")
                if overwrite == 'N':
                    return None
    except FileNotFoundError:
        pass

    # Generate Grading Input Format
    entry = {}
    for elem in exam['frmt']:
        entry[elem['name']] = input(elem['name'] + "_Mark: ")
        while entry[elem['name']] == "" and elem["optn"] == "F":
            print(elem['name'] + ' is not Optional.')
            entry[elem['name']] = input(elem['name'] + "_Mark: ")
        if elem['note'] == 'T':
            entry[elem['name']+'_Note'] = input(elem['name']+'_Note:')
    entry['SID'] = studentID
    entry['GRADER'] = input('Enter your name: ')
    entry['timestamp'] = datetime.now().time()
    entry = pd.DataFrame(data=entry, index=[0]).set_index('SID')

    if not os.path.isfile(exam['path']):
        entry.to_csv(exam['path'], header='column_names')
    else:
        entry.to_csv(exam['path'], mode='a', header=False)

    return None


if __name__ == "__main__":
    print("Welcome to the NYCDSA Exam Grader :D")
    print("Please input the following: ")
    studentID = input("Student ID: ")
    examID = input("Exam ID: ")
    input_grade(studentID, examID)
