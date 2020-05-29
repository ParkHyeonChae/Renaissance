from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import login_message_required, admin_required, logout_message_required
from django.views.generic import CreateView, FormView, TemplateView, View
from .forms import RegisterForm, LoginForm


# 메인화면
def index(request):
    return render(request, 'users/index.html')


# 로그인
@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=user_id, password=password)
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)

            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
            
        return super().form_valid(form)


# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')