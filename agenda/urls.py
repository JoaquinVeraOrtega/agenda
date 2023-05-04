from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/',include('contact.urls') ),
    path('todo/',include('todo.urls') ),
    path("accounts/", include("accounts.urls")),
    path('', views.index, name="index"),
]
