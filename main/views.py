# -*- coding: utf-8 -*-
import re
from django.db import connection
from django.shortcuts import render
from gtts import gTTS
from pydub import AudioSegment
import os
import latex2mathml.converter

# Falta corregir orden en el código.
from asemi import settings


def index(request):
    # Si llega el método post.
    if request.POST:
        if request.POST.get('latex_form', False): # Si llega post para convertir
            name_record = "last_record.mp3"
            final_name = "last_record.ogg"
            # Convierte la ecuación latex a mathml
            mathml_output = latex2mathml.converter.convert(request.POST['latex_form'])
            matches_list = find_matches(request.POST['latex_form'])
            tts_str = ""
            if len(matches_list) > 0:
                for m in matches_list:
                    tts_str += search_string_db(m)
            else:
                tts_str = request.POST['latex_form']
            print(tts_str)
            print('racc' in tts_str)
            if 'frac' in request.POST['latex_form']:
                tts_str = tts_str.replace('}{', ' sobre ')
            print(tts_str)
            # Genera el código para generar el audio de lectura.
            text = gTTS(text=tts_str, lang='es')
            # Borra los archivos anteriores
            try:
                os.remove("/opt/asemi/asemi/static/"+name_record)
            except:
                pass
            #Obtiene fecha para el nombre del archivo
            text.save("/opt/asemi/asemi/static/"+name_record)
            # Convierte el audio
            convert_audio("/opt/asemi/asemi/static/"+name_record, "/opt/asemi/asemi/static/"+final_name)
            return render(request, 'main/index.html', {"mathml_data": mathml_output, "latex_form": request.POST['latex_form'], "name_record": final_name})
    else:
        print("GET METHOD")
        return render(request, 'main/index.html', {})


def find_matches(text):
    regex = settings.FUNCTIONS.get("FRAC")
    matches = re.findall(regex, text)
    print("Matches")
    print(matches)
    return matches


def convert_audio(name_record, final_name):
    try:
        record = AudioSegment.from_mp3(name_record)
        record.export(final_name, format="ogg")
    except Exception as e:
        print(e)


def search_string_db(st):
    print("st")
    print(st)
    data = query_str(st)
    print("data")
    print(len(data))
    if len(data) > 0:
        for d in data:
            print(d[3])
            return d[3]
    return st


def query_str(st):
    st = format_str(st)
    query = "select * from expresiones_matematicas where expresion_latex = '%s'" % (st)
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query);
        data = cursor.fetchall()
    return data


def format_str(str):
    if str.startswith('\\'):
        return '\\'+str
    return str
