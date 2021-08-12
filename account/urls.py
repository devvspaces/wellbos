from django.urls import path

from . import views


app_name='account'
urlpatterns = [
    path('login-register/', views.AuthenticationView.as_view(), name='authentication'),
    path('logout/', views.Logout, name='logout'),

    path('change-password/', views.ChangePassword.as_view(), name='change_password'),
    
    path("activate/<slug:uidb64>/<slug:token>/", views.activate_email, name="activate"),

    path('reset-password/', views.ResetPasswordFormPage.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', views.ResetPasswordVerify.as_view(), name='password_reset_confirm'),
]
