import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mess
from tkinter import ttk
import tkinter.simpledialog as tsd
import os
import cv2
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import winsound
import pymongo


# Database Connectivity===========================================================
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["FRAMS_DATABASE"] #Database

#  Collections *******************************************************************
mycol_pd = mydb["Personal_Details"]
mycol_att = mydb["Attendance"]
mycol_tr = mydb["Total_Registrations"]



# Functions===========================================================


# AskforQUIT
def on_closing():
    winsound.PlaySound("sounds/Quit_init.wav", winsound.SND_FILENAME)
    if mess.askyesno("Exit", "Do you want to quit?"):
        winsound.PlaySound("sounds/Quit_final.wav", winsound.SND_FILENAME)
        time.sleep(0.1)
        winsound.PlaySound("sounds/Climax.wav", winsound.SND_FILENAME)
        window.destroy()

# Cancel
def on_cancel():
    winsound.PlaySound("sounds/Cancel.wav", winsound.SND_FILENAME)
    master.destroy()

# contact
def contact():
    mess._show(title="Contact Me",
               message="If you find anything weird or you need any help contact me on 'AppleDog@gmail.com'")


# instructions
def instructions():
    mess._show(title="Instructions",
               message="For Registrations,Enter Your ID & Name and then Follow the below steps:\n\n\nStep 1:  Take Images\n\nStep 2:   Save Profile\n\nPlease Make Sure To Have A Clean Background Before Taking the Image. ")


# about
def about():
    winsound.PlaySound("sounds/About.wav", winsound.SND_ASYNC)
    mess._show(title="About", message="This Attendance System is designed by Team AppleDog")


# clearbutton
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    res = ""
    message1.configure(text=res)
    winsound.PlaySound("sounds/Clear.wav", winsound.SND_FILENAME)


# Check for correct Path
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


# check for haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='haarcascade file missing', message='some file is missing.Please contact me for help')
        window.destroy()


# check the password for change the password
def save_pass():
    winsound.PlaySound("sounds/SavePass.wav", winsound.SND_FILENAME)
    global str
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str = tf.read()
    else:
        master.destroy()
        new_pas = tsd.askstring('Password not set', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='Null Password Entered', message='Password not set.Please try again!')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered!', message='New password was registered successfully!')
            return
    op = (old.get())
    newp = (new.get())
    nnewp = (nnew.get())
    if (op == str):
        if (newp == nnewp):
            txf = open("Pass_Train\pass.txt", "w")
            txf.write(newp)
        else:
            mess._show(title='Error', message='Confirm new password again!!!')
            return
    else:
        mess._show(title='Wrong Password', message='Please enter correct old password.')
        return
    mess._show(title='Password Changed', message='Password changed successfully!!')
    master.destroy()


# change password
def change_pass():
    winsound.PlaySound("sounds/chng_pass.wav", winsound.SND_ASYNC)
    global master
    master = tkinter.Tk()
    master.geometry("500x200")
    master.resizable(False, False)
    master.title("Change Admin Password")
    master.configure(background="#070911")
    master.attributes('-alpha', 0.89)
    lbl4 = tkinter.Label(master, text='    Enter Old Password', bg='#070911', fg='#007ef9',
                         font=('Microsoft San Serif', 11, ' bold '))
    lbl4.place(x=10, y=20)
    global old
    old = tkinter.Entry(master, width=36, fg='white', bg='#4a4f63', relief='solid',
                        font=('Microsoft San Serif', 11, ' bold '), show='*')
    old.place(x=185, y=20)
    lbl5 = tkinter.Label(master, text='   Enter New Password', bg='#070911', fg='#007ef9',
                         font=('Microsoft San Serif', 11, ' bold '))
    lbl5.place(x=10, y=55)
    global new
    new = tkinter.Entry(master, width=36, fg='white', bg='#4a4f63', relief='solid',
                        font=('Microsoft San Serif', 11, ' bold '), show='*')
    new.place(x=185, y=55)
    lbl6 = tkinter.Label(master, text='Confirm New Password', bg='#070911', fg='#007ef9',
                         font=('Microsoft San Serif', 11, ' bold '))
    lbl6.place(x=10, y=90)
    global nnew
    nnew = tkinter.Entry(master, width=36, fg='white', bg='#4a4f63', relief='solid',
                         font=('Microsoft San Serif', 11, ' bold '), show='*')
    nnew.place(x=185, y=90)

    cancel = tkinter.Button(master, text="Cancel", command=on_cancel, fg="white", bg="#ff0000", height=1, width=23,
                            activebackground="#de2020", font=('Microsoft San Serif', 11, ' bold '))
    cancel.place(x=260, y=150)
    save1 = tkinter.Button(master, text="Save", command=save_pass, fg="white", bg="#0081ff", height=1, width=23,
                           activebackground="#277ed3", font=('Microsoft San Serif', 11, ' bold '))
    save1.place(x=25, y=150)
    master.mainloop()


# ask for password
def psw():
    winsound.PlaySound("sounds/ProfileSave.wav", winsound.SND_FILENAME)
    global str_pass
    assure_path_exists("Pass_Train/")
    exists1 = os.path.isfile("Pass_Train\pass.txt")
    if exists1:
        tf = open("Pass_Train\pass.txt", "r")
        str_pass = tf.read()
    else:
        new_pas = tsd.askstring('Old Password not found', 'Please enter a new password below', show='*')
        if new_pas == None:
            mess._show(title='No Password Entered', message='Password not set!! Please try again')
        else:
            tf = open("Pass_Train\pass.txt", "w")
            tf.write(new_pas)
            mess._show(title='Password Registered', message='New password was registered successfully!!')
            return
    password = tsd.askstring('Password', 'Enter Password', show='*')
    if password == str_pass:
        TrainImages()

    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='You have entered wrong password')


# $$$$$$$$$$$$$
def TakeImages():
    winsound.PlaySound("sounds/TakeImg.wav", winsound.SND_FILENAME)
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("PersonsDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("PersonsDetails\PersonsDetails.csv")
    if exists:
        with open("PersonsDetails\PersonsDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("PersonsDetails\PersonsDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.05, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('Taking Images', img)
            # wait for 10 miliseconds
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()

        winsound.PlaySound("sounds/Img_Taken.wav", winsound.SND_FILENAME)

        # _____________CSV Data Entry_______________________________________________________
        res = "                             Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]


        #_____________Database Data Entry_______________________________________________________
        info_pd={ 'ID_No': Id,'S.No':serial , 'Name': name}
        insert_val=mycol_pd.insert_one(info_pd)

        with open('PersonsDetails\PersonsDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)


########################################################################################
# $$$$$$$$$$$$$
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("Pass_Train/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return
    recognizer.save("Pass_Train\Trainner.yml")
    res = "                              Profile Saved Successfully"
    message1.configure(text=res)
    time.sleep(0.1)
    winsound.PlaySound("sounds/TotalRegistration.wav", winsound.SND_FILENAME)
    message.configure(text='Total Registrations till now  : ' + str(ID[0]))


############################################################################################3
# $$$$$$$$$$$$$
def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


###########################################################################################
# $$$$$$$$$$$$$
def TrackImages():
    winsound.PlaySound("sounds/Attendance.wav", winsound.SND_FILENAME)
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("PersonsDetails/")
    for k in tb.get_children():
        tb.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    exists3 = os.path.isfile("Pass_Train\Trainner.yml")
    if exists3:
        recognizer.read("Pass_Train\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Please click on Save Profile to reset data!!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("PersonsDetails\PersonsDetails.csv")
    if exists1:

        df = pd.read_csv("PersonsDetails\PersonsDetails.csv")
    else:
        mess._show(title='Details Missing', message='Students details are missing, please check!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)] # CSV
                att = {'ID_No': str(ID), 'Name': bb, 'Date': str(date), 'Time': str(timeStamp)} #DATABASE

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 255, 0), 2)
        cv2.putText(im, 'Press Q to Take Attendance', (155, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)
        cv2.imshow('Taking Attendance', im)

        if (cv2.waitKey(1) == ord('q')):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1) #CSV
            writer.writerow(attendance)
            insert_att = mycol_att.insert_one(att) #DATABASE
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1) #CSV
            writer.writerow(col_names)
            writer.writerow(attendance)
            insert_att = mycol_att.insert_one(att) #DATABASE
        csvFile1.close()

    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tb.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()


# Front End===========================================================
if __name__ == "__main__":
    # front End Inside Main Function
    time.sleep(0.1)
    winsound.PlaySound("sounds/loadsound1.wav", winsound.SND_ASYNC)
    window = tkinter.Tk()
    #resolution of application
    window_width = 1280 #width of application
    window_height = 720 #height of application

    # get screen width and height
    screen_width = window.winfo_screenwidth() #actual screen width
    screen_height = window.winfo_screenheight() #actual screen height

    # calculate position x and y coordinates
    x = (screen_width / 2) - (window_width / 2) # x coordinate for center window placement
    y = (screen_height / 2) - (window_height / 2) # y coordinate for center window placement

    window.title("FRAMS - Face Recognition Based Attendance Management System")
    window.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    bgimg = PhotoImage(file="app_file\gui_im.png")
    my_labelbg = Label(window, image=bgimg)
    my_labelbg.place(x=-1.6, y=0, relwidth=1, relheight=1)
    exec(open('Loader\loading.py').read())
    winsound.PlaySound("sounds/loadsound2.wav", winsound.SND_ASYNC)
    time.sleep(2.5)
    winsound.PlaySound("sounds/Startup.wav", winsound.SND_ASYNC)
    window.resizable(False, False)
    window.configure(background='#0f1320')
    window.iconbitmap('icon\cam_icon.ico')
    window.attributes('-alpha', 0.89)



    # Help menubar----------------------------------------------
    menubar = Menu(window)
    help = Menu(menubar, tearoff=0)
    help.add_command(label="Change Password!", command=change_pass)
    help.add_command(label="Contact Us", command=contact)
    help.add_command(label="Instructions", command=instructions)
    help.add_separator()
    help.add_command(label="Exit", command=on_closing)
    menubar.add_cascade(label="Help", menu=help)

    # add ABOUT label to menubar-------------------------------
    menubar.add_command(label="About", command=about)

    # This line will attach our menu to window
    window.config(menu=menubar)

    # main window------------------------------------------------

    # message3 = tkinter.Label(window, text="Face Recognition Based Attendance Management System" ,fg="white",bg="#181e36" ,width=60 ,height=1,font=('times', 29, ' bold '))
    # message3.place(x=10, y=10,relwidth=1)


    # frames-------------------------------------------------
    frame1 = tkinter.Frame(window, bg='#121624')
    frame1.place(relx=0.09, rely=0.13, relwidth=0.39, relheight=0.80)

    frame2 = tkinter.Frame(window, bg='#121624')
    frame2.place(relx=0.53, rely=0.13, relwidth=0.39, relheight=0.80)

    # frame_header
    fr_head1 = tkinter.Label(frame1, text="Registration", fg="white", bg="black", font=('times', 17, ' bold '))
    fr_head1.place(x=0, y=0, relwidth=1, relheight=0.085)

    fr_head2 = tkinter.Label(frame2, text="Mark Attendance", fg="white", bg="black", font=('times', 17, ' bold '))
    fr_head2.place(x=0, y=0, relwidth=1, relheight=0.085)

    # registration frame
    lbl = tkinter.Label(frame1, text="Enter ID", width=20, height=1, fg='#007ef9', bg='#121624',
                        font=('Microsoft San Serif', 15, ' bold '))
    lbl.place(x=0, y=55)

    txt = tkinter.Entry(frame1, width=32, fg="white", bg="#4a4f63", highlightcolor='#007ef9', highlightthickness=2,
                        font=('Microsoft San Serif', 13, ' bold '))
    txt.place(x=55, y=88, relwidth=0.79, relheight=0.072)

    lbl2 = tkinter.Label(frame1, text="     Enter Name", width=20, fg='#007ef9', bg='#121624',
                         font=('Microsoft San Serif', 15, ' bold '))
    lbl2.place(x=0, y=140)

    txt2 = tkinter.Entry(frame1, width=32, fg="white", bg="#4a4f63", highlightcolor='#007ef9', highlightthickness=2,
                         font=('Microsoft San Serif', 13, ' bold '))
    txt2.place(x=55, y=173, relwidth=0.79, relheight=0.072)

    message0 = tkinter.Label(frame1, text="", bg='#121624', fg="white", width=39, height=1,
                             font=('times', 16, ' bold '))
    message0.place(x=7, y=275)

    message1 = tkinter.Label(frame1, text="", bg='#121624', fg="white", width=39, height=1, activebackground="yellow",
                             font=('Microsoft San Serif', 12, ' bold '))
    message1.place(x=7, y=430)

    message = tkinter.Label(frame1, text="", bg="white", fg="black", width=39, height=1, activebackground="yellow",
                            font=('Microsoft San Serif', 16, ' bold '))
    message.place(x=7, y=500)
    # Attendance frame
    lbl3 = tkinter.Label(frame2, text="         Attendance Table", width=20, fg='#007ef9', bg='#121624', height=1,
                         font=('Microsoft San Serif', 15, ' bold '))
    lbl3.place(x=100, y=115)

    # Display total registration----------
    res = 0

    exists = os.path.isfile("PersonsDetails\PersonsDetails.csv")
    if exists:
        with open("PersonsDetails\PersonsDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                res = res + 1
        res = (res // 2) - 1

        info_tr = mycol_tr.find({'_id': '0'})
        for i in info_tr:

            info_tr=i

        new_tr = {"$set": {'_id':'0' , 'Total Registrations': res}}
        mycol_tr.update_one(info_tr, new_tr)

        csvFile1.close()

    else:
        res = 0
        info_tr = mycol_tr.find({'_id':'0'})

        if info_tr.count() > 0 :
            pass
        else :
            tr = {'_id': '0', 'Total Registrations': res}
            mycol_tr.insert_one(tr)




    message.configure(text='Total Registrations : ' + str(res), fg="white", bg='#121624')






    # BUTTONS----------------------------------------------
    cb1 = PhotoImage(file='icon/button_clear.png')
    cb_label1 = Label(image=cb1)
    clearButton = tkinter.Button(frame1, image=cb1, command=clear, borderwidth=0, fg="white", bg='#121624', width=6,
                                 activebackground="#121624", font=('times', 12, ' bold '))
    clearButton.pack(pady=20)
    clearButton.place(x=55, y=230, relwidth=0.28)

    cb2 = PhotoImage(file='icon/button_take-images.png')
    cb_label2 = Label(image=cb2)
    takeImg = tkinter.Button(frame1, image=cb2, command=TakeImages, borderwidth=0, fg="black", bg='#121624', width=6,
                             activebackground='#121624', font=('times', 16, ' bold '))
    takeImg.pack(pady=20)
    takeImg.place(x=30, y=290, relwidth=0.89)

    cb3 = PhotoImage(file='icon/button_save-profile.png')
    cb_label3 = Label(image=cb3)
    trainImg = tkinter.Button(frame1, image=cb3, command=psw, borderwidth=0, fg="black", bg='#121624', width=6,
                              activebackground='#121624', font=('times', 16, ' bold '))
    trainImg.pack(pady=20)
    trainImg.place(x=30, y=350, relwidth=0.89)

    cb4 = PhotoImage(file='icon/button_take-attendence.png')
    cb_label4 = Label(image=cb4)
    trackImg = tkinter.Button(frame2, image=cb4, command=TrackImages, borderwidth=0, fg="black", bg='#121624',
                              activebackground='#121624', font=('times', 16, ' bold '))
    trackImg.pack(pady=20)
    trackImg.place(x=30, y=60, relwidth=0.88)

    cb5 = PhotoImage(file='icon/button_quit.png')
    cb_label5 = Label(image=cb5)
    quitWindow = tkinter.Button(frame2, image=cb5, command=on_closing, borderwidth=0, fg="white", bg='#121624', width=6,
                                activebackground='#121624', font=('times', 16, ' bold '))
    quitWindow.pack(pady=20)
    quitWindow.place(x=30, y=480, relwidth=0.89)



    # Attandance table----------------------------
    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))  # Modify the font of the body
    style.configure("mystyle.Treeview.Heading",
                    font=('Microsoft San Serif', 13, 'bold'))  # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})], )  # Remove the borders
    tb = ttk.Treeview(frame2, height=13, columns=('name', 'date', 'time'), style="mystyle.Treeview")
    tb.column('#0', width=82)
    tb.column('name', width=130)
    tb.column('date', width=133)
    tb.column('time', width=133)
    tb.grid(row=2, column=0, padx=(0, 0), pady=(150, 0), columnspan=4, )
    tb.heading('#0', text='ID')
    tb.heading('name', text='NAME')
    tb.heading('date', text='DATE')
    tb.heading('time', text='TIME')



    # SCROLLBAR--------------------------------------------------

    scroll = ttk.Scrollbar(frame2, orient='vertical', command=tb.yview, )
    scroll.grid(row=2, column=4, padx=(0, 100), pady=(150, 0), sticky='ns')
    tb.configure(yscrollcommand=scroll.set)



    # closing lines------------------------------------------------
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

# For Creating Executable file goto terminal and run the following code
# pyinstaller.exe --onefile -w --icon=icon\FRAMS_icon.ico AttendanceSystem.py
