from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import Employee, CheckIn, CheckOut, RequestDemo, ContactUs
from .forms import EmployeeForm, RequestDemoForm, ContactUsForm, RegisterForm
import requests
import cv2
import numpy as np
import face_recognition
import os
from time import ctime
from datetime import datetime
from datetime import date
import mysql.connector

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model

# Start Sandra virtual AI Assistance
import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime

User = get_user_model()


# Create your views here.
@login_required
def home(request):
    return HttpResponse('Oops!, Go to homepage')


@login_required
def dashboard(request):
    return render(request, 'dashboard_main/home.html')


@login_required
def check_in(request):
    return render(request, 'dashboard_main/Check_In.html')


@login_required
def check_out(request):
    return render(request, 'dashboard_main/Check_Out.html')


@login_required
def edit_employees(request):
    return render(request, 'dashboard_main/edit_employees.html')


@login_required
def general_reports(request):
    return render(request, 'dashboard_main/General_Reports.html')


@login_required
def helps(request):
    return render(request, 'dashboard_main/Help.html')


@login_required
def manage_admins(request):
    admins = User.objects.all().order_by('-id')
    return render(request, 'dashboard_main/Manage_Admins.html', {'admins': admins})

def edit_admins(request, id):
    admins = User.objects.get(id=id)
    return render(request, 'dashboard_main/edit_admins.html', {'admins': admins})


@login_required
def update_admins(request, id):
    user = User.objects.get(id=id)
    user.username = request.POST['username']
    user.email = request.POST['email']
    user.password = make_password(request.POST['password'])
    user.save()
    return redirect('manage_admins')


@login_required
def destroy_admins(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect("manage_admins")


@login_required
def manage_employees(request):
    return render(request, 'dashboard_main/manage_employees.html')


@login_required
def notes(request):
    return render(request, 'dashboard_main/notes.html')


#CRUD for Employees
@login_required
def read(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('dashboard_main/Manage_Employees.html')
            except:
                pass
    else:
        employees = Employee.objects.all().order_by('-id')
    return render(request, 'dashboard_main/Manage_Employees.html', {'employees': employees})


@login_required
def new(request):
    return render(request, 'dashboard_main/add_employees.html')


@login_required
def create(request):
    employee = Employee()
    # person.id = 250734965211
    employee.employee_name = request.POST['employee_name']
    employee.image = request.FILES['image']
    employee.employee_email = request.POST['employee_email']
    employee.employee_password = make_password(request.POST['employee_password'])
    employee.employee_phone = request.POST['employee_phone']
    employee.employee_address = request.POST['employee_address']
    employee.employee_latitude = request.POST['employee_latitude']
    employee.employee_longitude = request.POST['employee_longitude']
    employee.employee_gender = request.POST['employee_gender']
    employee.save()
    return redirect('manage_employees')


@login_required
def edit(request, id):
    employees = Employee.objects.get(id=id)
    return render(request, 'dashboard_main/edit_employees.html', {'employees': employees})


@login_required
def update(request, id):
    employee = Employee.objects.get(id=id)
    employee.employee_name = request.POST['employee_name']
    employee.employee_email = request.POST['employee_email']
    employee.employee_password = request.POST['employee_password']
    employee.employee_phone = request.POST['employee_phone']
    employee.employee_address = request.POST['employee_address']
    employee.employee_latitude = request.POST['employee_latitude']
    employee.employee_longitude = request.POST['employee_longitude']
    employee.save()
    return redirect('manage_employees')


@login_required
def destroy(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("manage_employees")


@login_required
#CRUD for Check_IN
def read_checkin(request):
    employee_checkin = CheckIn.objects.all().order_by('-id')
    return render(request, 'dashboard_main/Check_In.html', {'employee_checkin': employee_checkin})



#CRUD for Check_Out
@login_required
def read_checkout(request):
    employee_checkout = CheckOut.objects.all().order_by('-id')
    return render(request, 'dashboard_main/Check_Out.html', {'employee_checkout': employee_checkout})

# ///////////////////////
# Main website Views ::::
# ///////////////////////

#######################
def login(request):
    return render(request, 'website_main/login.html')


def register_page(request):
    return render(request, 'website_main/register_page.html')

@login_required
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('manage_admins')
    else:
        form = RegisterForm()
        admins = User.objects.all().order_by('-id')
    return render(request, "dashboard_main/Manage_Admins.html", {"admins": admins})

#####################


def homepage(request):
    return render(request, 'website_main/homepage.html')


def aboutus(request):
    return render(request, 'website_main/about-us.html')


def ourmission(request):
    return render(request, 'website_main/our-mission.html')


def howitworks(request):
    return render(request, 'website_main/how-it-works.html')


def contactus(request):
    return render(request, 'website_main/contact-us.html')


def contactus_read(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('website_main/contact-us.html')
            except:
                pass
    else:
        contact_us = ContactUs.objects.all().order_by('-id')
    return render(request, 'dashboard_main/admin_contact_us.html', {'contact_us': contact_us})


def new_contact(request):
    return render(request, 'website_main/contact-us.html')


def create_contact(request):
    contact_us = ContactUs()
    # person.id = 250734965211
    contact_us.name = request.POST['name']
    contact_us.email = request.POST['email']
    contact_us.message = request.POST['message']
    contact_us.save()
    return render(request, 'website_main/contact-us.html')


def requestdemo(request):
    return render(request, 'website_main/request-demo.html')


def requestdemo_read(request):
    if request.method == "POST":
        form = RequestDemoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('website_main/request-demo.html')
            except:
                pass
    else:
        request_demo = RequestDemo.objects.all().order_by('-id')
    return render(request, 'dashboard_main/admin_request_demo.html', {'request_demo': request_demo})


def new_request(request):
    return render(request, 'website_main/request-demo.html')


def create_request(request):
    request_demo = RequestDemo()
    # person.id = 250734965211
    request_demo.name = request.POST['name']
    request_demo.company_name = request.POST['company_name']
    request_demo.email = request.POST['email']
    request_demo.phone = request.POST['phone']
    request_demo.save()
    return render(request, 'website_main/request-demo.html')

# ////////////////////////////
# Start Face Recognition :::::
# ////////////////////////////





def attendance(request):
    return render(request, 'website_main/attendance.html')


def attendance_check_in(request):

    #Make A Connection with DB
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="master_django_v4"
    )

    mycursor = mydb.cursor()


    path = "./static/uploads/ImageAttendance"
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def markAttendance(name, user_id):
        # myDataList = f.readlines()
        # nameList = []
        # for line in myDataList:
        #     entry = line.split(',')
        #     nameList.append(entry[0])
        # if name not in nameList:
        sql = "INSERT INTO checkin (name, day,time, user_id) VALUES (%s, %s,%s, %s)"
        now = datetime.now()
        dtString = now.strftime('%Y-%b-%d %H:%M:%S')
        dtday = now.strftime('%A')
        val = (name, dtday, dtString, user_id)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print(mycursor)
        # exit()

        # mycursor.execute("SHOW TABLE")
        # for x in mycursor:
        #     print(x)


    # with open('Attendance.csv','r+') as f:
    #     myDataList = f.readlines()
    #     nameList = []
    #     for line in myDataList:
    #         entry = line.split(',')
    #         nameList.append(entry[0])
    #     if name not in nameList:
    #         now = datetime.now()
    #         dtString = now.strftime('%H:%M:%S')
    #         f.writelines(f'\n{name},{dtString}')
    # if name in nameList:
    #     print("Alhamdulelah, I Did it")


    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
# | Start | Just for test - JPL
                employees = Employee.objects.all()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT employee_email FROM employees")
                my_result = mycursor.fetchall()
                for x in my_result:
                    print('XOXOXOXOXOXOXOXOXOXOXOXOX')
                    print(x)
                # print(Employee.objects.get(id=employees.id))
                print('xxxxxxxxxxxxxxxx')
                print(employees)
                print(mycursor)
                print('xxxxxxxxxxxxxxxx')
                print(employees)
                print('test test')
                print(classNames)
                print(classNames[matchIndex])
                print(name)
                user_id = '2'
                # print(name)
                # print(ctime())
# | End | Just for test - JPL
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name,user_id)

        cv2.imshow('webcam', img)
        cv2.waitKey(1)


    # faceLoc = face_recognition.face_locations(imgElon)[0]
    # encodeElon = face_recognition.face_encodings(imgElon)[0]
    # cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)
    #
    # print(faceLoc)
    #
    # faceLocTest = face_recognition.face_locations(imgTest)[0]
    # encodeTest = face_recognition.face_encodings(imgTest)[0]
    # cv2.rectangle(imgTest, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (50, 0, 255), 2)
    #
    # faceLocTest2 = face_recognition.face_locations(imgTest2)[0]
    # encodeTest2 = face_recognition.face_encodings(imgTest2)[0]
    # cv2.rectangle(imgTest2, (faceLocTest2[3], faceLocTest2[0]), (faceLocTest2[1], faceLocTest2[2]), (100, 0, 255), 2)
    #
    # print(faceLocTest2)
    #
    # # Results to compare
    # results = face_recognition.compare_faces([encodeElon], encodeTest)
    # faceDis = face_recognition.face_distance([encodeElon], encodeTest)
    # results_laith_with_elon = face_recognition.compare_faces([encodeElon], encodeTest2)


def attendance_check_out(request):

    #Make A Connection with DB
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="master_django_v4"
    )

    mycursor = mydb.cursor()


    path = "./static/uploads/ImageAttendance"
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def markAttendance(name, user_id):
        sql = "INSERT INTO checkout (name, day,time, user_id) VALUES (%s, %s,%s, %s)"
        now = datetime.now()
        dtString = now.strftime('%Y-%b-%d %H:%M:%S')
        dtday = now.strftime('%A')
        val = (name, dtday, dtString, user_id)
        mycursor.execute(sql, val)
        mydb.commit()

        print(mycursor.rowcount, "record inserted.")
        print(mycursor)
        # exit()

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
# | Start | Just for test - JPL
                employees = Employee.objects.all()
                mycursor = mydb.cursor()
                mycursor.execute("SELECT employee_email FROM employees")
                my_result = mycursor.fetchall()
                for x in my_result:
                    print('XOXOXOXOXOXOXOXOXOXOXOXOX')
                    print(x)
                # print(Employee.objects.get(id=employees.id))
                print('xxxxxxxxxxxxxxxx')
                print(employees)
                print(mycursor)
                print('xxxxxxxxxxxxxxxx')
                print(employees)
                print('test test')
                print(classNames)
                print(classNames[matchIndex])
                print(name)
                user_id = '2'
                # print(name)
                # print(ctime())
# | End | Just for test - JPL
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name,user_id)

        cv2.imshow('webcam', img)
        cv2.waitKey(1)


def virtual_assistance(request):
    r = sr.Recognizer()

    def record_audio(ask=False):
        with sr.Microphone() as Source:
            if ask:
                laith_speak(ask)
            audio = r.listen(Source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio)
            except sr.UnknownValueError:
                laith_speak("Sorry, I did not get that")
                return render(request, 'website_main/homepage.html')
            except sr.RequerstError:
                laith_speak("Sorry, my speech service is down")
            return voice_data

    def laith_speak(audio_string):
        tts = gTTS(text=audio_string, lang='en')
        r = random.randint(1, 1000000)
        audio_file = 'auido-' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(audio_string)
        os.remove(audio_file)

    def respond(voice_data):
        if 'what is your name' in voice_data:
            laith_speak('My name is Sandra')
        if 'who i am?' in voice_data:
            laith_speak('Laith is my boss, He create me lately by using Artifitial Intelegence technology.')
            laith_speak('I Love him to give me a chance to breath and live on this earth')
        if 'like' in voice_data:
            laith_speak('mmmm, I"m fine. What about you?')
        if 'good' in voice_data:
            laith_speak('Wow. Great to hear that')
        if 'bad' in voice_data:
            laith_speak('I feel bad. can i tell you a joke to change your mode?')
        if 'yes' in voice_data:
            laith_speak('I miss you')

        if 'what is the time now' in voice_data:
            laith_speak(ctime())
        if 'search' in voice_data:
            search = record_audio('What do you want to search for?')
            url = 'https://google.com/search?q=' + search
            webbrowser.get().open(url)
            laith_speak('Here is what I found for ' + search)
        if 'find location' in voice_data:
            location = record_audio('What is the location')
            url = 'https://google.nl/maps/place/' + location + '/&amp;'
            webbrowser.get().open(url)
            laith_speak('Here is the location of ' + location)
        if 'open' in voice_data:
            open_youtube = record_audio('Are you want to play your playlist on youtube?')
            url = 'https://www.youtube.com/watch?v=291kcUaf0rM&list=RD291kcUaf0rM&start_radio=1'
            webbrowser.get().open(url)
            laith_speak('Here is what I found for you ' + open_youtube)
        if 'exit' in voice_data:
            exit()
        if 'bye' in voice_data:
            exit(1)
        if 'bye sandra' in voice_data:
            exit(1)
        if 'see you later' in voice_data:
            exit(1)

    time.sleep(1)
    laith_speak('Hi.')
    laith_speak('This is Sandra.')
    laith_speak('I am your virtual assistant. ')
    laith_speak('How I can help you?')
    while 1:
        voice_data = record_audio()
        respond(voice_data)












