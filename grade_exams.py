import pandas as pd
import numpy as np
import csv, json
from tabulate import tabulate


def input_grade(studentID, examID):

    #Pull Exam Structure
    try:
        with open("./exam_structure.txt", 'r') as e:
            exams = json.load(e)
        exam = exams['itms'][next((index for (index, d) in enumerate(exams['itms']) if d["id"] == examID), None)]
    except TypeError:
        return 'Exam ID not found.'
    except FileNotFoundError:
        return 'exam_structure.txt not found in project directory.\nAsk the System Administrator.'

    #Check Student Exists
    try:
        with open("./student_ids.txt") as s:
            students = json.load(s)
            student = students[next((index for (index, d) in enumerate(students) if d["id"] == studentID), None)]
    except TypeError:
        return 'Student ID not found.'
    except FileNotFoundError:
        return 'student_ids.txt not found in project directory.\nAsk the System Administrator.'
    print('Found Student and Exam!\n')

    #Generate Questionaire
    qtns = ['id'] + [val for pair in zip(
            [e['name'] + '_Mark' for e in exam['frmt']],
            [q['name'] + '_Note' if q['note'] == 'T' else 'kill' for q in exam['frmt']
        ]) for val in pair]
    entry = {'id': studentID}
    for q in qtns[1:]:
        entry[q] = input(q)
    entry = pd.DataFrame(data=entry, index=[0])
    print(entry.T)
    #Write entry to gradebook file




    # 1
    return None


if __name__ == "__main__":
    print("Welcome to the NYCDSA Exam Grader :D")
    print("Please input the following: ")
    studentID = input("Student ID: ")
    examID = input("Exam ID: ")

