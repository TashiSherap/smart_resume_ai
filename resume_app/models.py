from django.db import models

class Resume(models.Model):
    ROLE_CHOICES = [
        ("backend", "Backend Developer"),
        ("data_analyst", "Data Analyst"),
        ("ai_engineer", "AI Engineer"),
    ]

    # Personal Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Profile Section
    profile = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="GitHub / LinkedIn / Portfolio link or username"
    )

    profile_summary = models.TextField(
        blank=True,
        null=True,
        help_text="Short professional summary shown at the top of the resume"
    )

    # Resume Sections
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)

    # Target Role
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="backend"
    )

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"
