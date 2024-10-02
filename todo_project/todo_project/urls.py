"""
URL configuration for todo_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from todo import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from todo import views as todo_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include the 'todo' app's URLs (e.g., for todo API endpoints)
    path('api/', include('todo.urls')),  

    # Include Django Allauth URLs for account management (optional, can be removed if not needed)
    path('accounts/', include('allauth.urls')),

    # Schema endpoints for API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),  # Schema JSON
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # Swagger UI
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),  # Redoc UI

    # API-based Authentication endpoints
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/register/', todo_views.RegisterView.as_view(), name='auth_register'),
    path('api/auth/forgot-password/', todo_views.ForgotPasswordView.as_view(), name='auth_forgot_password'),
    path('api/auth/reset-password/<uidb64>/<str:token>/', todo_views.ResetPasswordView.as_view(), name='auth_reset_password'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Todo management endpoints (API-based)
    path('api/todos/', todo_views.TodoListCreateView.as_view(), name='todo_list_create'),  # List/Create Todos
    path('api/todos/<int:pk>/', todo_views.TodoDetailView.as_view(), name='todo_detail'),  # Retrieve/Update/Delete Todos

    # HTML-based Authentication endpoints
    path('', todo_views.home_view, name='index'),  # Redirects to the login or dashboard
    path('register/', todo_views.register_view, name='register'),
    path('login/', todo_views.login_view, name='login'),
    path('logout/', todo_views.logout_view, name='logout'),
    path('forgot-password/', todo_views.forgot_password_view, name='forgot_password'),
    
    # HTML-based TODO management
    path('todo/', views.todo_list_view, name='todo_list'),  # TODO list view
    path('todo/create/', views.todo_create_view, name='todo_create'),  # TODO create view
    path('todo/update/<int:pk>/', views.todo_update_view, name='todo_update'),  # TODO update view
    path('todo/delete/<int:pk>/', views.todo_delete_view, name='todo_delete'),  # TODO delete view

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]


