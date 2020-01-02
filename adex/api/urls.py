from django.urls import path

from . import views

urlpatterns = [

    # ex: /adex/
    # path('', views.DataSourceListViewAPI.as_view()),

    # ex: /adex/datasources/
    path('datasources/', views.DataSourceListViewAPI.as_view()),

    # ex: /adex/datasources/5/
    path('datasources/<int:pk>/', views.DataSourceDetailsViewAPI.as_view()),

    ]

