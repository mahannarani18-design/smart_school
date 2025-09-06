from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

admin.site.site_header = "Moje Omid Irafshan Dormitory Management Panel"
admin.site.site_title = "Moje Omid Irafshan Management"
admin.site.index_title = "Welcome to the Management Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/dormitory/', include('dormitory.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/events/', include('events.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/feedback/', include('feedback.urls')),
    path('api/academics/', include('academics.urls')),
    path('api/alumni/', include('alumni.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)