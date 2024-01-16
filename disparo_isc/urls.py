from django.urls import path
from disparo_isc import views

app_name = 'disparo_isc'
urlpatterns = [
    path('', views.home, name='home'),
    
    path('envio_pesquisa/', views.envio_pesquisa, name='envio_pesquisa'),


]