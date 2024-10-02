from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ForgotPasswordForm, TodoForm
from .models import Todo
from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, TodoReadSerializer, TodoWriteSerializer, TodoUpdateSerializer
from .tasks import send_reset_email, send_task_created_email
from .forms import CustomUserCreationForm
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from jwt.exceptions import DecodeError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode  


def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

# Register view (HTML-based)
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'  
            login(request, user)
            return redirect('todo_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view (HTML-based)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('todo_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')


def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email=email)
            
            if users.exists():
                token_generator = PasswordResetTokenGenerator()

                for user in users:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = token_generator.make_token(user)

                    reset_link = f"http://{get_current_site(request).domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

                    send_mail(
                        subject='Password Reset Requested',
                        message=f'Click the link to reset your password: {reset_link}',
                        from_email='your-email@gmail.com',  
                        recipient_list=[email],
                        fail_silently=False,
                    )
                
                messages.success(request, 'If an account exists with that email, a reset link will be sent.')
            else:
                messages.error(request, 'No account found with that email address.')

            return redirect('login')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API-based Forgot Password view
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(email=email)
        if users.exists():
            for user in users:
                token_generator = PasswordResetTokenGenerator()
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                reset_link = f"http://localhost:8000/api/auth/reset-password/{uidb64}/{token}/"

                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link below to reset your password:\n{reset_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
        return Response({"message": "If an account with that email exists, a password reset email has been sent."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    token_generator = PasswordResetTokenGenerator()

    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and self.token_generator.check_token(user, token):
                new_password = serializer.validated_data['password']
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_user_from_token(self, uidb64, token):
        """
        Retrieve the user corresponding to the uidb64 and validate the token.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))  
            user = User.objects.get(pk=uid)  
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

        if self.token_generator.check_token(user, token):
            return user
        return None

# HTML-based TODO list view
@login_required
def todo_list_view(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo_list.html', {'todos': todos})

# HTML-based TODO create view
@login_required
def todo_create_view(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo_create.html', {'form': form})

# HTML-based TODO update view
@login_required
def todo_update_view(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo_update.html', {'form': form})

# HTML-based TODO delete view
@login_required
def todo_delete_view(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todo_confirm_delete.html', {'todo': todo})

# API-based TODO List and Create view
class TodoListCreateView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TodoReadSerializer
        return TodoWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# API-based TODO Detail view
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = TodoReadSerializer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# API-based TODO ViewSet
class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TodoReadSerializer
        elif self.action == 'create':
            return TodoWriteSerializer
        elif self.action in ['update', 'partial_update']:
            return TodoUpdateSerializer
        return TodoReadSerializer

    def perform_create(self, serializer):
        todo = serializer.save(user=self.request.user)
        send_task_created_email.delay(todo.task_name)
