from django.contrib import admin
from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup_page, name='signup_page'),
    path('companies/', include('companies.urls')),
    re_path(r"^$|^/$|^home/$", views.home, name='home'),
]
