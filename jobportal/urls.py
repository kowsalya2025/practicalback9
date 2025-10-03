"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from jobs import views as job_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', job_views.home, name='home'),
    # accounts
    path('register/', accounts_views.register, name='register'),
    path('login/', accounts_views.user_login, name='login'),
    path('logout/', accounts_views.user_logout, name='logout'),
    path('profile/', accounts_views.profile, name='profile'),
    # jobs
    path('jobs/', job_views.job_list, name='job_list'),
    path('jobs/create/', job_views.job_create, name='job_create'),
    path('jobs/<int:pk>/', job_views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/apply/', job_views.apply_job, name='apply_job'),
    path('employer/dashboard/', job_views.employer_dashboard, name='employer_dashboard'),
    path('seeker/dashboard/', job_views.seeker_dashboard, name='seeker_dashboard'),
    path('applications/<int:app_id>/shortlist/', job_views.shortlist_application, name='shortlist_application'),
    path('applications/<int:app_id>/schedule/', job_views.schedule_interview, name='schedule_interview'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

