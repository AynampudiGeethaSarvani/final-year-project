from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
           path("Admin.html", views.Admin, name="Admin"),
           path("AdminLogin", views.AdminLogin, name="AdminLogin"),
           path('Accuracy.html', views.Accuracy, name="Accuracy"),
	       path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
	       path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('EditProfile.html', views.EditProfile, name="EditProfile"), 
	       path('EditMyProfile', views.EditMyProfile, name="EditMyProfile"),
	       path('ChangePassword.html', views.ChangePassword, name="ChangePassword"),
	       path('ChangeMyPassword', views.ChangeMyPassword, name="ChangeMyPassword"),
           path("Viewuser.html", views.ViewUser, name="Viewuser"),
           path('HomePage.html', views.HomePage, name="HomePage"),
           path("Viewusers.html", views.ViewUsers, name="Viewusers"),
           path('Predict.html', views.Predict, name="Predict"),
           path('Prediction.html', views.Prediction, name="Prediction"),
]