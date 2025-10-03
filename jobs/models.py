from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile   # assuming Profile extends User with is_employer flag


class Job(models.Model):
    employer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'is_employer': True}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.employer.user.username})"   # ✅ shows job + employer


class Application(models.Model):
    JOB_STATUS = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('hired', 'Hired'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    seeker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        limit_choices_to={'is_employer': False}
    )
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='applications/', blank=True, null=True)
    status = models.CharField(max_length=30, choices=JOB_STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seeker.user.username} -> {self.job.title}"   # ✅ shows seeker + job


class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.application.seeker.user.username} - {self.application.job.title} @ {self.scheduled_at}"  # ✅ clearer


