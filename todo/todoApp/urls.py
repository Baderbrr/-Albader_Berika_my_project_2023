from django.urls import path
from .views import index, register_view, edit_note_view,  delete_note_view, login_view, logout_view, create_note_view

# list of URLs that fire off given function 
urlpatterns = [
    path('index/', index, name='index'),
    path('create-note/', create_note_view, name='create-note'),
    path('delete-note/<int:pk>', delete_note_view, name='delete-note'), 
    path('update-note/<int:pk>', edit_note_view, name='update-note'),
    path('register/', register_view, name='register-user'),
    path('login/', login_view, name='login-user'),
    path('logout/', logout_view, name='logout'),
]
