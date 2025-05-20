
from django.urls import path
from . import views

urlpatterns = [
    path('',  views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('multiplayer/', views.multiplayer, name='multiplayer'),
    path('settings/', views.settings, name='settings'),
    path('contact/', views.contact, name='contact'),

    path('questions/<int:book_id>/', views.questions, name='questions'),
    path('questions/<int:book_id>/<int:question_id>/', views.questions, name='question_detail'),
    path('store_answer/', views.store_answer, name='store_answer'),
    path('get_verse/', views.get_verse, name='get_verse'),

    path('profile/', views.profile, name='profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
