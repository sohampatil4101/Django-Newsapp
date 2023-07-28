from django.urls import path
from Newsapp import views
urlpatterns = [
    path('',views.home, name="home" ),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('newshome', views.newshome, name="newshome"),
    path('newscategories/<str:category>', views.newscategories, name="newscategories"),
    path('forgetpassword', views.forgetpassword, name="forgetpassword"),
    path('changepassword', views.changepassword, name="changepassword"),
    path('otpverification', views.otpverification, name="otpverification"),
    path('generateotp', views.generateotp, name="generateotp"),
    path('profile', views.profile, name="profile"),
    path('viewblog/<str:key>/<str:email>', views.viewblog, name="viewblog"),
    path('deleteblog/<str:key>/<str:email>', views.deleteblog, name="deleteblog"),
    path('createblog', views.createblog, name="createblog"),
    path('updateblog/<str:key>', views.updateblog, name="updateblog"),


    # api calls
    path('api/blogview', views.blogview, name="blogview"),
    path('api/createblog', views.createblog, name="createblog"),
    path('api/blogkeyview/<int:key>', views.blogkeyview, name="blogkeyview"),

]