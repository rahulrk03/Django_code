from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from phone_login.models import PhoneToken
from phone_login.utils import user_detail
from .serializers import (PhoneTokenCreateSerializer,
                          PhoneTokenValidateSerializer)
from django.shortcuts import render
from .forms import NewUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import re
from django.db.models import Q
from . import models
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib import messages


def index(request):
    return render(request,'auth_app/base.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def signup(request):
    registered = False
    user_form = NewUserForm(request.POST or None )
    if request.method == "POST":
        if user_form.is_valid():
            user = user_form.save(commit=True)
            registered = True
            return HttpResponseRedirect('/auth_app/user_login')
    else:
        user_form=NewUserForm()

    return render(request,'auth_app/signup.html',{'user_form':user_form,'registered':registered})



def user_login(request):
        queryset = PhoneToken.objects.all()
        return render(request, 'auth_app/login.html', {})

class GenerateOTP(CreateAPIView):
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenCreateSerializer

    def post(self, request, format=None):
        # Get the patient if present or result None.
        ser = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if ser.is_valid():
            number= request.data.get('phone_number')
            q1 = models.UserProfileInfo.objects.filter(phone_number__contains = number).exists()
            print(q1)
            if q1 ==True:
                token = PhoneToken.create_otp_for_number(number)
                if token:
                    phone_token = self.serializer_class(
                        token, context={'request': request}
                    )
                    data = phone_token.data
                    if getattr(settings, 'PHONE_LOGIN_DEBUG', False):
                        data['debug'] = token.otp
                    return Response(data)
                return Response({
                    'reason': "you can not have more than {n} attempts per day, please try again tomorrow".format(
                        n=getattr(settings, 'PHONE_LOGIN_ATTEMPTS', 10))}, status=status.HTTP_403_FORBIDDEN)
            
        return Response(
            {'reason': ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ValidateOTP(CreateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = PhoneToken.objects.all()
    serializer_class = PhoneTokenValidateSerializer

    def post(self, request, format=None):
        ser = self.serializer_class(
            data=request.data, context={'request': request}
        )
        if ser.is_valid():
            phone_number = request.data.get("phone_number")
            otp = request.data.get("otp")
            try:
                criterion1 = Q(phone_number__contains=phone_number)
                criterion2 = Q(otp__contains=otp)
                q1 = models.UserProfileInfo.objects.filter(phone_number__contains = phone_number).exists()
                print(q1)
                if q1 ==True:
                    q = PhoneToken.objects.filter(criterion1 ,criterion2).exists()
                    print(criterion1)
                    print(criterion2)
                #print(q)
                    if q == True:

                        return HttpResponseRedirect('/auth_app/searchcountry')
                    return Response(
                    {'reason': "OTP doesn't exist"},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                    )
            except ObjectDoesNotExist:
                return Response(
                   {'reason': "OTP doesn't exist"},
                   status=status.HTTP_406_NOT_ACCEPTABLE
                )
        return Response(
            {'reason': ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


def searchcountry(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(name__icontains=query)
            results= models.City.objects.filter(lookups).distinct()
            sult = models.City.objects.all()
            context={'results': results,'sult':sult,
            'submitbutton': submitbutton,}
            return render(request, 'auth_app/state_list.html', context)
        else:
            return render(request, 'auth_app/state_list.html')
    else:
        return render(request, 'auth_app/state_list.html')

class CountryDetailView(DetailView):
    model = models.Country
    template_name = 'auth_app/city_list.html'
