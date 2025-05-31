# splint_app/admin.py
from django.contrib import admin
from .models import UserProfile, Unit, LearningResource, SimulationFeedback

admin.site.register(UserProfile)
admin.site.register(Unit) # <--- 確保這一行存在
admin.site.register(LearningResource)
admin.site.register(SimulationFeedback)