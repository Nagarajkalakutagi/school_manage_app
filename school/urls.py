from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('class', views.my_class, name='class'),
    path('signup', views.signup, name='signup'),
    path("update",views.update_form,name="update"),
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
]
