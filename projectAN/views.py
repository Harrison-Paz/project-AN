from django.shortcuts import render
from django.conf import settings
from .scripts import conversor, scripts
import json

from .static.dataset.leyenda import mapeo_NUCLEO_FAMILIAR, mapeo_SEXO, mapeo_ZONA, mapeo_TIPO, mapeo_SEGURO, mapeo_NIVEL
from .scripts.scripts import mapeo_CONDUCTA_INAPROPIADA, categorizar_nota, mapeo_NOTA, mapeo_RETIRO

import os
import shutil
import csv
import pandas as pd

ruta_csv = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset.csv')
ruta_csv_conv = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-conv.csv')
ruta_csv_ret = os.path.join(settings.STATIC_DIR, 'dataset', 'dataset-ret.csv')

modelo_comp = None
modelo_ret = None
modelo_rend = None

modelo_comp_pres = ""
modelo_ret_pres = ""
modelo_rend_pres = ""

modelo_comp_list = []
modelo_ret_list = []
modelo_rend_list = []

modelo_comp_res = ""
modelo_ret_res = ""
modelo_rend_res = ""

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

def prob_comp(request):
    global ruta_csv
    acc, lista = scripts.get_prob_comp(ruta_csv)
    for row in lista:
        row['Importancia'] *= 100
    chart_data = json.dumps({
        'labels': list(map(lambda x: x['Columna'], lista))[:15],
        'data': list(map(lambda x: x['Importancia'], lista))[:15],
    })

    print(chart_data)
    context = {'acc': acc, 'list': lista, 'chart_data': chart_data}

    return render(request, 'probabilidad/malcomp.html', context=context)

def prob_ret(request):
    global ruta_csv_ret
    acc, lista = scripts.get_prob_ret(ruta_csv_ret)
    for row in lista:
        row['Importancia'] *= 100
    chart_data = json.dumps({
        'labels': list(map(lambda x: x['Columna'], lista))[:15],
        'data': list(map(lambda x: x['Importancia'], lista))[:15],
    })

    print(chart_data)
    context = {'acc': acc, 'list': lista, 'chart_data': chart_data}

    return render(request, 'probabilidad/ret.html', context=context)

def prob_rend(request):
    global ruta_csv
    acc, lista = scripts.get_prob_rend(ruta_csv)
    for row in lista:
        row['Importancia'] *= 100
    chart_data = json.dumps({
        'labels': list(map(lambda x: x['Columna'], lista))[:15],
        'data': list(map(lambda x: x['Importancia'], lista))[:15],
    })
    context = {'acc': acc, 'list': lista, 'chart_data': chart_data}
    return render(request, 'probabilidad/nota.html', context=context)

def comp_entrenar(request):
    global modelo_comp, modelo_comp_list, modelo_comp_pres
    items = [
            'NUCLEO_FAMILIAR',
            'EDAD',
            'SEXO',
            'ZONA',
            'NOTA',
            'TIPO',
            'SEGURO',
            'RETRASOS',
            'NIVEL'
        ]
    target = 'CONDUCTA_INAPROPIADA'
    if request.method == 'POST':
        selected_items = request.POST.getlist('items_checkbox')
        modelo, valor = scripts.entrenar_naives(ruta_csv, selected_items, target)
        accuracy = "{:.2f}%".format(valor * 100)
        modelo_comp = modelo
        modelo_comp_list = selected_items
        modelo_comp_pres = accuracy

    return render(request, 'entrenar/malcomp.html', {'accuracy': modelo_comp_pres, 'items': items, 'selected': modelo_comp_list})

def ret_entrenar(request):
    global modelo_ret, modelo_ret_list, modelo_ret_pres
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
    target = 'RETIRO'
    if request.method == 'POST':
        selected_items = request.POST.getlist('items_checkbox')
        modelo, valor = scripts.entrenar_naives_ret(ruta_csv_ret, selected_items, target)
        accuracy = "{:.2f}%".format(valor * 100)
        modelo_ret = modelo
        modelo_ret_list = selected_items
        modelo_ret_pres = accuracy
    
    return render(request, 'entrenar/ret.html', {'accuracy': modelo_ret_pres, 'items': items, 'selected': modelo_ret_list})


def rend_entrenar(request):
    global modelo_rend, modelo_rend_list, modelo_rend_pres
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
    target = 'NOTA'
    if request.method == 'POST':
        selected_items = request.POST.getlist('items_checkbox')
        modelo, valor = scripts.entrenar_regresor(ruta_csv, selected_items, target)
        error = "{:.2f}".format(valor)
        modelo_rend = modelo
        modelo_rend_list = selected_items
        modelo_rend_pres = error

    return render(request, 'entrenar/rend.html', {'error': modelo_rend_pres, 'items': items, 'selected': modelo_rend_list})

def predecir_comp(request):
    global modelo_comp_list, modelo_comp, modelo_comp_res

    if (modelo_comp == None):
        return render(request, 'error.html')

    context = {
        'map_NUCLEO_FAMILIAR': mapeo_NUCLEO_FAMILIAR,
        'map_SEXO': mapeo_SEXO,
        'map_ZONA': mapeo_ZONA,
        'map_TIPO': mapeo_TIPO,
        'map_SEGURO': mapeo_SEGURO,
        'map_NIVEL': mapeo_NIVEL,
        'map_CONDUCTA_INAPROPIADA': mapeo_CONDUCTA_INAPROPIADA,
        'lista_campos': modelo_comp_list,
        'resultado': modelo_comp_res
    }

    if request.method == 'POST':
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

        if 'NUCLEO_FAMILIAR' in modelo_comp_list:
            data['NUCLEO_FAMILIAR'] = nucleo_familiar
        if 'EDAD' in modelo_comp_list:
            data['EDAD'] = edad
        if 'SEXO' in modelo_comp_list:
            data['SEXO'] = sexo
        if 'ZONA' in modelo_comp_list:
            data['ZONA'] = zona
        if 'NOTA' in modelo_comp_list:
            data['NOTA'] = nota
        if 'TIPO' in modelo_comp_list:
            data['TIPO'] = tipo
        if 'SEGURO' in modelo_comp_list:
            data['SEGURO'] = seguro
        if 'RETRASOS' in modelo_comp_list:
            data['RETRASOS'] = retrasos
        if 'NIVEL' in modelo_comp_list:
            data['NIVEL'] = nivel

        prediction = modelo_comp.predict(pd.DataFrame(data, index=[0]))

        invertedMap = {v: k for k, v in mapeo_CONDUCTA_INAPROPIADA.items()}
        conv_prediction = invertedMap[prediction[0]]

        context['resultado'] = conv_prediction

    return render(request, 'predecir/malcomp.html', context=context)

def predecir_ret(request):
    global modelo_ret_list, modelo_ret, modelo_ret_res

    if (modelo_ret == None):
        return render(request, 'error.html')

    context = {
        'map_NUCLEO_FAMILIAR': mapeo_NUCLEO_FAMILIAR,
        'map_SEXO': mapeo_SEXO,
        'map_ZONA': mapeo_ZONA,
        'map_TIPO': mapeo_TIPO,
        'map_SEGURO': mapeo_SEGURO,
        'map_NIVEL': mapeo_NIVEL,
        'map_CONDUCTA_INAPROPIADA': mapeo_CONDUCTA_INAPROPIADA,
        'lista_campos': modelo_ret_list,
        'resultado': modelo_ret_res
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

        if 'NUCLEO_FAMILIAR' in modelo_ret_list:
            data['NUCLEO_FAMILIAR'] = nucleo_familiar
        if 'EDAD' in modelo_ret_list:
            data['EDAD'] = edad
        if 'SEXO' in modelo_ret_list:
            data['SEXO'] = sexo
        if 'ZONA' in modelo_ret_list:
            data['ZONA'] = zona
        if 'NOTA' in modelo_ret_list:
            data['NOTA'] = nota
        if 'CONDUCTA_INAPROPIADA' in modelo_ret_list:
            data['CONDUCTA_INAPROPIADA'] = conducta
        if 'TIPO' in modelo_ret_list:
            data['TIPO'] = tipo
        if 'SEGURO' in modelo_ret_list:
            data['SEGURO'] = seguro
        if 'RETRASOS' in modelo_ret_list:
            data['RETRASOS'] = retrasos
        if 'NIVEL' in modelo_ret_list:
            data['NIVEL'] = nivel

        prediction = modelo_ret.predict(pd.DataFrame(data, index=[0]))

        invertedMap = {v: k for k, v in mapeo_RETIRO.items()}
        conv_prediction = invertedMap[prediction[0]]

        context['resultado'] = conv_prediction

    return render(request, 'predecir/ret.html', context=context)

def predecir_rend(request):
    global modelo_rend_list, modelo_rend, modelo_rend_res

    if (modelo_rend == None):
        return render(request, 'error.html')

    context = {
        'map_NUCLEO_FAMILIAR': mapeo_NUCLEO_FAMILIAR,
        'map_SEXO': mapeo_SEXO,
        'map_ZONA': mapeo_ZONA,
        'map_TIPO': mapeo_TIPO,
        'map_SEGURO': mapeo_SEGURO,
        'map_NIVEL': mapeo_NIVEL,
        'map_CONDUCTA_INAPROPIADA': mapeo_CONDUCTA_INAPROPIADA,
        'lista_campos': modelo_rend_list,
        'resultado': modelo_rend_res,
        'porcetaje_resultado': modelo_rend_res*5
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

        if 'NUCLEO_FAMILIAR' in modelo_rend_list and nucleo_familiar:
            data['NUCLEO_FAMILIAR'] = nucleo_familiar
        if 'EDAD' in modelo_rend_list:
            data['EDAD'] = edad
        if 'SEXO' in modelo_rend_list:
            data['SEXO'] = sexo
        if 'ZONA' in modelo_rend_list:
            data['ZONA'] = zona
        if 'CONDUCTA_INAPROPIADA' in modelo_rend_list and conducta_inapropiada:
            data['CONDUCTA_INAPROPIADA'] = conducta_inapropiada
        if 'TIPO' in modelo_rend_list:
            data['TIPO'] = tipo
        if 'SEGURO' in modelo_rend_list:
            data['SEGURO'] = seguro
        if 'RETRASOS' in modelo_rend_list:
            data['RETRASOS'] = retrasos
        if 'NIVEL' in modelo_rend_list:
            data['NIVEL'] = nivel

        prediction = modelo_rend.predict(pd.DataFrame(data, index=[0]))
        conv_prediction = prediction[0]

        conv_prediction = "{:.2f}".format(conv_prediction)

        modelo_rend_res = conv_prediction

        context['resultado'] = conv_prediction
        context['porcetaje_resultado'] = prediction[0]*5

    return render(request, 'predecir/rend.html', context=context)

def grafico_comp(request):
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
        promedio = data.groupby(titulo)['CONDUCTA_INAPROPIADA'].mean().reset_index()
        promedio.rename(columns={titulo: 'label', 'CONDUCTA_INAPROPIADA': 'cantidad'}, inplace=True)
        arreglo = promedio.to_dict(orient='records')
        chart_data = json.dumps({
            'labels': list(map(lambda x: x['label'], arreglo)),
            'data': list(map(lambda x: x['cantidad'], arreglo)),
        })

        context['chart_data'] = chart_data
        context['titulo'] = titulo

    return render(request, 'grafico/malcomp.html', context=context)

def grafico_ret(request):
    global ruta_csv_ret

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

    data = pd.read_csv(ruta_csv_ret)

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

    return render(request, 'grafico/ret.html', context=context)

def grafico_rend(request):
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

    return render(request, 'grafico/rend.html', context=context)