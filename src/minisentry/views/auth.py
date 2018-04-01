from django.contrib.auth import views as django_views


class SignInView(django_views.LoginView):
    template_name = "signin.html"


class SignOutView(django_views.LogoutView):
    template_name = "signout.html"
