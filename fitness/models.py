from django.db import models
from django.contrib.auth.models import User

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    height = models.FloatField(blank=True, null=True)  # Storing height in cm
    weight = models.FloatField(blank=True, null=True)  # Storing weight in kg
    bmi = models.FloatField(blank=True, null=True)  # BMI (calculated later)
    body_fat = models.FloatField(blank=True, null=True)  # Body fat percentage
    heart_rate = models.IntegerField(blank=True, null=True)  # Resting heart rate (bpm)
    blood_pressure = models.CharField(max_length=10, blank=True, null=True)  # Blood pressure (e.g., "120/80")
    activity_level = models.CharField(
        max_length=20,
        choices=[
            ("sedentary", "Sedentary"),
            ("light", "Light Activity"),
            ("moderate", "Moderate Activity"),
            ("active", "Active"),
            ("very_active", "Very Active"),
        ],
        default="moderate"
    )
    workout_preference = models.CharField(
        max_length=50,
        choices=[
            ("strength", "Strength Training"),
            ("cardio", "Cardio"),
            ("yoga", "Yoga"),
            ("crossfit", "CrossFit"),
            ("mixed", "Mixed Workouts"),
        ],
        default="mixed"
    )
    sugar = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    thyroid = models.BooleanField(default=False)
    cholesterol = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.height and self.weight:
            self.bmi = round(self.weight / ((self.height / 100) ** 2), 2)  # Calculate BMI
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Health Data"
