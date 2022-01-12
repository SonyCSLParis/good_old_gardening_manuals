from django.urls import path

from . import views


app_name = 'manuals'

urlpatterns = [
    path('',
         views.IndexView.as_view(),
         name='index'),
    
    path('<int:pk>/',
         views.ManualView.as_view(),
         name='manual_text'),
    
    path('<int:pk>/annotations/',
         views.ManualAnnotationsView.as_view(),
         name='manual_annotations'),
    
    path('json/annotations/<str:manual>',
         views.AnnotationsJson.as_view(),
         name='annotations_json_all'),
    
    path('json/annotations/<str:manual>/<str:section>/<str:paragraph>/<str:index>',
         views.AnnotationsJson.as_view(),
         name='annotations_json'),
]
