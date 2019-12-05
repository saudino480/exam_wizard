import pandas as pd
import numpy as np
import csv
from tabulate import tabulate

input_python_grade


if __name__ == "__main__":
    print("Welcome to the NYCDSA Exam Grader :D")
    print("Please input the following: ")
    studentID = int(input("Student ID: "))
    examID = input("Exam ID: ")

    if examID == 'Python Midterm':
        input_python_grade(studentID)
    elif examID == 'R Midterm':
        input_r_grade(studentID)
    elif examID == 'ML Midterm':
        input_ml_grade(studentID)
    elif examID == 'Final Exam':
        input final_grade(studentID)
    else:
        print('Exam ID not recognized')