from django.contrib import admin
from django.urls import path, include
from fitness import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('get_fitness_plan/', views.get_fitness_plan, name='get_fitness_plan'),
]
