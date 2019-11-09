from django.urls import path
from . import views
from .views import GenerateOTP, ValidateOTP

app_name = 'auth_app'
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/', views.signup, name="signup"),
    path('user_login',views.user_login,name='user_login'),
    path('generate', GenerateOTP.as_view(), name="generate"),
    path('validate', ValidateOTP.as_view(), name="validate"),
    path('searchcountry/',views.searchcountry,name='searchcountry'),
    path('searchcountry/<int:pk>/',views.CountryDetailView.as_view(),name='list'),
]
