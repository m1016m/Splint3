from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_landing_view, name='course_landing'),
    path('pre-test/', views.pre_test_view, name='pre_test'),
    path('unit/<str:unit_code>/', views.unit_detail_view, name='unit_detail'),
    path('simulation/', views.simulation_view, name='simulation'),
    path('simulation/feedback/', views.simulation_feedback_view, name='simulation_feedback'),
]