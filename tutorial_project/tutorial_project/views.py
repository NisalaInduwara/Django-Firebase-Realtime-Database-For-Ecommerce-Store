from django.shortcuts import render
import pyrebase

config = {
    'apiKey': "AIzaSyDlaarTZeNO2_OKgbk9pjTod2kDpcHJfHg",
    'authDomain': "django-firebase-tutorial.firebaseapp.com",
    'databaseURL': "https://django-firebase-tutorial-default-rtdb.firebaseio.com",
    'projectId': "django-firebase-tutorial",
    'storageBucket': "django-firebase-tutorial.appspot.com",
    'messagingSenderId': "188805594137",
    'appId': "1:188805594137:web:85fd219a61566563777e88",
    'measurementId': "G-6PCKZS9HCF"
}

firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()

def signin(request):

    return render(request, "signin.html")


def postsignin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = auth.sign_in_with_email_and_password(email, password)

    return render(request, "welcome.html", {"e" : email})
