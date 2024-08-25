from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from companies.views import companies_home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', companies_home_page, name='companies_home_page'),
    path('signup/', views.signup_page, name='signup_page'),
    path('companies/', include('companies.urls')),
    
    #re_path(r"^$|^/$|^home/$", include('companies.urls')),
]
