from django.shortcuts import render
from django.conf import settings

from ..scripts.rendimiento import relacion_rendimiento, entrenar_rendimiento
from ..scripts.utils.mapeo import mapeo_CONDUCTA_INAPROPIADA

from ..static.dataset.leyenda import mapeo_NIVEL, mapeo_NUCLEO_FAMILIAR, mapeo_SEGURO, mapeo_SEXO, mapeo_TIPO, mapeo_ZONA

import os
import pandas as pd
import json

ruta_csv = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset.csv')


modelo_rendimiento = None
modelo_rendimiento_presicion = ""
modelo_rendimiento_lista = []
modelo_rendimiento_resultado = ""

def view_media_rendimiento(request):
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
        promedio = data.groupby(titulo)['NOTA'].mean().reset_index()
        promedio.rename(columns={titulo: 'label', 'NOTA': 'cantidad'}, inplace=True)
        arreglo = promedio.to_dict(orient='records')

        chart_data = json.dumps({
            'labels': list(map(lambda x: x['label'], arreglo)),
            'data': list(map(lambda x: x['cantidad'], arreglo)),
        })

        context['chart_data'] = chart_data
        context['titulo'] = titulo

    return render(request, 'rendimiento/media.html', context=context)
    
def view_relacion_rendimiento(request):
    global ruta_csv
    acc, lista = relacion_rendimiento(ruta_csv)
    for row in lista:
        row['Importancia'] *= 100
    chart_data = json.dumps({
        'labels': list(map(lambda x: x['Columna'], lista))[:15],
        'data': list(map(lambda x: x['Importancia'], lista))[:15],
    })
    context = {'acc': acc, 'list': lista, 'chart_data': chart_data}
    return render(request, 'rendimiento/relacion.html', context=context)

def view_entrenar_rendimiento(request):
    global modelo_rendimiento, modelo_rendimiento_lista, modelo_rendimiento_presicion
    items = [
            'NUCLEO_FAMILIAR',
            'EDAD',
            'SEXO',
            'ZONA',
            'CONDUCTA_INAPROPIADA',
            'TIPO',
            'SEGURO',
            'RETRASOS',
            'NIVEL'
        ]
    if request.method == 'POST':
        selected_items = request.POST.getlist('items_checkbox')
        modelo, valor = entrenar_rendimiento(ruta_csv, selected_items)
        error = "{:.2f}".format(valor)
        modelo_rendimiento = modelo
        modelo_rendimiento_lista = selected_items
        modelo_rendimiento_presicion = error

    context = {
        'error': modelo_rendimiento_presicion, 
        'items': items, 
        'selected': modelo_rendimiento_lista
    }

    return render(request, 'rendimiento/entrenar.html', context=context)

def view_predecir_rendimiento(request):
    global modelo_rendimiento, modelo_rendimiento_lista, modelo_rendimiento_resultado

    if (modelo_rendimiento == None):
        return render(request, 'error.html')

    context = {
        'map_NUCLEO_FAMILIAR': mapeo_NUCLEO_FAMILIAR,
        'map_SEXO': mapeo_SEXO,
        'map_ZONA': mapeo_ZONA,
        'map_TIPO': mapeo_TIPO,
        'map_SEGURO': mapeo_SEGURO,
        'map_NIVEL': mapeo_NIVEL,
        'map_CONDUCTA_INAPROPIADA': mapeo_CONDUCTA_INAPROPIADA,
        'lista_campos': modelo_rendimiento_lista,
        'resultado': modelo_rendimiento_resultado,
        'porcetaje_resultado': modelo_rendimiento_resultado*5
    }

    if request.method == 'POST':
        nucleo_familiar = request.POST.get('NUCLEO_FAMILIAR')
        edad = request.POST.get('EDAD')
        sexo = request.POST.get('SEXO')
        zona = request.POST.get('ZONA')
        conducta_inapropiada = request.POST.get('CONDUCTA_INAPROPIADA')
        tipo = request.POST.get('TIPO')
        seguro = request.POST.get('SEGURO')
        retrasos = request.POST.get('RETRASOS')
        nivel = request.POST.get('NIVEL')

        data = {}

        if 'NUCLEO_FAMILIAR' in modelo_rendimiento_lista and nucleo_familiar:
            data['NUCLEO_FAMILIAR'] = nucleo_familiar
        if 'EDAD' in modelo_rendimiento_lista:
            data['EDAD'] = edad
        if 'SEXO' in modelo_rendimiento_lista:
            data['SEXO'] = sexo
        if 'ZONA' in modelo_rendimiento_lista:
            data['ZONA'] = zona
        if 'CONDUCTA_INAPROPIADA' in modelo_rendimiento_lista and conducta_inapropiada:
            data['CONDUCTA_INAPROPIADA'] = conducta_inapropiada
        if 'TIPO' in modelo_rendimiento_lista:
            data['TIPO'] = tipo
        if 'SEGURO' in modelo_rendimiento_lista:
            data['SEGURO'] = seguro
        if 'RETRASOS' in modelo_rendimiento_lista:
            data['RETRASOS'] = retrasos
        if 'NIVEL' in modelo_rendimiento_lista:
            data['NIVEL'] = nivel

        prediction = modelo_rendimiento.predict(pd.DataFrame(data, index=[0]))
        conv_prediction = prediction[0]

        conv_prediction = "{:.2f}".format(conv_prediction)

        modelo_rendimiento_resultado = conv_prediction

        context['resultado'] = conv_prediction
        context['porcetaje_resultado'] = prediction[0]*5

    return render(request, 'rendimiento/predecir.html', context=context)
