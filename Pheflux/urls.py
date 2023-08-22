from django.urls import path
from . import views

app_name = 'Pheflux'

urlpatterns = [
    path('', views.pheflux_prediction, name='pheflux_prediction'),
    path('biggsearch/', views.bigg_search, name='searchbigg'),
    path('tcgasearch/', views.tcga_search, name='searchtcga')
]
