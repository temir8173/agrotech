from django.urls import path
from base_front import views


urlpatterns = [
    path('', views.index),
    path('investment-areas', views.investment_areas, name='investment_areas'),
    path('events', views.events),
    path('event/<int:event_id>/', views.event_view, name='event_view'),
    path('projects', views.projects),
    path('project/<int:project_id>/', views.project, name='project_view'),
    path('services', views.services),

    path('change-language/<str:language_code>/', views.change_language, name='change_language'),
]
