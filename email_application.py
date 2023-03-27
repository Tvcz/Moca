import tkinter
import tkinter.messagebox
import smtplib
class GUI:
    def email_login(self):
        self.login = tkinter.Toplevel()
        self.login.title("Login to Gmail")
        login_menu = tkinter.PanedWindow(self.login)
        login_menu.pack(fill="both", expand=True)
        
        email_field = tkinter.PanedWindow(login_menu, orient="vertical")
        email_field.pack(fill="both", expand=True)
        login_menu.add(email_field)

        email_field.add(tkinter.Label(email_field, text="Email:"))
        email_entry = tkinter.Entry(email_field, width=40)
        email_field.add(email_entry)

        password_field = tkinter.PanedWindow(login_menu, orient="vertical")
        password_field.pack(fill="both", expand=True)
        login_menu.add(password_field)

        password_field.add(tkinter.Label(password_field, text="Password:"))
        password_entry = tkinter.Entry(password_field, width=30)
        password_field.add(password_entry)

        button = tkinter.Button(login_menu, width=20, text="Sign In", command=lambda: self.verify_email(email_entry, password_entry))
        login_menu.add(button)

    def verify_email(self, email_entry, password_entry):
        self.email = email_entry.get()
        self.password = password_entry.get()
        self.mail = smtplib.SMTP('smtp.gmail.com', 587)
        self.mail.starttls()
        try:
            self.mail.login(self.email, self.password)
            self.login.destroy()
            del self.password
        except smtplib.SMTPAuthenticationError:
            tkinter.messagebox.showerror("Incorrect Email or Password!", 'This might also be due to "Less secure app access" being disabled. Visit "https://myaccount.google.com/security" to disable this feature.')

    def main_menu(self):
        menu = tkinter.PanedWindow(orient="vertical")
        menu.pack(fill="both", expand=True)

        receiver_row = tkinter.PanedWindow()
        receiver_row.pack(fill="both", expand=True)
        menu.add(receiver_row)

        receiver_row.add(tkinter.Label(receiver_row, text="To:"))
        self.receiver_entry = tkinter.Entry(receiver_row, width=50)
        receiver_row.add(self.receiver_entry)

        sender_row = tkinter.PanedWindow()
        sender_row.pack(fill="both", expand=True)
        menu.add(sender_row)

        sender_row.add(tkinter.Label(sender_row, text="From:"))
        self.sender_entry = tkinter.Entry(sender_row, width=30)
        sender_row.add(self.sender_entry)

        individual_receiver_row = tkinter.PanedWindow()
        individual_receiver_row.pack(fill="both", expand=True)
        menu.add(individual_receiver_row)

        individual_receiver_row.add(tkinter.Label(individual_receiver_row, text="Individualized recipients:"))
        self.individual_receiver_entry = tkinter.Entry(individual_receiver_row, width=30)
        individual_receiver_row.add(self.individual_receiver_entry)

        individual_receiver_names_row = tkinter.PanedWindow()
        individual_receiver_names_row.pack(fill="both", expand=True)
        menu.add(individual_receiver_names_row)

        individual_receiver_names_row.add(tkinter.Label(individual_receiver_names_row, text="Individualized recipient names:"))
        self.individual_receiver_names_entry = tkinter.Entry(individual_receiver_names_row, width=30)
        individual_receiver_names_row.add(self.individual_receiver_names_entry)

        options_row = tkinter.PanedWindow()
        options_row.pack(fill="both", expand=True)
        menu.add(options_row)

        options_row.add(tkinter.Label(options_row, text="Number of emails to send:"))
        self.repetitions_entry = tkinter.Entry(options_row, width=5)
        options_row.add(self.repetitions_entry)

        self.html_enabled = tkinter.IntVar(options_row, 0)
        options_row.add(tkinter.Checkbutton(options_row, text="Enable html embedding?", variable=self.html_enabled))

        subject_row = tkinter.PanedWindow()
        subject_row.pack(fill="both", expand=True)
        menu.add(subject_row)

        subject_row.add(tkinter.Label(subject_row, text="Subject:"))
        self.subject_entry = tkinter.Entry(subject_row, width=50)
        subject_row.add(self.subject_entry)

        menu.add(tkinter.Label(menu, text="Body:", anchor="w"))

        self.body_entry = tkinter.Text(menu, width=70, height=10)
        menu.add(self.body_entry)

        send_button = tkinter.Button(menu, width=20, text="Send", command=self.send_email)
        menu.add(send_button)

    def send_email(self):
        if str(self.repetitions_entry) != ".!panedwindow6.!entry" and str(self.repetitions_entry) != "":
            repetitions = int(self.repetitions_entry.get())
        else:
            repetitions = 1
        for iteration in range(repetitions):
            if iteration != 0:
                email_count = " #" + str(iteration + 1)
            else:
                email_count = ""
            try:	
                email_container = ""
                email_container += "From: " + str(self.sender_entry.get()) + "\n"
                
                if str(self.individual_receiver_entry.get()) == "":
                    receiver = str(self.receiver_entry.get())
                    email_container += "To: " + receiver + "\n"
                    if self.html_enabled:
                        email_container += "MIME-Version: 1.0\nContent-type: text/html\n"
                    email_container += "Subject: " + str(self.subject_entry.get()) + email_count + "\n"
                    email_container += str(self.body_entry.get("1.0","end-1c"))
                    if ", " in receiver:
                        receiver = receiver.split(", ")
                    self.mail.sendmail(self.email, receiver, email_container)
                
                else:
                    receiver_emails = str(self.individual_receiver_entry.get()).split(", ")
                    receiver_names = str(self.individual_receiver_names_entry.get()).split(", ")

                    for index in range(len(receiver_emails)):
                        email_container += "To: " + receiver_names[index] + " <" + receiver_emails[index]+ ">\n"
                        if self.html_enabled:
                            email_container += "MIME-Version: 1.0\nContent-type: text/html\n"
                        email_container += "Subject: " + str(self.subject_entry.get()) + email_count + "\n"
                        email_container += str(self.body_entry.get("1.0","end-1c"))
                        email_container = email_container.format(name=receiver_names[index])
                        self.mail.sendmail(self.email, receiver_emails[index], email_container)

            except smtplib.SMTPSenderRefused:
                sleep(300)
        tkinter.messagebox.showinfo("Success!", "Email(s) sent!")


app = tkinter.Tk()
gui = GUI()
app.title("MOCA Email Client")

gui.email_login()
gui.main_menu()

app.mainloop()
