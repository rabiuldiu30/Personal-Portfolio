from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile, Education, Experience, Skill, Project, ContactMessage
from .forms import (LoginForm, RegistrationForm, ContactForm, ProfileForm,
                    EducationForm, ExperienceForm, SkillForm, ProjectForm)


def get_or_create_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'full_name': user.username, 'email': user.email})
    return profile


# ── SPA Shell ────────────────────────────────────────────────────────────────

def spa(request):
    """Single Page Application shell — loads everything once."""
    try:
        admin = User.objects.get(username='admin')
        profile = Profile.objects.get(user=admin)
        projects = Project.objects.filter(profile=profile)
        skills = Skill.objects.filter(profile=profile)
        educations = Education.objects.filter(profile=profile)
        experiences = Experience.objects.filter(profile=profile)
    except (User.DoesNotExist, Profile.DoesNotExist):
        profile = projects = skills = educations = experiences = None

    return render(request, 'portfolio/spa.html', {
        'profile': profile,
        'projects': projects,
        'skills': skills,
        'educations': educations,
        'experiences': experiences,
    })

# Keep old URL aliases so /about/, /projects/ etc redirect to SPA
def home(request):        return redirect('/')
def about_view(request):  return redirect('/')
def projects_view(request): return redirect('/')
def contact_view(request):  return redirect('/')
def resume_view(request):   return redirect('/')


# ── Auth Views ────────────────────────────────────────────────────────────────

def login_view(request):
    from django.shortcuts import redirect
    return redirect('/admin/')

def register_view(request):
    from django.shortcuts import redirect
    return redirect('/admin/')

def logout_view(request):
    logout(request)
    return redirect('/')


# ── Dashboard Views ───────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    profile = get_or_create_profile(request.user)
    educations = Education.objects.filter(profile=profile)
    experiences = Experience.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)
    projects = Project.objects.filter(profile=profile)
    messages_list = ContactMessage.objects.all() if request.user.is_staff else []
    unread_count = ContactMessage.objects.filter(is_read=False).count() if request.user.is_staff else 0
    return render(request, 'portfolio/dashboard.html', {
        'profile': profile, 'educations': educations,
        'experiences': experiences, 'skills': skills,
        'projects': projects, 'messages_list': messages_list,
        'unread_count': unread_count
    })


@login_required
def edit_profile(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('/dashboard/')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'portfolio/edit_profile.html', {'form': form})


@login_required
def add_education(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False); edu.profile = profile; edu.save()
            messages.success(request, 'Education added!')
            return redirect('/dashboard/')
    else:
        form = EducationForm()
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Add Education'})

@login_required
def edit_education(request, pk):
    profile = get_or_create_profile(request.user)
    edu = get_object_or_404(Education, pk=pk, profile=profile)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=edu)
        if form.is_valid():
            form.save(); messages.success(request, 'Education updated!')
            return redirect('/dashboard/')
    else:
        form = EducationForm(instance=edu)
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Edit Education'})

@login_required
def delete_education(request, pk):
    edu = get_object_or_404(Education, pk=pk, profile=get_or_create_profile(request.user))
    edu.delete(); messages.success(request, 'Education removed.')
    return redirect('/dashboard/')

@login_required
def add_experience(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False); exp.profile = profile; exp.save()
            messages.success(request, 'Experience added!')
            return redirect('/dashboard/')
    else:
        form = ExperienceForm()
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Add Experience'})

@login_required
def edit_experience(request, pk):
    profile = get_or_create_profile(request.user)
    exp = get_object_or_404(Experience, pk=pk, profile=profile)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save(); messages.success(request, 'Experience updated!')
            return redirect('/dashboard/')
    else:
        form = ExperienceForm(instance=exp)
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Edit Experience'})

@login_required
def delete_experience(request, pk):
    exp = get_object_or_404(Experience, pk=pk, profile=get_or_create_profile(request.user))
    exp.delete(); messages.success(request, 'Experience removed.')
    return redirect('/dashboard/')

@login_required
def add_skill(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False); s.profile = profile; s.save()
            messages.success(request, 'Skill added!')
            return redirect('/dashboard/')
    else:
        form = SkillForm()
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Add Skill'})

@login_required
def delete_skill(request, pk):
    skill = get_object_or_404(Skill, pk=pk, profile=get_or_create_profile(request.user))
    skill.delete(); messages.success(request, 'Skill removed.')
    return redirect('/dashboard/')

@login_required
def add_project(request):
    profile = get_or_create_profile(request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False); p.profile = profile; p.save()
            messages.success(request, 'Project added!')
            return redirect('/dashboard/')
    else:
        form = ProjectForm()
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Add Project'})

@login_required
def edit_project(request, pk):
    profile = get_or_create_profile(request.user)
    proj = get_object_or_404(Project, pk=pk, profile=profile)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=proj)
        if form.is_valid():
            form.save(); messages.success(request, 'Project updated!')
            return redirect('/dashboard/')
    else:
        form = ProjectForm(instance=proj)
    return render(request, 'portfolio/form_page.html', {'form': form, 'title': 'Edit Project'})

@login_required
def delete_project(request, pk):
    proj = get_object_or_404(Project, pk=pk, profile=get_or_create_profile(request.user))
    proj.delete(); messages.success(request, 'Project removed.')
    return redirect('/dashboard/')

@login_required
def mark_message_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = True; msg.save()
    return redirect('/dashboard/')


# ── Contact POST (AJAX) ───────────────────────────────────────────────────────
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST as _require_POST

def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'ok': True})
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)
    return JsonResponse({'ok': False}, status=405)


# ── AI Proxy ──────────────────────────────────────────────────────────────────
import json as _json
import urllib.request
import urllib.error
from django.conf import settings

@csrf_exempt
@_require_POST
def ai_proxy(request):
    try:
        body = _json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
    if not api_key:
        return JsonResponse({'content': [{'type': 'text', 'text': "RAB.AI is ready! Set ANTHROPIC_API_KEY in your environment to enable live responses. Get a key at console.anthropic.com."}]})

    payload = _json.dumps({
        'model': 'claude-haiku-4-5-20251001',
        'max_tokens': 500,
        'system': body.get('system', ''),
        'messages': body.get('messages', []),
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={'Content-Type': 'application/json', 'x-api-key': api_key, 'anthropic-version': '2023-06-01'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return JsonResponse(_json.loads(resp.read()))
    except urllib.error.HTTPError as e:
        return JsonResponse({'error': e.read().decode()}, status=e.code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
