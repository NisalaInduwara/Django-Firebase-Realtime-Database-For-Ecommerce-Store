from django.shortcuts import render
import pyrebase
import requests

config = {
    'apiKey': "AIzaSyCEGnQQGooTl78XxDWBCsq7PQXCEEDptuQ",
    'authDomain': "anu-stores-items-databas-74b5c.firebaseapp.com",
    'databaseURL': "https://anu-stores-items-databas-74b5c-default-rtdb.firebaseio.com",
    'projectId': "anu-stores-items-databas-74b5c",
    'storageBucket': "anu-stores-items-databas-74b5c.appspot.com",
    'messagingSenderId': "371702204990",
    'appId': "1:371702204990:web:f0975392a8829fb0e75f6f",
    'measurementId': "G-16WNR1EMGP"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
database = firebase.database()

def signIn(request):
    return render(request, "login.html")

def home(request):
    return render(request, "home.html")


def postsignIn(request):
    
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user=auth.sign_in_with_email_and_password(email, password)
    except:
        message="Invalid Credentials!! Please check your data"
        return render(request, "login.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "home.html", {"email": email})


def logout(request):

    try:
        del request.session['uid']
    except:
        pass
    return render(request, "login.html")


def signUp(request):
    return render(request, "Registration.html")

def postsignUp(request):

    email = request.POST.get('email')
    password = request.POST.get("password")
    name = request.POST.get("name")

    try:
        user=auth.create_user_with_email_and_password(email, password)
        uid = user['localId']
        idtoken = request.session['uid']
    except:
        message="Invalid Credentials!! Can't register User"
        return render(request, "registration.html", {"message": message})
        
    return render(request, 'login.html')


def reset(request):
    return render(request, "Reset.html")


def postReset(request):

    email = request.POST.get('email')

    try:
        auth.send_password_reset_email(email)
        message = 'Email has sent to reset your password'
        return render(request, 'Reset.html', {'message': message})
    except:
        message = 'Something went wrong please enter an correct email'
        return render(request, 'Reset.html', {'message': message})

    
def add_item(request):
    return render(request, 'add_item.html')


def add_item_form(request):

    if not request.session.get('uid'):
        return render(request, 'login.html')
    
    item_id = request.POST.get('item_id')
    item_link = request.POST.get('item_link')
    item_name = request.POST.get('item_name')
    profit = request.POST.get('item_profit')
    description = request.POST.get('description')

    item_data = {
        'item_id': item_id,
        'item_link': item_link,
        'item_name': item_name,
        'item_profit': float(profit),
        'description': description
    }

    try:
        uid = request.session['uid']
        item_id = str(item_id) 
        new_item_ref = database.child('Items').child(item_id).set(item_data)
        message = 'Item added successfully'
        return render(request, 'home.html', {'message': message})
    
    except Exception as e:
        message = f'Error adding item: {str(e)}'
        return render(request, 'home.html', {'message': message})


def get_item_link_form(request):

    if not request.session.get('uid'):
        return render(request, 'login.html')
    
    item_id = request.GET.get('item_id')
    item_id = str(item_id)

    try:
        item_link = database.child('Items').child(item_id).child('item_link').get().val()
        return render(request, 'home.html', {'item_link': item_link})
    except Exception as e:
        message = f'Error getting item link: {str(e)}'
        return render(request, 'home.html', {'message': message})

