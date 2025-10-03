from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application, Interview
from .forms import JobForm, ApplicationForm, InterviewForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    recent = Job.objects.order_by('-created_at')[:10]
    return render(request, 'jobs/home.html', {'recent': recent})

def job_list(request):
    jobs = Job.objects.order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def job_create(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_employer:
        messages.error(request, "Only employers can post jobs.")
        return redirect('home')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = profile
            job.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'jobs/job_create.html', {'form': form})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    profile = Profile.objects.get(user=request.user)
    if profile.is_employer:
        messages.error(request, "Employers cannot apply to jobs.")
        return redirect('home')
    existing = Application.objects.filter(job=job, seeker=profile).first()
    if existing:
        messages.info(request, "You have already applied.")
        return redirect('job_detail', pk=pk)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.seeker = profile
            # if seeker has profile resume and didn't upload, keep it blank and use profile.resume
            if not app.resume and profile.resume:
                app.resume = profile.resume
            app.save()
            messages.success(request, "Applied successfully.")
            return redirect('seeker_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if not profile.is_employer:
        messages.error(request, "Access denied.")
        return redirect('home')
    jobs = Job.objects.filter(employer=profile)
    applications = Application.objects.filter(job__in=jobs).order_by('-applied_at')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs, 'applications': applications})

@login_required
def seeker_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    if profile.is_employer:
        messages.error(request, "Access denied.")
        return redirect('home')
    apps = Application.objects.filter(seeker=profile)
    return render(request, 'jobs/seeker_dashboard.html', {'applications': apps})

@login_required
def shortlist_application(request, app_id):
    profile = Profile.objects.get(user=request.user)
    app = get_object_or_404(Application, id=app_id)
    if not profile.is_employer or app.job.employer != profile:
        messages.error(request, "Not allowed")
        return redirect('home')
    app.status = 'shortlisted'
    app.save()
    messages.success(request, "Application shortlisted.")
    return redirect('employer_dashboard')

@login_required
def schedule_interview(request, app_id):
    profile = Profile.objects.get(user=request.user)
    app = get_object_or_404(Application, id=app_id)
    if not profile.is_employer or app.job.employer != profile:
        messages.error(request, "Not allowed")
        return redirect('home')
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = app
            interview.save()
            app.status = 'interview_scheduled'
            app.save()
            messages.success(request, "Interview scheduled.")
            return redirect('employer_dashboard')
    else:
        form = InterviewForm()
    return render(request, 'jobs/interview_schedule.html', {'form': form, 'application': app})

