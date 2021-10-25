from django.urls import path,include
from home import views


urlpatterns = [
     path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('search/',views.search,name='search'),
    path('signup/',views.handleSignup,name='signup'),
    path('login/',views.handlelogin, name='loggingin'),
    path('logout/',views.handlelogout,name='loggingout')
]