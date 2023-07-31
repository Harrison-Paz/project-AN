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
from .views import main, comportamiento, retiro, rendimiento

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', main.index, name="index"),
    path('subir/', main.subirDataset, name='subirDataset'),
    path('ver/', main.verDataset, name='verDataset'),

    path('comportamiento/media', comportamiento.view_media_comportamiento, name='comportamiento_media'),
    path('comportamiento/relacion', comportamiento.view_relacion_comportamiento, name='comportamiento_relacion'),
    path('comportamiento/entrenar', comportamiento.view_entrenar_comportamiento, name='comportamiento_entrenar'),
    path('comportamiento/predecir', comportamiento.view_predecir_comportamiento, name='comportamiento_predecir'),

    path('retiro/media', retiro.view_media_retiro, name='retiro_media'),
    path('retiro/relacion', retiro.view_relacion_retiro, name='retiro_relacion'),
    path('retiro/entrenar', retiro.view_entrenar_retiro, name='retiro_entrenar'),
    path('retiro/predecir', retiro.view_predecir_retiro, name='retiro_predecir'),

    path('rendimiento/media', rendimiento.view_media_rendimiento, name='rendimiento_media'),
    path('rendimiento/relacion', rendimiento.view_relacion_rendimiento, name='rendimiento_relacion'),
    path('rendimiento/entrenar', rendimiento.view_entrenar_rendimiento, name='rendimiento_entrenar'),
    path('rendimiento/predecir', rendimiento.view_predecir_rendimiento, name='rendimiento_predecir'),
]
