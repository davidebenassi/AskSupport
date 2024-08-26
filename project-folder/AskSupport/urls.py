from django.contrib import admin
from django.urls import include, path, re_path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r"^$|^/$|^home/$", views.home, name='home'),
    path('admin/', admin.site.urls),

    # View that let you select what kind of profile you want to create #
    path('signup/', views.signup_page, name='signup_page'),

    # Views from Django #
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path('companies/', include('companies.urls')),
    path('users/', include('users.urls')),
]
