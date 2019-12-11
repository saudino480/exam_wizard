from Gmail import Gmail

myGmail = Gmail("charles.cohen@nycdatascience.com")

msg = myGmail.create_attached_message("nycdsa.student@gmail.com", "Zip File Attached",
                                      "This message contains a zip file\n\nDo not respond.",
                                      ".", "Charlie.zip")
myGmail.send_message(msg)