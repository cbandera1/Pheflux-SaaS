from django.urls import path
from . import views

app_name = 'Pheflux'

urlpatterns = [
    path('predict/', views.pheflux_prediction, name='pheflux_prediction'),
    path('biggsearch/', views.bigg_search, name='searchbigg'),
    path('tcgasearch/', views.tcga_search, name='searchtcga'),
    path('landing/', views.landing, name='landing_page'),
    path('', views.redirect_to_landing, name='redirect_to_landing'),
    path('help/', views.help, name='landing_page'),
]
