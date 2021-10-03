# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
#import packages and modules
from django.urls import path, re_path
from apps.app import views
# basic URLs
urlpatterns = [

    # The home page
    # path('index/', views.index, name='home'),
    path('index/', views.ClubChartView.as_view(), name='home'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
