import pandas as pd
import numpy as np
from tabulate import tabulate


def process_exams(inpath, outpath):
    df = pd.read_csv(inpath)
    filter_students = ['nan', 'AVERAGE', 'ATTEMPTED\n', 'GRADING GUIDE', '5', '4', '3', '2', '1', '0', np.nan, 'NaN']
    students = [name for name in df.Name.values if name not in [filter_students]]
    q1 = [col for col in df.columns.values if col[0] == '1']
    q2 = [col for col in df.columns.values if col[0] == '2']

    for student in students:
        if type(student) == float:
            break
        print(f'Processing {student}')
        grades = df[df.Name == student]
        g1 = tabulate(
            pd.concat([grades[q1].filter(regex='M$').T.rename(index=lambda s: s[:-1]).rename(columns={7: 'mark'}),
                       grades[q1].filter(regex='N$').T.rename(index=lambda s: s[:-1]).rename(columns={7: 'note'}).
                      fillna('').apply(lambda l: l.str.wrap(70))], axis=1), headers='keys', tablefmt='fancy_grid')
        g2 = tabulate(
            pd.concat([grades[q2].filter(regex='M$').T.rename(index=lambda s: s[:-1]).rename(columns={7: 'mark'}),
                       grades[q2].filter(regex='N$').T.rename(index=lambda s: s[:-1]).rename(columns={7: 'note'}).
                      fillna('').apply(lambda l: l.str.wrap(70))],
                      axis=1), headers='keys', tablefmt='fancy_grid')

        report = f"""
MACHINE LEARNING MIDTERM GRADE REPORT\nSTUDENT: {student}\nROOM: {int(grades.Room.iloc[0])}\n\n\
QUESTION 1\n{g1}\n\n\nQUESTION 2\n{g2}\n\nOVERALL COMMENTS: {grades["Exam Notes"].iloc[0]}\n\
EXAM GRADE: {grades["Exam Grade"].iloc[0]} / 10\n\nGRADER: {grades.GRADER.iloc[0]}
"""

        with open(outpath + student + '.txt', 'w') as f:
            f.write(report)
            f.close()

        print('...done')


    return 2


if __name__ == "__main__":
    print(process_exams('./ML_grades.csv', './reports/'))

