from django.urls import path
from base_front import views


urlpatterns = [
    path('', views.index),
    path('investment-areas', views.investment_areas, name='investment_areas'),
    path('events', views.events),
    path('event/<int:event_id>/', views.event_view, name='event_view'),
    path('projects', views.projects),
    path('project/<int:project_id>/', views.project, name='project_view'),
    path('partners', views.partners),
    path('partner/<int:partner_id>/', views.partner, name='partner_view'),
    path('farmer_training', views.farmer_training),

    path('service/consulting/', views.consulting),
    path('service/consulting/<str:slug>/', views.consulting_view, name='consulting_view'),
    path('service/<str:slug>/', views.service),

    path('store', views.store),
    path('courses/<int:category_id>/', views.courses, name='courses'),

    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
]
