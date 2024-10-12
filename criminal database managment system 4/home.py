import shutil
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from dbHandler import *
from facerec import *
from register import *
from facerec import detect_faces, recognize_face
import tkinter as tk
from tkinter import ttk
import mysql.connector

active_page = 0
thread_event = None
left_frame = None
right_frame = None
heading = None
webcam = None
img_label = None
img_read = None
img_list = []
slide_caption = None
slide_control_panel = None
current_slide = -1


import tkinter as tk
from tkinter import messagebox
import pymysql

import subprocess


def login(username, password):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="mysql369963",
            database="CRIMINALDB"
        )
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username)
            # Destroy the login window
            root.destroy()
            # Call the function to execute home.py
            execute_home_py()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except pymysql.Error as err:
        messagebox.showerror("Error", "Database connection error: {}".format(err))

def execute_home_py():
    # Put the code to execute home.py here
    pass  # Placeholder, replace with actual code to execute home.py


# Add the function to execute home.py
 # Replace "python" with the appropriate command to execute Python scripts on your system

def open_warning_page(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")

    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def open_warning_page(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")

    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def open_warning_page(message):
    warning_window = tk.Toplevel()
    warning_window.title("Warning")

    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def register_user():
    def register():
        name = name_entry.get()
        dob = dob_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        admin_code = admin_code_entry.get()  # Get the admin code

        # Validate admin code
        if not admin_code:
            open_warning_page("Please enter the admin code or user credentials!.")
            return

        # Validate the admin code value
        if admin_code != "admin123":  # Change "admin123" to your desired admin code
            open_warning_page("Invalid Admin Code")
            return

        # Check if any field is empty
        if not all([name, dob, email, username, password]):
            open_warning_page("Please fill in all fields.")
            return

        # Connect to MySQL database
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="mysql369963",
                database="CRIMINALDB"
            )
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                open_warning_page("Username already exists. Please choose a different username.")
                return

            # Insert new user into the database
            query = "INSERT INTO users (name, dob, email, username, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, dob, email, username, password))
            conn.commit()
            messagebox.showinfo("Registration Successful", "You have been successfully registered!")

        except pymysql.Error as err:
            messagebox.showerror("Error", "Database connection error: {}".format(err))

    # Create registration window
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    # Create labels and entry widgets for registration
    name_label = tk.Label(registration_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(registration_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    dob_label = tk.Label(registration_window, text="Date of Birth:")
    dob_label.grid(row=1, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(registration_window)
    dob_entry.grid(row=1, column=1, padx=10, pady=5)

    email_label = tk.Label(registration_window, text="Email:")
    email_label.grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(registration_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    username_label = tk.Label(registration_window, text="Username:")
    username_label.grid(row=3, column=0, padx=10, pady=5)
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=3, column=1, padx=10, pady=5)

    password_label = tk.Label(registration_window, text="Password:")
    password_label.grid(row=4, column=0, padx=10, pady=5)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    admin_code_label = tk.Label(registration_window, text="Admin Code:")
    admin_code_label.grid(row=5, column=0, padx=10, pady=5)
    admin_code_entry = tk.Entry(registration_window, show="*")
    admin_code_entry.grid(row=5, column=1, padx=10, pady=5)

    # Create register button
    register_button = tk.Button(registration_window, text="Register", command=register)
    register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

# Main window (login window)
root = tk.Tk()
root.geometry("1500x900+200+100")
root.title("Login")

# Calculate the center coordinates of the window
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)

# Set the window to be centered on the screen
root.geometry("+{}+{}".format(position_right, position_down))

# Create a frame for the login section
login_frame = tk.Frame(root, bd=3,bg="#F5F4F4", relief=tk.RAISED, width=420, height=220)  # Adjust width and height as needed
login_frame.place(relx=0.5, rely=0.4, anchor="center")

# Create login labels and entry widgets inside the login frame
username_label = tk.Label(login_frame, text="Username:")
username_label.place(relx=0.3, rely=0.3, anchor="center")
username_entry = tk.Entry(login_frame)
username_entry.place(relx=0.62, rely=0.3, anchor="center")

password_label = tk.Label(login_frame, text="Password  :")
password_label.place(relx=0.3, rely=0.45, anchor="center")
password_entry = tk.Entry(login_frame, show="*")
password_entry.place(relx=0.62, rely=0.45, anchor="center")

# Create login button inside the login frame
login_button = tk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()),
                         padx=10, pady=5, bg="blue", fg="#00C1FF", width=20)  # Adjust the width as needed
login_button.place(relx=0.5, rely=0.65, anchor="center")

# Create registration button inside the login frame
register_button = tk.Button(login_frame, text="Register", command=register_user, padx=10, pady=5, bg="green", fg="#00DF39", width=20)  # Adjust the width as needed
register_button.place(relx=0.5, rely=0.85, anchor="center")

# Configure login frame properties
login_frame.configure(bg="white")
root.mainloop()


root = tk.Tk()
root.geometry("1500x900+200+100")
# create Pages
pages = []
for i in range(6):  # Change range to range(6) to create 6 pages
    pages.append(tk.Frame(root, bg="#000080"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)


def basicPageSetup(pageNo):
    global left_frame, right_frame, heading

    # Create the heading label
    heading = tk.Label(pages[pageNo], fg="white", bg="#000080", font="Arial 20 bold", pady=17)
    heading.pack()
    print("Heading label created and packed successfully")

    # Load the back button image only if not on page 4 or 5
    if pageNo != 4 and pageNo != 5:  # Adjust condition to exclude page 4 and 5
        back_img = tk.PhotoImage(file="back.png")

        # Create the back button
        back_button = tk.Button(pages[pageNo], image=back_img, bg="#710083", bd=1, highlightthickness=0,
                                activebackground="white", command=goBack)
        back_button.image = back_img

        # Place the back button
        back_button.place(x=10, y=0.1)
        print("Back button created and placed successfully")

    # Create a frame for the content
    content = tk.Frame(pages[pageNo], bg="#000080")
    content.pack(expand="true", fill="both")
    print("Content frame created and packed successfully")

    # Create the left frame
    left_frame = tk.Frame(content, bg="#000080")
    left_frame.grid(row=0, column=0, sticky="nsew")
    print("Left frame created and gridded successfully")

    # For pages other than page 4 or 5, create the right frame
    if pageNo != 4 and pageNo != 5:  # Adjust condition to exclude page 4 and 5
        right_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#710083", font="Arial 20 bold", bd=4,foreground="white", labelanchor="n")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        print("Right frame created and gridded successfully")

        # Configure grid weights
        content.grid_columnconfigure(0, weight=1, uniform="group1")
        content.grid_columnconfigure(1, weight=1, uniform="group1")
        content.grid_rowconfigure(0, weight=1)


def showImage(frame, img_size):
    global img_label, left_frame

    img = cv2.resize(frame, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    if (img_label == None):
        img_label = tk.Label(left_frame, image=img, bg="white")
        img_label.image = img
        img_label.pack(padx=20)
    else:
        img_label.configure(image=img)
        img_label.image = img


def getNewSlide(control):
    global img_list, current_slide

    if len(img_list) > 1:
        if control == "prev":
            current_slide = (current_slide - 1) % len(img_list)
        else:
            current_slide = (current_slide + 1) % len(img_list)

        img_size = left_frame.winfo_height() - 200
        showImage(img_list[current_slide], img_size)

        slide_caption.configure(text="Image {} of {}".format(current_slide + 1, len(img_list)))


def selectMultiImage(opt_menu, menu_var):
    global img_list, current_slide, slide_caption, slide_control_panel

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path_list = filedialog.askopenfilenames(title="Choose least 5 images", filetypes=filetype)

    if len(path_list) < 5:
        messagebox.showerror("Error", "Choose least 5 images.")
    else:
        img_list = []
        current_slide = -1

        # Resetting slide control panel
        if slide_control_panel is not None:
            slide_control_panel.destroy()

        # Creating Image list
        for path in path_list:
            img_list.append(cv2.imread(path))

        # Creating choices for profile pic menu
        menu_var.set("")
        opt_menu['menu'].delete(0, 'end')

        for i in range(len(img_list)):
            ch = "Image " + str(i + 1)
            opt_menu['menu'].add_command(label=ch, command=tk._setit(menu_var, ch))
            menu_var.set("Image 1")

        # Creating slideshow of images
        img_size = left_frame.winfo_height() - 200
        current_slide += 1
        showImage(img_list[current_slide], img_size)

        slide_control_panel = tk.Frame(left_frame, bg="#000080", pady=10)
        slide_control_panel.pack()

        back_img = tk.PhotoImage(file="previous.png")
        next_img = tk.PhotoImage(file="next.png")

        prev_slide = tk.Button(slide_control_panel, image=back_img, bg="#710083", bd=2, highlightthickness=0,
                               activebackground="white", command=lambda: getNewSlide("prev"))
        prev_slide.image = back_img
        prev_slide.grid(row=0, column=0, padx=60)

        slide_caption = tk.Label(slide_control_panel, text="Image 1 of {}".format(len(img_list)), fg="white",
                                 bg="#710083", font="Arial 20 bold")
        slide_caption.grid(row=0, column=1)

        next_slide = tk.Button(slide_control_panel, image=next_img, bg="#710083", bd=2, highlightthickness=0,
                               activebackground="white", command=lambda: getNewSlide("next"))
        next_slide.image = next_img
        next_slide.grid(row=0, column=2, padx=60)



def insert_into_database(data):
    try:
        # Call the insert_data function to insert data into the database
        row_id = insert_data(data)
        if row_id is not None and row_id > 0:
            print("Data inserted successfully. Row ID:", row_id)
            return row_id
        else:
            print("Failed to insert data into the database.")
            return None
    except Exception as e:
        print("Error inserting data:", e)
        return None


def register(entries, required, menu_var):
    global img_list

    # Checking if no image selected
    if len(img_list) == 0:
        messagebox.showerror("Error", "Select Images first.")
        return

    # Fetching data from entries
    entry_data = {}
    for i, entry in enumerate(entries):
        val = entry[1].get()

        if len(val) == 0 and required[i] == 1:
            messagebox.showerror("Field Error", "Required field missing :\n\n%s" % (entry[0]))
            return
        else:
            entry_data[entry[0]] = val.lower()

    # Setting Directory
    path = os.path.join('face_samples', "temp_criminal")
    if not os.path.isdir(path):
        os.mkdir(path)

    no_face = []
    for i, img in enumerate(img_list):
        # Storing Images in directory
        id = registerCriminal(img, path, i + 1)
        if (id != None):
            no_face.append(id)

    # check if any image doesn't contain face
    if len(no_face) > 0:
        no_face_st = ""
        for i in no_face:
            no_face_st += "Image " + str(i) + ", "
        messagebox.showerror("Registration Error", "Registration failed!\n\nFollowing images doesn't contain","face or Face is too small:\n\n%s" % (no_face_st))
        shutil.rmtree(path, ignore_errors=True)
    else:
        # Storing data in database
        rowId = insert_into_database(entry_data)

        if rowId is not None:  # Check if rowId is not None
            if rowId > 0:
                messagebox.showinfo("Success", "Criminal Registered Successfully.")
                shutil.move(path, os.path.join('face_samples', entry_data["Name"]))

                # save profile pic
                profile_img_num = int(menu_var.get().split(' ')[1]) - 1
                if not os.path.isdir("profile_pics"):
                    os.mkdir("profile_pics")
                cv2.imwrite("profile_pics/criminal %d.png" % rowId, img_list[profile_img_num])

                goBack()
            else:
                shutil.rmtree(path, ignore_errors=True)
                messagebox.showerror("Database Error", "Some error occurred while storing data.")
        else:
            messagebox.showerror("Database Error", "Failed to insert data into the database.")


## update scrollregion when all widgets are in canvas
def on_configure(event, canvas, win):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.itemconfig(win, width=event.width)

import tkinter as tk
## Register Page ##
def getPage1():
    global active_page, left_frame, right_frame, heading, img_label, pages  # Add 'pages' to the global variables

    active_page = 1
    img_label = None
    opt_menu = None
    menu_var = tk.StringVar(root)
    pages[1].lift()

    basicPageSetup(1)
    heading.configure(text="REGISTER CRIMINAL")
    right_frame.configure(text="ENTER DETAILS")

    btn_grid = tk.Frame(left_frame, bg="white")
    btn_grid.pack()

    tk.Button(btn_grid, text="Select Images", command=lambda: selectMultiImage(opt_menu, menu_var),
              font="Arial 17 bold", bg="#710083", fg="white", pady=10, bd=5, highlightthickness=0,
              activebackground="#091428", activeforeground="white").grid(row=0, column=0, padx=3, pady=3)

    # Creating Scrollable Frame
    canvas = tk.Canvas(right_frame, bg="#710083", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand="true", padx=30)
    scrollbar = tk.Scrollbar(right_frame, command=canvas.yview, width=20, troughcolor="white", bd=2,
                             activebackground="#FF0000", bg="black", relief="raised")
    scrollbar.pack(side="left", fill="y")

    scroll_frame = tk.Frame(canvas, bg="#710083", pady=20)
    scroll_win = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event, win=scroll_win: on_configure(event, canvas, win))

    tk.Label(scroll_frame, text="* Required Fields", bg="#000080", fg="yellow", font="Arial 14 bold").pack()
    # Adding Input Fields
    input_fields = (
        "Name", "Father's Name", "Mother's Name", "Gender", "DOB(yyyy-mm-dd)", "Blood Group", "Identification Mark",
        "Nationality", "Religion", "Crimes Done", "Profile Image")
    ip_len = len(input_fields)
    required = [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]

    entries = []
    for i, field in enumerate(input_fields):
        row = tk.Frame(scroll_frame, bg="#710083")
        row.pack(side="top", fill="x", pady=15)

        label = tk.Text(row, width=18, height=1, bg="#710083", fg="white", font="Arial 15", highlightthickness=1, bd=0.5)
        label.insert("insert", field)
        label.pack(side="left")

        if (required[i] == 1):
            label.tag_configure("star", foreground="yellow", font="Arial 15 bold")
            label.insert("end", "  *", "star")
        label.configure(state="disabled")

        if (i != ip_len - 1):
            ent = tk.Entry(row, font="Arial 15", selectbackground="#710083")
            ent.pack(side="right", expand="true", fill="x", padx=10)
            entries.append((field, ent))
        else:
            menu_var.set("Image 1")
            choices = ["Image 1"]
            opt_menu = tk.OptionMenu(row, menu_var, *choices)
            opt_menu.pack(side="right", fill="x", expand="true", padx=10)
            opt_menu.configure(font="Arial 14", bg="#52009B", fg="white", bd=2, highlightthickness=0,
                               activebackground="blue")
            menu = opt_menu.nametowidget(opt_menu.menuname)
            menu.configure(font="Arial 14", bg="white", activebackground="red", bd=1)

    # Create a button with command that uses scroll_frame
    tk.Button(scroll_frame, text="Register", command=lambda: register(entries, required, menu_var),
              font="Arial 15 bold", bg="#52009B", fg="white", pady=10, padx=30, bd=2, highlightthickness=0.5,
              activebackground="red", activeforeground="white").pack(pady=25)


import pymysql


def retrieveData(name):
    # Connect to the database
    db = pymysql.connect(host='localhost', user='root', password='mysql369963', database='CRIMINALDB')

    # Prepare a cursor object
    cursor = db.cursor()

    try:
        # Execute the SQL query
        cursor.execute("SELECT * FROM criminaldata WHERE Name = %s", (name,))

        # Fetch the result
        row = cursor.fetchone()

        if row:
            # Extract the ID and criminal data
            id = row[0]
            crim_data = {
                "Name": row[1],
                "Father's Name": row[2],
                "Mother's Name": row[3],
                "Gender": row[4],
                "DOB": row[5],
                "Blood Group": row[6],
                "Identification Mark": row[7],
                "Nationality": row[8],
                "Religion": row[9],
                "Crimes Done": row[10]
            }
            return (id, crim_data)
        else:
            return (None, None)
    except Exception as e:
        print("Error retrieving data:", e)
        return (None, None)
    finally:
        # Close the database connection
        cursor.close()
        db.close()


def showCriminalProfile(name):
    top = tk.Toplevel(bg="#202d42")
    top.title("Criminal Profile")
    top.geometry("1500x900+%d+%d" % (root.winfo_x() + 10, root.winfo_y() + 10))

    tk.Label(top, text="Criminal Profile", fg="white", bg="#202d42", font="Arial 20 bold", pady=10).pack()
    content = tk.Frame(top, bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")
    content.grid_columnconfigure(0, weight=3, uniform="group1")
    content.grid_columnconfigure(1, weight=5, uniform="group1")
    content.grid_rowconfigure(0, weight=1)

    (id, crim_data) = retrieveData(name)

    if id is not None:
        path = os.path.join("profile_pics", "criminal %d.png" % id)
        profile_img = cv2.imread(path)

        profile_img = cv2.resize(profile_img, (500, 500))
        img = cv2.cvtColor(profile_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(content, image=img, bg="#202d42")
        img_label.image = img
        img_label.grid(row=0, column=0)

        info_frame = tk.Frame(content, bg="#202d42")
        info_frame.grid(row=0, column=1, sticky='w')

        for i, item in enumerate(crim_data.items()):
            tk.Label(info_frame, text=item[0], pady=15, fg="yellow", font="Arial 15 bold", bg="#202d42").grid(row=i,
                                                                                                              column=0,
                                                                                                              sticky='w')
            tk.Label(info_frame, text=":", fg="yellow", padx=50, font="Arial 15 bold", bg="#202d42").grid(row=i,
                                                                                                          column=1)
            val = "---" if (item[1] == "") else item[1]
            tk.Label(info_frame, text=val.capitalize(), fg="white", font="Arial 15", bg="#202d42").grid(row=i, column=2,
                                                                                                        sticky='w')
    else:
        tk.Label(content, text="Criminal ID not found!", fg="red", font="Arial 15 bold", bg="#202d42").pack()


def startRecognition():
    global img_read, img_label

    if (img_label == None):
        messagebox.showerror("Error", "No image selected. ")
        return

    crims_found_labels = []
    for wid in right_frame.winfo_children():
        wid.destroy()

    frame = cv2.flip(img_read, 1, 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_coords = detect_faces(gray_frame)

    if (len(face_coords) == 0):
        messagebox.showerror("Error", "Image doesn't contain any face or face is too small.")
    else:
        (model, names) = train_model()
        print('Training Successful. Detecting Faces')
        (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

        img_size = left_frame.winfo_height() - 40
        frame = cv2.flip(frame, 1, 0)
        showImage(frame, img_size)

        if (len(recognized) == 0):
            messagebox.showerror("Error", "No criminal recognized.")
            return

        for i, crim in enumerate(recognized):
            crims_found_labels.append(tk.Label(right_frame, text=crim[0], bg="orange",font="Arial 15 bold", pady=20))
            crims_found_labels[i].pack(fill="x", padx=20, pady=10)
            crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]: showCriminalProfile(name))


def selectImage():
    global left_frame, img_label, img_read
    for wid in right_frame.winfo_children():
        wid.destroy()

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if (len(path) > 0):
        img_read = cv2.imread(path)

        img_size = left_frame.winfo_height() - 40
        showImage(img_read, img_size)

## Detection Page ##
def getPage2():
    global active_page, left_frame, right_frame, img_label, heading
    img_label = None
    active_page = 2
    pages[2].lift()

    basicPageSetup(2)
    heading.configure(text="DETECT CRIMINAL")
    right_frame.configure(text="DETECTED CRIMINALS")

    btn_grid = tk.Frame(left_frame, bg="#000080")
    btn_grid.pack()

    tk.Button(btn_grid, text="Select Image", command=selectImage, font="Arial 15 bold", padx=20, bg="#710083",
              fg="white", pady=10, bd=3, highlightthickness=0.5, activebackground="#2E00FF",
              activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    tk.Button(btn_grid, text="Recognize", command=startRecognition, font="Arial 15 bold", padx=20, bg="#710083",
              fg="white", pady=10, bd=3, highlightthickness=0.5, activebackground="#2E00FF",
              activeforeground="white").grid(row=0, column=1, padx=25, pady=25)


## Import the functions from dbHandler
from dbHandler import fetchAllData, updateData, deleteData
from tkinter import messagebox  # Importing messagebox from tkinter


def deleteRecord(id):
    """
    Delete the criminal record with the specified ID.
    Args:
        id (int): The ID of the criminal record to delete.
    """
    # Call the deleteData function from dbHandler
    if deleteData(id):
        messagebox.showinfo("Success", "Criminal record deleted successfully.")
    else:
        messagebox.showerror("Error", "Failed to delete criminal record.")


def videoLoop(model, names):
    global thread_event, left_frame, webcam, img_label
    webcam = cv2.VideoCapture(0)
    old_recognized = []
    crims_found_labels = []
    img_label = None

    try:
        while not thread_event.is_set() and webcam.isOpened():
            # Loop until the camera is working
            while True:
                # Put the image from the webcam into 'frame'
                return_val, frame = webcam.read()
                if return_val:
                    break
                else:
                    print("Failed to open webcam. Trying again...")

            # Flip the image (optional)
            frame = cv2.flip(frame, 1, 0)
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect Faces
            face_coords = detect_faces(gray_frame)
            (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

            # Recognize Faces
            recog_names = [item[0] for item in recognized]
            if recog_names != old_recognized:
                for wid in right_frame.winfo_children():
                    wid.destroy()
                crims_found_labels.clear()

                for i, crim in enumerate(recognized):
                    crims_found_labels.append(
                        tk.Label(right_frame, text=crim[0], bg="orange", font="Arial 15 bold", pady=20))
                    crims_found_labels[i].pack(fill="x", padx=20, pady=10)
                    crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]: showCriminalProfile(name))

                old_recognized = recog_names

            # Display Video stream
            img_size = min(left_frame.winfo_width(), left_frame.winfo_height()) - 20
            showImage(frame, img_size)

    except RuntimeError as e:
        print("[INFO] Caught Runtime Error:", e)
    except tk.TclError as e:
        print("[INFO] Caught Tcl Error:", e)
    finally:
        # Release webcam resources
        webcam.release()


## video surveillance Page ##
# Function to initialize the video surveillance page
def getPage3():
    global active_page, thread_event, webcam
    active_page = 3
    pages[3].lift()

    basicPageSetup(3)
    heading.configure(text="Video Surveillance")
    right_frame.configure(text="Detected Criminals")
    left_frame.configure(pady=40)

    # Train the model for face recognition
    (model, names) = train_model()
    print('Training Successful. Detecting Faces')

    # Start video surveillance in a separate thread
    thread_event = threading.Event()
    thread = threading.Thread(target=videoLoop, args=(model, names))
    thread.start()


# Function to handle "go back" action
def goBack():
    global active_page, thread_event, webcam

    # Check if the active page is the video surveillance page and if video surveillance is running
    if active_page == 3 and thread_event.is_set():
        # Stop video surveillance
        thread_event.clear()  # Clear the event to stop video surveillance
        webcam.release()  # Release the webcam resources

    # Destroy widgets associated with the current page
    for widget in pages[active_page].winfo_children():
        widget.destroy()

    # Lift the main page to show after clearing widgets
    pages[0].lift()
    active_page = 0

## Manage Criminal Page ##
# You can use fetchAllData, updateData, and deleteData functions here as needed.

def updateRecord(id, entries):
    """
    Update the criminal record with the specified ID using the data from the input entries.
    Args:
        id (int): The ID of the criminal record to update.
        entries (dict): A dictionary containing the updated data.
    """
    # Call the updateData function from dbHandler
    if updateData(id, entries):
        messagebox.showinfo("Success", "Criminal record updated successfully.")
    else:
        messagebox.showerror("Error", "Failed to update criminal record.")



def on_record_select(record_id):
    global selected_id
    selected_id = record_id


def goBack():
    global active_page

    # Clear widgets from the current active page
    for widget in pages[active_page].winfo_children():
        widget.destroy()

    # Lift the main page to show after clearing widgets
    pages[0].lift()
    active_page = 0


selected_id = None

# Function to update the criminal information display with the selected record
from tkinter import messagebox
from dbHandler import connect_to_database, fetch_all_criminal_data, updateData, deleteData

selected_id = ""  # Global variable to store the selected record ID

def updateRecord(id, entries):
    """
    Update the criminal record with the specified ID using the data from the input entries.
    Args:
        id (int): The ID of the criminal record to update.
        entries (dict): A dictionary containing the updated data.
    """
    # Call the updateData function from dbHandler
    if updateData(id, entries):
        messagebox.showinfo("Success", "Criminal record updated successfully.")
    else:
        messagebox.showerror("Error", "Failed to update criminal record.")

def deleteRecord():
    """
    Delete the criminal record with the selected ID.
    """
    global selected_id
    if not selected_id:
        messagebox.showerror("Error", "Please select a record to delete.")
        return

    try:
        # Convert selected_id to integer
        id_to_delete = int(selected_id)
        deleteData(id_to_delete)
        getPage4()  # Refresh the page after deleting the record
    except ValueError:
        messagebox.showerror("Error", "Invalid record ID.")


def updateRecord(id, entries):
    """
    Update the criminal record with the specified ID using the data from the input entries.
    Args:
        id (int): The ID of the criminal record to update.
        entries (dict): A dictionary containing the updated data.
    """
    # Call the updateData function from dbHandler
    if updateData(id, entries):
        messagebox.showinfo("Success", "Criminal record updated successfully.")
    else:
        messagebox.showerror("Error", "Failed to update criminal record.")
    if record_id:
        # Fetch the record details based on the record_id
        record = fetch_criminal_record(record_id)
        if record:
            # Update the display fields with the record details
            name_entry.delete(0, tk.END)  # Clear existing content
            name_entry.insert(tk.END, record["Name"])

            father_name_entry.delete(0, tk.END)
            father_name_entry.insert(tk.END, record["Father's Name"])

            mother_name_entry.delete(0, tk.END)
            mother_name_entry.insert(tk.END, record["Mother's Name"])

            gender_entry.delete(0, tk.END)
            gender_entry.insert(tk.END, record["Gender"])

            dob_entry.delete(0, tk.END)
            dob_entry.insert(tk.END, record["DOB"])

            blood_group_entry.delete(0, tk.END)
            blood_group_entry.insert(tk.END, record["Blood Group"])

            identification_mark_entry.delete(0, tk.END)
            identification_mark_entry.insert(tk.END, record["Identification Mark"])

            nationality_entry.delete(0, tk.END)
            nationality_entry.insert(tk.END, record["Nationality"])

            religion_entry.delete(0, tk.END)
            religion_entry.insert(tk.END, record["Religion"])

            crimes_done_entry.delete(0, tk.END)
            crimes_done_entry.insert(tk.END, record["Crimes Done"])
        else:
            messagebox.showerror("Error", "Failed to fetch record details.")
    else:
        messagebox.showerror("Error", "No record selected.")

# Define getPage4 function for page 4
def getPage4():
    global active_page, selected_id, left_frame, heading

    selected_id = ""  # Initialize selected_id

    active_page = 4
    if len(pages) >= 5:
        pages[4].lift()
        # Basic setup for the page (ensure pages[4] is valid)
        basicPageSetup(4)  # Use the correct page index
        left_frame.configure(pady=100)
    else:
        print("Error: getPage4 - Index out of range")
        return

    # Create a frame for the content
    content = tk.Frame(pages[4], bg="#710083")
    content.pack(side="left", padx=20, pady=5, fill="both", expand=True)
    content.lift()

    # Add your code for managing criminals here
    # Create a frame for the form on the left side
    form_frame = tk.Frame(content, bd=5, bg="#710083")
    form_frame.pack(side="left", padx=60, pady=10, fill="both", expand=True)

    # Create a frame for the record list with scrollbar on the right side
    record_frame_left = tk.Frame(content, bg="#710083")  # Change variable name to avoid conflict
    record_frame_left.pack(side="right", padx=10, pady=20, fill="both", expand=True)

    # Create a label for the form title
    form_title_label = tk.Label(form_frame, text="CRIMINAL INFORMATION", bg="#710083", fg="white", font=("Arial", 14))
    form_title_label.pack(pady=(0.00011, 0.00011))  # Adjusted pady

    # Define ID label
    ID = "ID"

    # Add form fields with labels for each field
    form_fields = [ID, "Name", "Father's Name", "Mother's Name", "Gender", "DOB", "Blood Group", "Identification Mark",
                   "Nationality", "Religion", "Crimes_done"]
    form_entries = {}

    # Pack form fields within the form_frame
    for label in form_fields:
        # Create a Label for the form field
        tk.Label(form_frame, text=label, bg="#710083", fg="white", font=("Arial", 11)).pack(padx=(0.50, 0.50), pady=(0.50,0.50), anchor="w")

        # Create the Entry widget
        entry = tk.Entry(form_frame, font=("Arial", 13), width=30)
        entry.pack(padx=(0.18,0.18), pady=(0.18,0.18), fill="x")

        # Store the Entry widget in the form_entries dictionary
        form_entries[label] = entry

    # Create a frame for the buttons
    button_frame = tk.Frame(form_frame, bg="#710083")
    button_frame.pack(side="bottom", pady=8)

    # Add buttons for update and delete operations
    # Create the Update button
    update_button = tk.Button(button_frame, text="Update", bg="#23FF00", activebackground="#1AB202", command=lambda: updateRecord(selected_id, {field: entry.get() for field, entry in form_entries.items()}))
    update_button.grid(row=0, column=1, padx=15)

    # Create the Delete button
    delete_button = tk.Button(button_frame, text="Delete", bg="#FF0000", activebackground="#B20202",
                              command=deleteRecord)
    delete_button.grid(row=0, column=0, padx=15)

    # Create the Go Back button
    back_button = tk.Button(button_frame, text="Back", bg="#E0FF00", activebackground="#BDD700", command=goBack)
    back_button.grid(row=0, column=2, padx=15)

    # Fetch all criminal records from the database
    criminal_records = fetch_all_criminal_data()

    if criminal_records:
        # Create a scrollbar for the record list
        scrollbar = tk.Scrollbar(record_frame_left)
        scrollbar.pack(side="right", fill="y")

        # Calculate the number of records to determine the height of the listbox
        num_records = len(criminal_records)
        listbox_height = min(num_records, 13)  # Limit the height to a maximum of 13 records

        # Create a listbox to display the records with limited height
        record_listbox = tk.Listbox(record_frame_left, yscrollcommand=scrollbar.set, font=("Arial", 11), bg="white", height=listbox_height, width=70)  # Adjust font size and width
        record_listbox.pack(side="left", fill="both", expand=True)

        # Configure the scrollbar
        scrollbar.config(command=record_listbox.yview)

        # Populate the listbox with record information
        for record in criminal_records:
            # Inside getPage4() function, when populating record_info
            record_info = f"ID: {record['id']} | Name: {record['name']} | Father's Name: {record['father_name']} | Mother's Name: {record['mother_name']} | Gender: {record['gender']} | DOB(yyyy-mm-dd): {record['dob']} | Blood Group: {record['blood_group']} | Identification Mark: {record.get('identification_mark', '---')} | Nationality: {record['nationality']} | Religion: {record['religion']} | Crimes Done: {record['Crimes Done']}"

            record_listbox.insert(tk.END, record_info)
    else:
        # If no criminal records found, display a message above the record_listbox
        no_records_label = tk.Label(record_frame_left, text="No criminal records found.", bg="white", fg="black", font=("Arial", 14), width=40)
        no_records_label.pack(fill="both", expand=True)




# Import the necessary modules
import mysql.connector
import tkinter as tk
from tkinter import ttk
 # Assuming you are using MySQL


def getPage5():
    global active_page, left_frame

    active_page = 5
    if len(pages) >= 6:
        pages[5].lift()
        basicPageSetup(5)
        left_frame.configure(pady=100)
    else:
        print("Error: getPage5 - Index out of range")
        return

    # Create a frame for the content
    content = tk.Frame(pages[5], bg="#710083")
    content.pack(side="top", padx=15, pady=15, fill="both", expand=True)
    content.lift()

    # Fetch officers' information from the database
    officers_info = fetchOfficersInfo()

    if officers_info:
        # Create a heading for officers' details
        officers_heading = tk.Label(content, text="Officers Details", fg="white", bg="#710083",
                                    font=("Arial", 20, "bold"))
        officers_heading.pack(side="top", pady=10)

        # Create a Treeview widget to display officers' information
        officers_tree = ttk.Treeview(content,columns=("Name", "Station", "Place", "DOB", "Post", "Criminals Caught", "Stars"),show="headings", height=20)
        officers_tree.pack(side="top", fill="both", expand=True)

        # Add headings for each column
        officers_tree.heading("Name", text="Name")
        officers_tree.heading("Station", text="Station")
        officers_tree.heading("Place", text="Place")
        officers_tree.heading("DOB", text="DOB")
        officers_tree.heading("Post", text="Post")
        officers_tree.heading("Criminals Caught", text="Criminals Caught")
        officers_tree.heading("Stars", text="Stars")

        # Add officers' information to the Treeview
        for officer in officers_info:
            officer_data = (officer['name'], officer['station'], officer['place'], officer['dob'], officer['post'], officer['criminals_caught'], officer['stars'])
            officers_tree.insert("", "end", values=officer_data)

        # Create a vertical scrollbar
        vsb = ttk.Scrollbar(content, orient="vertical", command=officers_tree.yview)
        vsb.pack(side="right", fill="y")

        # Create a horizontal scrollbar
        hsb = ttk.Scrollbar(content, orient="horizontal", command=officers_tree.xview)
        hsb.pack(side="bottom", fill="x")

        # Configure the Treeview to use the scrollbars
        officers_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Set the vertical scrollbar command to the yview method of the Treeview
        vsb.config(command=officers_tree.yview)
        # Set the horizontal scrollbar command to the xview method of the Treeview
        hsb.config(command=officers_tree.xview)

    else:
        # If no officers' information found, display a message
        no_officers_label = tk.Label(content, text="No officers' information found.", bg="white", fg="black",
                                     font=("Arial", 14), width=40)
        no_officers_label.pack(fill="both", expand=True)

    # Create a back button
    back_button = tk.Button(pages[5], text="Back to Home", command=goBack, bg="red", bd=5, fg="white",
                            font=("Arial", 14, "bold"))
    back_button.pack(side="bottom", padx=10, pady=20)
def fetchOfficersInfo():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="mysql369963", database="CRIMINALDB")
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM officers")
        officers_info = cursor.fetchall()
        conn.close()
        return officers_info
    except mysql.connector.Error as e:
        print(f"Error fetching officers' information: {e}")
        return None


######################################## Home Page ####################################
######################################## Home Page ####################################
# Label and image
tk.Label(pages[0], text="CRIMINAL IDENTIFICATION SYSTEM", fg="white", bg="#000080", font="Arial 35 bold", pady=10).pack()

hacker = tk.PhotoImage(file="hacker.png")
tk.Label(pages[0], image=hacker, bg="#000080").pack()

# Button frame
btn_frame = tk.Frame(pages[0], bg="", pady=10)
btn_frame.pack()

# First row of buttons
btn_register = tk.Button(btn_frame, text="Register Criminal", command=getPage1)
btn_register.grid(row=1, column=1, padx=5)
btn_detect = tk.Button(btn_frame, text="Detect Criminal", command=getPage2)
btn_detect.grid(row=0, column=1, padx=5)
btn_video = tk.Button(btn_frame, text="Video Surveillance", command=getPage3)
btn_video.grid(row=0, column=2, padx=5)
btn_manage = tk.Button(btn_frame, text="Manage Criminal", command=getPage4)
btn_manage.grid(row=1, column=2, padx=5)

# Manage Officers button in the second row
btn_manage_officers = tk.Button(btn_frame, text="Manage Officers", command=getPage5)
btn_manage_officers.grid(row=2, column=1, columnspan=2, pady=10)

# Configure buttons
for btn in btn_frame.winfo_children():
    btn.configure(font="Arial 20", width=17, bg="white", fg="black", pady=10, bd=10, highlightthickness=1,activebackground="red", activeforeground="black")

pages[0].lift()
root.mainloop()


