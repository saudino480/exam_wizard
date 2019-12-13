from google_apps import GMail

myGmail = GMail("charles.cohen@nycdatascience.com")

msg = myGmail.create_attached_message("nycdsa.student@gmail.com", "Text File Test",
                                      "This message contains a text file attachment.\n\nDo not respond.",
                                      ".", "TODO_2.txt")
myGmail.send_message(msg)