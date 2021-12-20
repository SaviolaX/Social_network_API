from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.api.urls')),
    path('api/', include('posts.api.urls')),
    path('api/', include('analitics.api.urls')),

    path('api/docs/', include_docs_urls(title='Social Network API')),
]
