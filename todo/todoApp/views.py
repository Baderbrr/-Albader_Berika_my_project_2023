from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, ToDoForm
from datetime import datetime
from .models import Note, User
import pytz

current_datetime = datetime.now(pytz.utc)

def login_view(request):
    form = LoginForm()
    message=''
    if request.method == "POST":
        form = LoginForm(request.POST) # filling form with sent data with post request
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user) # using login() builtin method to authenticate the user 
                return redirect('index')
            else:
                message='Login Failed'
    
    return render(request, 'login.html', {"message": message}) # rendering login.html if the request method is GET

def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                                email=form.cleaned_data['typeEmailX'],
                                                password=form.cleaned_data['typePasswordX'])
            new_user.save() # saving new created user in database
            return redirect('login-user') # redirecting to login form after user created
            
    return render(request, 'register.html') # render register.html if the request method is GET

def logout_view(request):
    logout(request) # using logout() built in django method to delete authentication of user from the current session
    return redirect('/login')


def index(request):
    notes = Note.objects.filter(user=request.user).order_by('due_date') # get all the notes from database for logged in user and order them based od Due_date param
    for note in notes:
        if note.due_date < current_datetime: # check if notes from database has it's time expired if so then expired parameter is set to True
            note.expired = True
            note.save()
    return render(request, 'index.html', {"notes": notes})

def create_note_view(request):
    if request.method == "POST":
        print(request.POST)
        form = ToDoForm(request.POST)
        if form.is_valid():
            Note.objects.create(user=request.user, title=form.cleaned_data['title'], content=form.cleaned_data['content'], created_date=form.cleaned_data['due_date'], due_date=form.cleaned_data['due_date'])
            return redirect('index')
    else:
        form = ToDoForm() # reqquest.method == "GET"
    return render(request, 'create_note_form.html')

def edit_note_view(request, pk):
    note = Note.objects.get(id=pk) # get's one specific note based on id from URL (pk is dynamica value from URL)
    if request.method == "POST":
        form = ToDoForm(request.POST)
        if form.is_valid():
            note.title = form.cleaned_data['title'] # if the form is valid with the ToDoForm class then variables of object that we got from database are set to new one from form object
            note.content = form.cleaned_data['content']
            note.due_date = form.cleaned_data['due_date']
            if form.cleaned_data['due_date'] < current_datetime:
                note.expired = True
            else: 
                note.expired = False
            note.save()
            return redirect('index')
    else:
        form = {"id": note.id, 'title': note.title, 'content': note.content, 'due_date': note.due_date} # send context object to template if request method is GET so form can be preffiled with this data from database
    return render(request, 'update_note.html', {"form_data": form})
    
def delete_note_view(request, pk):
    Note.objects.get(id=pk).delete() # look for one specific note based on dymic value of URL and delete it
    return redirect('index')

def remove(request, item_id):
    item = Note.objects.get(id=item_id)
    item.delete()
    messages.info(request, "item removed")
    return redirect('index')