from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

class Admin(LoginRequiredMixin):
    login_url = '/login/'  # URL to redirect unauthenticated users
    redirect_field_name = 'next'  # Where to redirect after successful login

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        # Check if the user is an admin
        if not getattr(request.user, 'is_admin', False):  # Default to False if `is_admin` doesn't exist
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        # Proceed with the normal request/response flow
        return super().dispatch(request, *args, **kwargs)
