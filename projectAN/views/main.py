from django.shortcuts import render
from django.conf import settings

import os
import shutil
import csv

from ..scripts.utils import conversor

ruta_csv = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset.csv')

def index(request):
    return render(request, 'index.html')

def subirDataset(request):
    if request.method == 'POST' and request.FILES['archivo']:
        archivo = request.FILES['archivo']
        with open(ruta_csv, 'wb') as destino:
            shutil.copyfileobj(archivo, destino)
        conversor.convertir(ruta_csv)
        conversor.retiro(ruta_csv)

    return render(request, 'dataset/subir.html')

def verDataset(request):
    datos_csv = []
    with open(ruta_csv, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for idx, fila in enumerate(reader):
            if idx > 21:
                break
            datos_csv.append(fila)
    return render(request, 'dataset/ver.html', {'datos': datos_csv})