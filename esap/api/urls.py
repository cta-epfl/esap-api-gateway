from django.urls import path

from . import views

urlpatterns = [

    # ex: /esap/
    path('', views.ArchiveListViewAPI.as_view(), name='archive-view'),

    path('archives/', views.ArchiveListViewAPI.as_view(), name='archive-view'),
    path('archives/<int:pk>/', views.ArchiveDetailsViewAPI.as_view(), name='archive-detail'),
    path('archives-uri/', views.ArchiveListUriViewAPI.as_view(), name='archive-uri-view'),
    path('archives-uri/<int:pk>/', views.ArchiveDetailsUriViewAPI.as_view(), name='archive-uri-detail'),

    path('datasets/', views.DataSetListViewAPI.as_view(), name='dataset-view'),
    path('datasets/<int:pk>/', views.DataSetDetailsViewAPI.as_view(), name='dataset-detail'),
    path('datasets-uri/', views.DataSetListUriViewAPI.as_view(), name='dataset-uri-view'),
    path('datasets-uri/<int:pk>/', views.DataSetDetailsUriViewAPI.as_view(), name='dataset-uri-detail'),

    path('catalogs/', views.CatalogListViewAPI.as_view(), name='catalog-view'),
    path('catalog/<int:pk>/', views.CatalogDetailsViewAPI.as_view(), name='catalog-detail'),

    path('catalog-services/', views.CatalogServicesListViewAPI.as_view(), name='catalog-services-view'),
    path('catalog-services/<int:pk>/', views.CatalogServicesDetailsViewAPI.as_view(), name='catalog-services-detail'),

]

