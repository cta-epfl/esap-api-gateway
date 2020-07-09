from django.urls import path

from . import views

urlpatterns = [

    # ex: /esap/query
    path('', views.IndexView.as_view(), name='index-view'),

    #--- REST API: collections and documents ---

    path('archives', views.ArchiveListViewAPI.as_view(), name='archive-view'),
    path('archives/<int:pk>/', views.ArchiveDetailsViewAPI.as_view(), name='archive-detail'),
    path('archives-uri/', views.ArchiveListUriViewAPI.as_view(), name='archive-uri-view'),
    path('archives-uri/<int:pk>/', views.ArchiveDetailsUriViewAPI.as_view(), name='archive-uri-detail'),

    path('datasets', views.DataSetListViewAPI.as_view(), name='dataset-view'),
    path('datasets/<int:pk>/', views.DataSetDetailsViewAPI.as_view(), name='dataset-detail'),
    path('datasets-uri/', views.DataSetListUriViewAPI.as_view(), name='dataset-uri-view'),
    path('datasets-uri/<int:pk>/', views.DataSetDetailsUriViewAPI.as_view(), name='dataset-uri-detail'),

    path('catalogs', views.CatalogListViewAPI.as_view(), name='catalog-view'),
    path('catalogs/<int:pk>/', views.CatalogDetailsViewAPI.as_view(), name='catalog-detail'),


#    path('catalog-services/', views.CatalogServicesListViewAPI.as_view(), name='catalog-services-view'),
#    path('catalog-services/<int:pk>/', views.CatalogServicesDetailsViewAPI.as_view(), name='catalogservice-detail'),
    path('parameter-mapping', views.ParameterMappingListViewAPI.as_view(), name='parameter-mapping-view'),
    path('parameter-mapping/<int:pk>/', views.ParameterMappingDetailsViewAPI.as_view(), name='parametermapping-detail'),

    path('configuration', views.ConfigurationView, name='configuration-view'),

    #--- REST API: controllers ---

    # example: /esap-api/query/?target=M51&archive_uri=astron_vo
    path('create-query/', views.CreateQueryView.as_view(), name='create-query-view'),

    # example: /esap-api/run-query?dataset=ivoa.obscore&query=https://vo.astron.nl/__system__/tap/run/tap/sync?lang=ADQL&REQUEST=doQuery&QUERY=SELECT TOP 10 * from ivoa.obscore where obs_title='TGSSADR_R01D36_5x5'
    path('run-query/', views.RunQueryView.as_view(), name='run-query-view'),

    # example: /esap-api/query?level=raw&category=imaging&ra=342.16&dec=33.94&fov=10&archive_uri=apertif
    path('query/', views.CreateAndRunQueryView.as_view(), name='query-view'),

]

