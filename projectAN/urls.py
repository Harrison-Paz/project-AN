"""
URL configuration for projectAN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('subir/', views.subirDataset, name='subirDataset'),
    path('ver/', views.verDataset, name='verDataset'),
    path('comportamiento/probabilidad', views.prob_comp, name='prob_comp'),
    path('comportamiento/entrenar', views.comp_entrenar, name='comp_entrenar'),
    path('comportamiento/prediccion', views.predecir_comp, name='predecir_comp'),
    path('comportamiento/grafico', views.grafico_comp, name='grafico_comp'),
    path('rendimiento/probabilidad', views.prob_rend, name='prob_rend'),
    path('rendimiento/entrenar', views.rend_entrenar, name='rend_entrenar'), 
    path('rendimiento/prediccion', views.predecir_rend, name='predecir_rend'),
    path('rendimiento/grafico', views.grafico_rend, name='grafico_rend'),
    path('retiro/probabilidad', views.prob_ret, name='prob_ret'),
    path('retiro/entrenar', views.ret_entrenar, name='ret_entrenar'),
    path('retiro/prediccion', views.predecir_ret, name='predecir_ret'),
    path('retiro/grafico', views.grafico_ret, name='grafico_ret'),
]
