# actual anonimizer function

from anon_helper import *

switch_key = ""
i = 0

while switch_key == "":
    print("What would you like to do today? Default is anonymize. [encrypt, decrypt, exit]")

    temp = input()

    if "encr" in temp.lower():
        switch_key = False
    elif "decr" in temp.lower():
        switch_key = True
    elif "exit" in temp.lower():
        exit()
    else:
        print("Please pick one of the options and try again.\n\n")
        if i > 1:
            print("You've entered in a wrong value three times, please restart the program. \n\n")
            exit()
        i+=1

if not switch_key:
    print("\n\n\nYou've selected: Encrypt")
else:
    print("\n\n\nYou've selected: Decrypt")
print("\nPlease enter in the filepath. Hitting return without entering anything will default to the folder that is your PWD.")

temp = input()

user_filepath = "./" if temp == "" else file_checker(temp)

print("\nPlease enter in the filetype of the exam. Hitting return without entering anything will default to '.ipynb'.")

user_filetype = ""

while user_filetype == "":

    temp = input()

    if temp == "":
        user_filetype = ".ipynb"
    elif temp.lower() in [".r", ".ipynb", ".rmd", ".py"]:
        user_filetype = temp
    else:
        print("\nPlease enter a supported exam file ending.")


print("Please enter in the exam name. Hitting return without entering anything will default to 'default'.")

temp = input()

user_examname = "default" if temp == "" else temp

if not switch_key:
    print("Please enter in the name of CSV that will store the information to convert the files later. The default is 'conversion.csv'.")
else:
    print("Please enter the name of the CSV that stores the conversion information. The default is 'conversion.csv'.")

temp = input()

user_outputfile = "conversion.csv" if temp == "" else temp

print("Anonomyzing with settings:","\nFilepath: ", user_filepath,
      "\nFiletype: ", user_filetype, "\nExam Name: ", user_examname,
      "\nOutput CSV: ", user_outputfile)

encryptor(filepath = user_filepath, filetype = user_filetype,
           exam_name = user_examname, output_filename = user_outputfile, decrypt = switch_key)

print("\n\n\nAll done! The key to convert the files back is: ", user_outputfile)
