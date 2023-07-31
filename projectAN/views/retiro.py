from django.shortcuts import render
from django.conf import settings

from ..scripts.retiro import relacion_retiro, entrenar_retiro
from ..scripts.utils.mapeo import mapeo_CONDUCTA_INAPROPIADA, mapeo_RETIRO

from ..static.dataset.leyenda import mapeo_NIVEL, mapeo_NUCLEO_FAMILIAR, mapeo_SEGURO, mapeo_SEXO, mapeo_TIPO, mapeo_ZONA

import os
import pandas as pd
import json

modelo_retiro = None
modelo_retiro_presicion = ""
modelo_retiro_lista = []
modelo_retiro_resultado = ""

ruta_csv = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-ret.csv')

def view_media_retiro(request):
    global ruta_csv

    items = [
        'NUCLEO_FAMILIAR',
        'EDAD',
        'SEXO',
        'ZONA',
        'TIPO',
        'SEGURO',
        'NIVEL',
    ]

    context = {
        'items': items,
        'char_data': None
    }

    data = pd.read_csv(ruta_csv)

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        promedio = data.groupby(titulo)['RETIRO'].mean().reset_index()
        promedio.rename(columns={titulo: 'label', 'RETIRO': 'cantidad'}, inplace=True)
        arreglo = promedio.to_dict(orient='records')
        chart_data = json.dumps({
            'labels': list(map(lambda x: x['label'], arreglo)),
            'data': list(map(lambda x: x['cantidad'], arreglo)),
        })

        context['chart_data'] = chart_data
        context['titulo'] = titulo

    return render(request, 'retiro/media.html', context=context)

def view_relacion_retiro(request):
    global ruta_csv
    acc, lista = relacion_retiro(ruta_csv)
    for row in lista:
        row['Importancia'] *= 100
    chart_data = json.dumps({
        'labels': list(map(lambda x: x['Columna'], lista))[:15],
        'data': list(map(lambda x: x['Importancia'], lista))[:15],
    })

    context = {'acc': acc, 'list': lista, 'chart_data': chart_data}

    return render(request, 'retiro/relacion.html', context=context)

def view_entrenar_retiro(request):
    global modelo_retiro, modelo_retiro_lista, modelo_retiro_presicion
    
    items = [
            'NUCLEO_FAMILIAR',
            'EDAD',
            'SEXO',
            'ZONA',
            'NOTA',
            'TIPO',
            'SEGURO',
            'RETRASOS',
            'NIVEL',
            'CONDUCTA_INAPROPIADA',
        ]
    
    if request.method == 'POST':
        selected_items = request.POST.getlist('items_checkbox')
        modelo, valor = entrenar_retiro(ruta_csv, selected_items)
        accuracy = "{:.2f}%".format(valor * 100)
        modelo_retiro = modelo
        modelo_retiro_lista = selected_items
        modelo_retiro_presicion = accuracy

    context = {
        'accuracy': modelo_retiro_presicion, 
        'items': items, 
        'selected': modelo_retiro_lista
    }
    
    return render(request, 'retiro/entrenar.html', context=context)

def view_predecir_retiro(request):
    global modelo_retiro, modelo_retiro_lista, modelo_retiro_resultado

    if (modelo_retiro == None):
        return render(request, 'error.html')

    context = {
        'map_NUCLEO_FAMILIAR': mapeo_NUCLEO_FAMILIAR,
        'map_SEXO': mapeo_SEXO,
        'map_ZONA': mapeo_ZONA,
        'map_TIPO': mapeo_TIPO,
        'map_SEGURO': mapeo_SEGURO,
        'map_NIVEL': mapeo_NIVEL,
        'map_CONDUCTA_INAPROPIADA': mapeo_CONDUCTA_INAPROPIADA,
        'lista_campos': modelo_retiro_lista,
        'resultado': modelo_retiro_resultado
    }

    if request.method == 'POST':
        conducta = request.POST.get('CONDUCTA_INAPROPIADA')
        nucleo_familiar = request.POST.get('NUCLEO_FAMILIAR')
        edad = request.POST.get('EDAD')
        sexo = request.POST.get('SEXO')
        zona = request.POST.get('ZONA')
        nota = request.POST.get('NOTA')
        tipo = request.POST.get('TIPO')
        seguro = request.POST.get('SEGURO')
        retrasos = request.POST.get('RETRASOS')
        nivel = request.POST.get('NIVEL')

        data = {}

        if 'NUCLEO_FAMILIAR' in modelo_retiro_lista:
            data['NUCLEO_FAMILIAR'] = nucleo_familiar
        if 'EDAD' in modelo_retiro_lista:
            data['EDAD'] = edad
        if 'SEXO' in modelo_retiro_lista:
            data['SEXO'] = sexo
        if 'ZONA' in modelo_retiro_lista:
            data['ZONA'] = zona
        if 'NOTA' in modelo_retiro_lista:
            data['NOTA'] = nota
        if 'CONDUCTA_INAPROPIADA' in modelo_retiro_lista:
            data['CONDUCTA_INAPROPIADA'] = conducta
        if 'TIPO' in modelo_retiro_lista:
            data['TIPO'] = tipo
        if 'SEGURO' in modelo_retiro_lista:
            data['SEGURO'] = seguro
        if 'RETRASOS' in modelo_retiro_lista:
            data['RETRASOS'] = retrasos
        if 'NIVEL' in modelo_retiro_lista:
            data['NIVEL'] = nivel

        prediction = modelo_retiro.predict(pd.DataFrame(data, index=[0]))

        invertedMap = {v: k for k, v in mapeo_RETIRO.items()}
        conv_prediction = invertedMap[prediction[0]]

        context['resultado'] = conv_prediction

    return render(request, 'retiro/predecir.html', context=context)

