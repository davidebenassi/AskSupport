from django.contrib import admin
from django.urls import include, path, re_path
from . import views
from companies.views import companies_home_page

from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r"^$|^/$|^home/$", companies_home_page, name='home'),   # The companies home page is renderes ad the whole site home #
    path('admin/', admin.site.urls),

    # View that let you select what kind of profile you want to create #
    path('signup/', views.signup_page, name='signup_page'),

    # Views from Django #
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path('companies/', include('companies.urls')),
    path('users/', include('users.urls')),
    path('tickets/', include('tickets.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
