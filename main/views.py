# -*- coding: utf-8 -*-
import ast
import re

import pdfkit
from django.db import connection
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render
from gtts import gTTS
from pydub import AudioSegment
from asemi import settings
import os
import latex2mathml.converter

# Falta corregir orden en el código.


def index(request):
    #Consulta los símbolos de la tabla de apoyo.
    query = "select * from guia_expresiones where expresion_estado = 1"
    data_symbols = query_str(query)
    print(data_symbols)

    # Si llega el método post.
    if request.POST:
        if request.POST.get('latex_form', False): # Si llega post para convertir
            try:
                ############ Variables para Producción
                name_record = "/opt/asemi/asemi/static/last_record%d.mp3"
                final_name = "/opt/asemi/asemi/static/last_record%d.ogg"
                ############ Variables para pruebas
                # name_record = "main/static/last_record%d.mp3"
                # final_name = "main/static/last_record%d.ogg"
                list_final = []
                mathml_output = []
                # Listado de ecuaciones escritas.
                equa_list = request.POST['latex_form'].split('\n')
                print(equa_list)
                num_audio = 0
                for index, value in enumerate(equa_list):
                    print(num_audio)
                    # Quita espacios que no sirven
                    # Convierte la ecuación latex a mathml
                    value = value.rstrip()
                    if value:
                        mathml_output.append(latex2mathml.converter.convert(value))
                        matches_list = find_matches(value)
                        tts_str = ""
                        if len(matches_list) > 0:
                            for m in matches_list:
                                if "\r" in m:
                                    m.replace("\r", "")
                                if m != "":
                                    tts_str += search_string_db(m)
                        else:
                            tts_str = value
                        if 'frac' in value:
                            tts_str = tts_str.replace('}{', ' sobre ')
                        # Genera el código para generar el audio de lectura.
                        text = gTTS(text=tts_str, lang='es')
                        # Borra los archivos anteriores
                        try:
                            os.remove(name_record % index)
                        except:
                            pass
                        # Obtiene fecha para el nombre del archivo
                        text.save(name_record % num_audio)
                        # Convierte el audio
                        convert_audio(name_record % num_audio, final_name % num_audio)
                        list_final.append(final_name % num_audio)
                        num_audio+=1
                print(mathml_output)
                print(list_final)
                return render(request, 'main/index.html',
                              {"mathml_data": mathml_output, "latex_form": request.POST['latex_form'],
                               "name_record": list_final, "data_symbols": data_symbols})
            except Exception as e:
                print(e)
                return render(request, 'main/index.html',
                              {"mathml_data": "", "latex_form": request.POST.get('latex_form', ""),
                               "name_record": "", "data_symbols": data_symbols})
        else:
            print("GET METHOD")
            return render(request, 'main/index.html', {"data_symbols": data_symbols})
    else:
        print("GET METHOD")
        return render(request, 'main/index.html', {"data_symbols": data_symbols})


def find_matches(text):
    regex = settings.FUNCTIONS.get("FRAC")
    matches = re.findall(regex, text)
    return matches


def convert_audio(name_record, final_name):
    try:
        record = AudioSegment.from_mp3(name_record)
        record.export(final_name, format="ogg")
    except Exception as e:
        print(e)


def search_string_db(st):
    st = format_str(st)
    query = "select * from expresiones_matematicas where expresion_latex = '%s'" % (st)
    data = query_str(query)
    if len(data) > 0:
        for d in data:
            print(d[3])
            return d[3]
    return st


def query_str(query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query);
            data = cursor.fetchall()
        return data
    except Exception as e:
        print(e)
        raise


def format_str(str):
    if str.startswith('\\'):
        return '\\'+str
    return str


def pdf(request):
    if request.POST:
        nhtml = """
         <html>
              <head>
              </head>
              <body style="margin: 60px; font-size: 25px">
                %s
              </body>
              <script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
          </html>
        """
        data_mathml = request.POST.get("data_mathml", False)
        try:
            if data_mathml:
                data_mathml = ast.literal_eval(data_mathml)
                data_mathml = [n.strip() for n in data_mathml]
                print(type(data_mathml))
                data_mathml = '<br><br>'.join(data_mathml)
                nhtml = nhtml % data_mathml
                print(nhtml)
                pdf = pdfkit.PDFKit(nhtml, "string").to_pdf()
                response = HttpResponse(pdf)  # Generates the response as pdf response.
                response['Content-Type'] = 'application/pdf'
                response['Content-Disposition'] = 'filename=output.pdf'
                return response  # returns the response.
            else:
                raise Http404("Not found")
        except Exception as e:
            raise Http404("Not found")

    else:
        return render(request, 'main/index.html', {})
