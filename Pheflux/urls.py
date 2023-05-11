from django.urls import path
from . import views

app_name = 'Pheflux'

urlpatterns = [
    path('', views.pheflux_prediction, name='pheflux'),

]
