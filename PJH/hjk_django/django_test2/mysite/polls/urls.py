from django.urls import path
from . import views

urlpatterns = [
    # main url
    path('', views.Main_page, name='Main_page'),
    path('Chat_page', views.Chat_page, name='Chat_page'),
    path('Signup', views.Signup, name = 'Signup'),
    path('email_activate/<token>', views.email_activate , name='email_activate')

]