from django.urls import path

from . import views

app_name = 'EMS'
# url patterns has list of all urls corresponding to the views and the webpages
urlpatterns = [
    path('', views.main, name='main'),
    path('login/organizer', views.login_page_organizer, name = 'login_page_organizer'),
    path('login/participant', views.login_page_participant, name = 'login_page_participant'),
    path('event_view/<int:event_id>/', views.event_view, name='event_view'),
    # path('logout/', views.logout_page, name= 'logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home_page, name='home_page'),
    path('event_registration/', views.event_registration, name='event_registration'),
    path('event_edit/<int:id>', views.event_edit, name='event_edit'),
    path('delete_event/<int:id>', views.delete_event, name='delete_event'),
    path('statistics/', views.statistics_page, name='statistics'),
    path('register_event/<int:event_id>/', views.register_for_event, name='register_event'),
    path('unregister_event/<int:registration_id>/', views.unregister_from_event, name='unregister_event'),

    # path('profile/<str:username>', views.profile, name = 'profile'),
    # #path('editprofile/<str:username>', views.edit_profile, name = 'edit_profile'),
    # path('userprofiles/', views.user_profiles, name = 'user_profiles'),
]
