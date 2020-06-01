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
from .models import User
from django.http import HttpResponseRedirect, Http404
from django.forms.utils import ErrorList
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse


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


# 회원가입 약관동의
@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'users/agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            return redirect('/users/register/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'users/agreement.html')


# 회원가입 
class RegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False

        url = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated:
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입을 축하드립니다.")
        return settings.LOGIN_URL

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())


# 계정프로필
def profile_view(request):
    pass