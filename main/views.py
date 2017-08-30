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
            name_record = "last_record%d.mp3"
            final_name = "last_record%d.ogg"
            list_final = []
            mathml_output = []
            # Listado de ecuaciones escritas.
            equa_list = request.POST['latex_form'].split('\n')
            print(equa_list)
            for index, value in enumerate(equa_list):
                # Convierte la ecuación latex a mathml
                mathml_output.append(latex2mathml.converter.convert(value))
                matches_list = find_matches(value)
                tts_str = ""
                if len(matches_list) > 0:
                    for m in matches_list:
                        tts_str += search_string_db(m)
                else:
                    tts_str = value
                print(tts_str)
                print('racc' in tts_str)
                if 'frac' in value:
                    tts_str = tts_str.replace('}{', ' sobre ')
                print(tts_str)
                # Genera el código para generar el audio de lectura.
                text = gTTS(text=tts_str, lang='es')
                # Borra los archivos anteriores
                try:
                    os.remove("main/static/" + name_record % index)
                except:
                    pass
                # Obtiene fecha para el nombre del archivo
                text.save("main/static/" + name_record % index)
                # Convierte el audio
                convert_audio(name_record % index, final_name % index)
                list_final.append(final_name % index)
            print(mathml_output)
            print(list_final)
            return render(request, 'main/index.html',
                              {"mathml_data": mathml_output, "latex_form": request.POST['latex_form'],
                               "name_record": list_final})
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
        record = AudioSegment.from_mp3("main/static/" + name_record)
        record.export("main/static/" + final_name, format="ogg")
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
