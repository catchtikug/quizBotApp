
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/',  views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('reviews/', views.reviews_list, name='reviews'),
    path('multiplayer/', views.multiplayer, name='multiplayer'),
    path('settings/', views.settings, name='settings'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Partners
    path('partners/', views.public_partners, name='public_partners'),
    path('admins/partners/', views.partners_view, name='partners'),
    path('admins/partners/add/', views.add_partner, name='add_partner'),
    path('admins/partners/<int:partner_id>/update/', views.update_partner, name='update_partner'),
    path('admins/partners/<int:partner_id>/delete/', views.delete_partner, name='delete_partner'),

    # Admin dashboard URLs
    path('admins/users/', views.user_management, name='user_management'),
    path('admins/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('admins/users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('admins/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('admins/reports/', views.reports_view, name='reports'),
    path('admins/settings/', views.settings_view, name='settings'),
    path('admins/active-sessions/', views.active_sessions_view, name='active_sessions'),
    path('admins/pending-reports/', views.pending_reports_view, name='pending_reports'),

    path('questions/<int:book_id>/', views.questions, name='questions'),
    path('questions/<int:book_id>/<int:question_id>/', views.questions, name='question_detail'),
    path('store_answer/', views.store_answer, name='store_answer'),
    path('get_verse/', views.get_verse, name='get_verse'),

    path('profile/', views.profile, name='profile'),
    path('profile/update-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
