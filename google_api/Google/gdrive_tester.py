from google_apps import GDrive, GMail

myDrive = GDrive()

file_link = myDrive.upload_file('Charlie.zip')

myGmail = GMail("charles.cohen@nycdatascience.com")

msg = myGmail.create_message("sam.audino@nycdatascience.com", "Sharing Uploaded File Test",
                             "Here is the download link: " + file_link)

myGmail.send_message(msg)



