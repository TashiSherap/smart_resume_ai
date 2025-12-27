from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume_builder/', views.resume_builder, name='resume_builder'),
    path('preview_resume/<int:resume_id>/', views.preview_resume, name='preview_resume'),
    path('download_resume/<int:resume_id>/', views.generate_pdf, name='download_resume'),
]
