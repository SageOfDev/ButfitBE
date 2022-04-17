"""ButfitBE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from docs.views import schema_view

# admin_site config
admin.site.site_header = 'Butfit Admin'
admin.site.site_title = 'Butfit Admin'
# admin.site.index_title = ''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('program/', include('program.urls')),
    path('mypage/', include('mypage.urls')),
    path('booking/', include('booking.urls')),

    # drf browsable API login
    path('api-auth/', include('rest_framework.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        # drf_yasg
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        # debug_toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]
