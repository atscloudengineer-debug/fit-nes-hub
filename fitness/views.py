from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import HealthData
import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect("login")
    return render(request, "register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
    return render(request, "login.html")

from django.shortcuts import render, redirect
from .models import HealthData
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user
    if request.method == "POST":
        height = request.POST.get("height")
        weight = request.POST.get("weight")
        body_fat = request.POST.get("body_fat")
        heart_rate = request.POST.get("heart_rate")
        blood_pressure = request.POST.get("blood_pressure")
        activity_level = request.POST.get("activity_level")
        workout_preference = request.POST.get("workout_preference")

        sugar = request.POST.get("sugar") == "on"
        diabetes = request.POST.get("diabetes") == "on"
        thyroid = request.POST.get("thyroid") == "on"
        cholesterol = request.POST.get("cholesterol") == "on"

        # Check if user already has a record
        health_data, created = HealthData.objects.get_or_create(user=user)
        
        # Update fields
        health_data.height = float(height) if height else None
        health_data.weight = float(weight) if weight else None
        health_data.body_fat = float(body_fat) if body_fat else None
        health_data.heart_rate = int(heart_rate) if heart_rate else None
        health_data.blood_pressure = blood_pressure
        health_data.activity_level = activity_level
        health_data.workout_preference = workout_preference
        health_data.sugar = sugar
        health_data.diabetes = diabetes
        health_data.thyroid = thyroid
        health_data.cholesterol = cholesterol

        return redirect("get_fitness_plan")  # Redirect after saving

    # Fetch user's health data
    health_data = HealthData.objects.filter(user=user).first()
    return render(request, "dashboard.html", {"health_data": health_data})


def get_fitness_plan(request):
    user_health = HealthData.objects.get(user=request.user)
    prompt = f"Create a fitness and diet plan for a person with height {user_health.height} cm, weight {user_health.weight} kg, "
    prompt += f"sugar: {user_health.sugar}, diabetes: {user_health.diabetes}, thyroid: {user_health.thyroid}, cholesterol: {user_health.cholesterol}."

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return render(request, "plan.html", {"plan": response.text})


def chatbot(request):
    if request.method == "POST":
        user_query = request.POST["message"]
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(user_query)
        return render(request, "chatbot.html", {"response": response.text})

    return render(request, "chatbot.html")

