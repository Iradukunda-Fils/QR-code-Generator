from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

#PASSWORD RESET PROCESSIES
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


from django.shortcuts import redirect

class CustomLoginView(View):
    template_name = 'M-users/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True  # Custom flag

    def get(self, request):
        # Check if the user is already authenticated
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.redirect_authenticated_user_logic()

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Check if the user is already authenticated
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return self.redirect_authenticated_user_logic()

        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.is_admin:
                    return redirect('home-admin')
                elif user.is_staff:
                    messages.success(request, 'You are staff authenticated.')
                    return redirect('user-qr')
                else:
                    messages.success(request, 'You are authenticated.')
                    return redirect('user-qr')  # Default redirection for non-admin and non-staff users
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, self.template_name, {'form': form})

    def redirect_authenticated_user_logic(self):
        """Logic for redirecting authenticated users."""
        if self.request.user.is_admin:
            return redirect('home-admin')
        elif self.request.user.is_staff:
            messages.success(self.request, 'You are staff authenticated.')
            return redirect('user-qr')
        else:
            messages.success(self.request, 'You are authenticated.')
            return redirect('user-qr')


class UserRegistrationView(LoginRequiredMixin, View):
    template_name = 'M-users/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
        
    def get(self, request):
        if self.request.user.is_admin:
            form = self.form_class()    
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('user-qr')
    
    def post(self, request):
        if self.request.user.is_admin:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Optionally, you could add custom logic here, such as sending a confirmation email
                return redirect(self.success_url)
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('user-qr')


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)  # Logs out the user
        return redirect('login')
    
    
    
    
#PASSWORD RESET PROCESSIES

class CustomPasswordResetView(PasswordResetView):
    template_name = 'M-users/password-reset.html'
    email_template_name = 'M-users/password-reset-email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'M-users/password-reset-done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'M-users/password-reset-confirm.html'
    success_url = reverse_lazy('password-reset-complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'M-users/password-reset-complete.html'
    
    
    
#DOWNLOAD QR CODE

class AdminView(LoginRequiredMixin,View):
    template_name  = 'admin-page.html'
    def get(self, request):
        if self.request.user.is_admin:
            context = {
            'users': User.objects.all(),
            }
            return render(request, self.template_name,context)
        else:
            return redirect('user-qr')
    
class UsersView(LoginRequiredMixin,View):
    template_name  = 'user_qr.html'
    def get(self, request):
        return render(request, self.template_name)



from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class DownloadQRCodeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Get the user by their ID (or email, etc.)
        user = get_object_or_404(User, id=kwargs['user_id'])
        
        # Check if the user has a QR code
        if user.qr_code:
            # Serve the QR code as a download response
            response = FileResponse(user.qr_code.open('rb'), as_attachment=True, content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{user.first_name}_{user.last_name}_qr_code.png"'
            return response
        else:
            # Return a response if the QR code does not exist
            return HttpResponse("QR Code not found for this user.", status=404)
