from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import Employee, CheckIn, CheckOut, RequestDemo, ContactUs
from .forms import EmployeeForm, RequestDemoForm, ContactUsForm, RegisterForm
from django.core.paginator import Paginator
import requests
# Face recognition
import cv2
import numpy as np
import face_recognition
import os
from time import ctime
from datetime import datetime
from datetime import date
import mysql.connector
# Auth
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
    paginator = Paginator(employee_checkin, 20)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    employee_checkin = paginator.get_page(page_number)

    return render(request, 'dashboard_main/Check_In.html', {'employee_checkin': employee_checkin})



#CRUD for Check_Out
@login_required
def read_checkout(request):
    employee_checkout = CheckOut.objects.all().order_by('-id')
    paginator = Paginator(employee_checkout, 10)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    employee_checkout = paginator.get_page(page_number)
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


def done(request):
    return render(request, 'website_main/done.html')


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


    def getEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def bluePrintAttendance(name, user_id):

        sql = "INSERT INTO checkin (name, day,time, user_id) VALUES (%s, %s,%s, %s)"
        now = datetime.now()
        dtString = now.strftime('%Y-%b-%d %H:%M:%S')
        dtday = now.strftime('%A')
        val = (name, dtday, dtString, user_id)
        mycursor.execute(sql, val)
        mydb.commit()


        print(mycursor.rowcount, "record inserted.")
        print(mycursor)
        # cv2.destroyAllWindows()


    encodeListKnown = getEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)
    print('three yes')

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
                bluePrintAttendance(name,user_id)
                print('one yes')

        cv2.imshow('webcam', img)
        key = cv2.waitKey(1)
        if key == ord('n') or key == ord('p') or key == 27:
            break

    # Exit->All capture Done,
    cap.release()
    cv2.destroyAllWindows()
    return redirect('done')



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


    def getEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def bluePrintAttendance(name, user_id):
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

    encodeListKnown = getEncodings(images)
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
                bluePrintAttendance(name,user_id)

        cv2.imshow('webcam', img)
        key = cv2.waitKey(1)
        if key == ord('n') or key == ord('p') or key == 27:
            break

    # Exit->All capture Done,
    cap.release()
    cv2.destroyAllWindows()
    return redirect('done')

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
        if 'open video' in voice_data:
            open_youtube = record_audio('What are you looking for on youtube?')
            url = 'https://www.youtube.com/results?search_query=' + open_youtube
            webbrowser.get().open(url)
            laith_speak('Here is what I found for you ' + open_youtube)
        if 'news' in voice_data:
            open_cnn = record_audio('Do you want to start news?')
            url = 'https://tunein.streamguys1.com/cnn-new?ads.cust_params=partnerId%253dydvgH5BP%2526ads_partner_alias%253dydvgH5BP%2526premium%253dfalse%2526abtest%253d%2526language%253den-US%2526stationId%253ds20407%2526is_ondemand%253dfalse%2526genre_id%253dg3124%2526class%253dtalk%25252cspoken%25252cnews%2526is_family%253dfalse%2526is_mature%253dfalse%2526country_region_id%253d227%2526station_language%253denglish%2526programId%253dp341054%2526is_event%253dfalse&url=https%3a%2f%2ftunein.com%2fdesc%2fs20407%2f&description_url=https%3a%2f%2ftunein.com%2fdesc%2fs20407%2f&ads.npa=1&ads.gdfp_req=1&aw_0_1st.playerid=ydvgH5BP&aw_0_1st.skey=1619436777&aw_0_1st.platform=tunein'
            webbrowser.get().open(url)
            laith_speak('Here is what I found news for you ' + open_cnn)
        if 'Homepage' in voice_data:
            laith_speak('Opening Homepage, Im happy to help you')
            webbrowser.get().open('http://127.0.0.1:8000/homepage/')
        if 'about us' in voice_data:
            laith_speak('Opening about us page, Im happy to help you')
            webbrowser.get().open('http://127.0.0.1:8000/about-us/')
        if 'attendance area' in voice_data:
            laith_speak('Opening Attendance area, Im happy to help you')
            webbrowser.get().open('http://127.0.0.1:8000/attendance/')
        if 'How it works' in voice_data:
            laith_speak('Opening How it works, Im happy to help you')
            webbrowser.get().open('http://127.0.0.1:8000/how-it-works/')
        if 'contact us' in voice_data:
            laith_speak('Opening contact us, Im happy to help you')
            webbrowser.get().open('http://127.0.0.1:8000/contact-us/')


        if 'exit' in voice_data:
            exit()
        if 'bye' in voice_data:
            print('bye')
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












