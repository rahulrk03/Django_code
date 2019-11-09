from django.contrib import admin
from django.urls import path,include
from auth_app import urls
from auth_app import views
from auth_app.views import GenerateOTP

app_name='auth_app'

urlpatterns = [
    path('',views.index,name='index'),
    path('admin/', admin.site.urls),
    path('auth_app/', include('auth_app.urls'),),
    path('logout/', views.user_logout, name='logout'),
]
