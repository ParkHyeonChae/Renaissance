from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('profile/', views.profile_view, name='profile'),
]