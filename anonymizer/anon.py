# actual anonimizer function

from anon_helper import anonomizer, decrypter, file_checker

switch_key = ""
i = 0

while switch_key == "":
    print("What would you like to do today? Default is anonymize. [anonymize, decrypt]")

    temp = input()

    if "anon" in temp.lower():
        switch_key = True
    elif "decr" in temp.lower():
        switch_key = False
    elif "exit" in temp.lower():
        exit()
    else:
        print("Please pick one of the options and try again.\n\n")
        if i > 1:
            print("You've entered in a wrong value three times, please restart the program. \n\n")
            exit()
        i+=1

if switch_key:
    print("\n\n\nYou've selected: Anonymize")
    print("\nPlease enter in the filepath. Hitting return without entering anything will default to the folder that this bash file is currently located in.")

    temp = input()

    user_filepath = "./" if temp == "" else file_checker(temp)

    print("Please enter in the filetype of the exam. Hitting return without entering anything will default to '.ipynb'.")

    temp = input()

    user_filetype = ".ipynb" if temp == "" else temp

    print("Please enter in the exam name. Hitting return without entering anything will default to 'default'.")

    temp = input()

    user_examname = "default" if temp == "" else temp

    print("Please enter in the name of CSV that will store the information to convert the files later. The default is 'conversion.csv'.")

    temp = input()

    user_outputfile = "conversion.csv" if temp == "" else temp

    print("Anonomyzing with settings:","\nFilepath: ", user_filepath,
          "\nFiletype: ", user_filetype, "\nExam Name: ", user_examname,
          "\nOutput CSV: ", user_outputfile)

    anonomizer(filepath = user_filepath, filetype = user_filetype,
               exam_name = user_examname, output_filename = user_outputfile)

    print("\n\n\nAll done! The key to convert the files back is: ", user_outputfile)

else:
    print("\n\n\nYou've selected: Decrypt")
    print("Please enter in the filepath. Hitting return without entering anything will default to the folder that this bash file is currently located in.")

    temp = input()

    user_filepath = "./" if temp == "" else file_checker(temp)

    print("Please enter in the filetype of the exam. Hitting return without entering anything will default to '.ipynb'.")

    temp = input()

    user_filetype = ".ipynb" if temp == "" else temp

    print("Please enter in the name of the CSV containing the encryption data. Hitting return without entering anything will default to 'default'.")

    temp = input()

    user_keycsv = "conversion.csv" if temp == "" else temp

    print("Anonomyzing with settings:","\nFilepath: ", user_filepath,
          "\nFiletype: ", user_filetype, "\nKey CSV: ", user_keycsv)

    decrypter(filepath = user_filepath, filetype = user_filetype,
              key_csv = user_keycsv)

    print("\n\n\nAll done!")
