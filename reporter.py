import pandas as pd
import numpy as np
import csv, json
from tabulate import tabulate
from datetime import datetime


def report_grades(examID):
    # Load Exam Structure
    with open("./exam_structure.txt", 'r') as e:
        exams = json.load(e)
    exam = exams['itms'][next((index for (index, d) in enumerate(exams['itms']) if d["id"] == examID), None)]

    # Load exams gradebook
    grades = pd.read_csv(exam['path'], converters={'SID': lambda l: str(l)}).\
        sort_values('timestamp').drop_duplicates('SID', keep='last')

    # Load student database
    with open("./student_ids.txt", 'r') as s:
        students = json.load(s)

    def compile_report(entry, roster):
        """
        entry: pandas series
        """
        student = roster[next((index for (index, d) in enumerate(roster) if d["id"] == entry.SID.iloc[0]), None)]

        report = f"{exam.name.upper()} GRADE REPORT\nSTUDENT: {student.name.iloc[0]}\nROOM: {student.rm.iloc[0]}\n\n\\"






        # QUESTION 1\n{g1}\n\n\nQUESTION 2\n{g2}\n\nOVERALL COMMENTS: {grades["Exam Notes"].iloc[0]}\n\
        # EXAM GRADE: {grades["Exam Grade"].iloc[0]} / 10\n\nGRADER: {grades.GRADER.iloc[0]}









if __name__ == "__main__":
    report_grades("0000")



