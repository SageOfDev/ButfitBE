from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from docs.views import schema_view

# admin_site config
admin.site.site_header = 'Butfit Admin'
admin.site.site_title = 'Butfit Admin'
# admin.site.index_title = ''

api_urls = [
    path('program/', include('program.urls')),
    path('mypage/', include('mypage.urls')),
    path('booking/', include('booking.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(api_urls)),

    # drf browsable API login
    path('api-auth/', include('rest_framework.urls')),

    # api_docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
         # debug_toolbar
        path('__debug__/', include(debug_toolbar.urls)),
    ]
