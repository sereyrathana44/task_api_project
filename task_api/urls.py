from django.contrib import admin
from django.urls import path, include
from tasks.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),             # ទំព័រដើម HTML
    path('api/', include('tasks.urls')),      # API routes ចេញពី tasks/urls.py
]