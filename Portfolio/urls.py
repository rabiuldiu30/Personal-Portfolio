from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # SPA — public site
    path('', views.spa, name='spa'),

    # Login/register removed — redirect to Django admin
    path('login/',    RedirectView.as_view(url='/admin/', permanent=False)),
    path('register/', RedirectView.as_view(url='/admin/', permanent=False)),

    # Logout still works (redirects to home)
    path('logout/', views.logout_view, name='logout'),

    # Contact AJAX
    path('api/contact/', views.contact_submit, name='contact_submit'),

    # AI Proxy
    path('api/ai/', views.ai_proxy, name='ai_proxy'),

    # Dashboard (staff only via Django admin session)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/education/add/', views.add_education, name='add_education'),
    path('dashboard/education/<int:pk>/edit/', views.edit_education, name='edit_education'),
    path('dashboard/education/<int:pk>/delete/', views.delete_education, name='delete_education'),
    path('dashboard/experience/add/', views.add_experience, name='add_experience'),
    path('dashboard/experience/<int:pk>/edit/', views.edit_experience, name='edit_experience'),
    path('dashboard/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
    path('dashboard/skill/add/', views.add_skill, name='add_skill'),
    path('dashboard/skill/<int:pk>/delete/', views.delete_skill, name='delete_skill'),
    path('dashboard/project/add/', views.add_project, name='add_project'),
    path('dashboard/project/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('dashboard/project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('dashboard/message/<int:pk>/read/', views.mark_message_read, name='mark_message_read'),
]
