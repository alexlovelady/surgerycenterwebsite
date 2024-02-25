from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedbacklist/', views.feedback_list, name='feedback_list'),
    path('feedback/delete/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),
    path('admin/', views.admin_page, name='admin_page'),
    path('user_management/', views.user_management, name='user_management'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('activity-log/', views.activity_log_page, name='activity_log_page'),
    path('analytics/', views.analytics_page, name='analytics'),
    path('calendar/', views.calendar_view, name='calendar'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
