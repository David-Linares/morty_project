# -*- coding: utf-8 -*-
import ast
import re
from io import BytesIO

import pdfkit
from django.db import connection
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.template.loader import get_template
from gtts import gTTS
import imgkit
from pydub import AudioSegment
# from xhtml2pdf import pisa
from asemi import settings
from uuid import getnode as get_mac
import os
import latex2mathml.converter

# Falta corregir orden en el código.


def index(request):
    #Consulta los símbolos de la tabla de apoyo.
    query = "select * from guia_expresiones where expresion_estado = 1 order by categoria_expresion_ge"
    data_symbols = query_str(query)
    # Si llega el método post.
    if request.POST:
        if request.POST.get('latex_form', False): # Si llega post para convertir
            try:
                ############ Variables para Producción
                name_record = "/opt/asemi/asemi/static/audio/"+str(mac)+"last_record%d.mp3"
                final_name = "/opt/asemi/asemi/static/audio/"+str(mac)+"last_record%d.ogg"
                ############ Variables para pruebas
                # name_record = "main/static/"+str(mac)+"last_record%d.mp3"
                # final_name = "main/static/"+str(mac)+"last_record%d.ogg"
                list_final = []
                mathml_output = []
                # Listado de ecuaciones escritas.
                equa_list = request.POST['latex_form'].split('\n')
                num_audio = 0
                for index, value in enumerate(equa_list):
                    # Quita espacios que no sirven
                    # Convierte la ecuación latex a mathml
                    value = value.rstrip()
                    if value:
                        print("paso 1")
                        print(value)
                        value1 = value[:]
                        mathml_output.append(latex2mathml.converter.convert(value))
                        
                        print(mathml_output)
                        matches_list = find_matches(value)
                        tts_str = value[:]
                        print("paso 3")
                        print(matches_list)
                        if len(matches_list) > 0:
                            print("3.1")
                            for m in matches_list:
                                print("3.2")
                                print(m)
                                if "\r" in m:
                                    print("3.3")
                                    m.replace("\r", "")
                                if m != "":
                                    print("3.4")
                                    strdb = search_string_db(m)
                                    tts_str = tts_str.replace(m, strdb)
                                    print(tts_str)
                        else:
                            print("3.5")
                            tts_str = value1
                        print("paso 4")
                        print(tts_str)
                        print(value)
                        print(value1)
                        if 'frac' in value1:
                            tts_str = tts_str.replace('}{', ' sobre ')
                        # Genera el código para generar el audio de lectura.
                        elif 'oint' in value1:
                            tts_str = tts_str.replace('(', ' (')
                            tts_str = tts_str.replace('_{', ' desde ')
                            tts_str = tts_str.replace('}^{', ' hasta ')
                            tts_str = tts_str.replace(' (', ' de ')
                        elif 'int' in value1:
                            tts_str = tts_str.replace('(', ' (')
                            tts_str = tts_str.replace('_{', ' desde ')
                            tts_str = tts_str.replace('}^{', ' hasta ')
                            tts_str = tts_str.replace(' (', ' de ')
                        elif 'sqrt[' in value1:
                            tts_str = tts_str.replace('[', ' ')
                            tts_str = tts_str.replace(']{', ' de ')
                        elif 'sqrt{' in value1:
                            tts_str = tts_str.replace('{', ' cuadrada de ')
                        elif 'lim' in value1:
                            tts_str = tts_str.replace('_{', ' desde ')
                            tts_str = tts_str.replace('\\to', ' hasta ')
                            tts_str = tts_str.replace('}(', ' de ')
                        print("paso 5")
                        print(tts_str)
                        text = gTTS(text=tts_str, lang='es')
                        # Borra los archivos anteriores
                        try:
                            os.remove(name_record % num_audio)
                        except:
                            pass
                        # Obtiene fecha para el nombre del archivo
                        text.save(name_record % num_audio)
                        # Convierte el audio
                        convert_audio(name_record % num_audio, final_name % num_audio)
                        list_final.append(final_name % num_audio)
                        num_audio+=1
                return render(request, 'main/index.html',
                              {"mathml_data": mathml_output, "latex_form": request.POST['latex_form'],
                               "name_record": list_final, "data_symbols": data_symbols, "upload_file": False, "val_sound": str(mac)+"last_record"})
            except Exception as e:
                print(e)
                return render(request, 'main/index.html',
                              {"mathml_data": "", "latex_form": request.POST.get('latex_form', ""),
                               "name_record": "", "data_symbols": data_symbols, "upload_file": False})
        else:
            return render(request, 'main/index.html', {"data_symbols": data_symbols, "upload_file": False})
    else:
        return render(request, 'main/index.html', {"data_symbols": data_symbols,"upload_file": False})


def find_matches(text):
    print("paso 2")
    regex = settings.FUNCTIONS.get("FRAC")
    matches = re.findall(regex, text)
    print(matches)
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
    print(query)
    data = query_str(query)
    print(data)
    if len(data) > 0:
        for d in data:
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


def pdf2(request):
    if request.POST:
        nhtml = """
        <!DOCTYPE html>
         <html>
              <head>
                <meta charset="UTF-8">
                <script src="http://fred-wang.github.io/mathml.css/mspace.js"></script>
                <script src="http://fred-wang.github.io/mathjax.js/mpadded.js"></script>
                <script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.2/MathJax.js?config=TeX-MML-AM_CHTML"></script>
              </head>
              <body style="margin: 60px; font-size: 25px">
                %s
              </body>
              
          </html>
        """
        data_mathml = request.POST.get("data_mathml", False)
        print(data_mathml)
        try:
            if data_mathml:
                data_mathml = ast.literal_eval(data_mathml)
                print(data_mathml)
                data_mathml = [n.strip() for n in data_mathml]
                print(data_mathml)
                print(data_mathml)
                data_mathml = data_mathml.replace('<math>', '<math xmlns="http://www.w3.org/1998/Math/MathML">')
                print(data_mathml)
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
            print(e)
            raise Http404("Not found")

    else:
        return render(request, 'main/index.html', {})


def pdf_pdfkit(request):
    mac = get_mac()
    if request.POST:
        data_mathml = request.POST.get("data_mathml", False)
        data_mathml = ast.literal_eval(data_mathml)
        print(data_mathml)
        data_mathml = [n.strip() for n in data_mathml]
        data_mathml = "<br><br>".join(data_mathml)
        print(data_mathml)
        # template = get_template('pdf/pdf_template.html')
        img_html = """
        <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
        <html>
        <head>
        <title>Mathedemo</title>
            <meta charset="utf-8">
        <script type="text/x-mathjax-config">
          MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
        </script>
        <script type="text/javascript"
          src="http://localhost:80/static/main/js/mathjax/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
        </script>
        </head>
        
        <body style="margin: 50px; font-size: 30px; color: white;">
        
        <div style="color: black">
            %s
        </div>
        
        </body>
        </html>
        """
        img_html = img_html % data_mathml
        path_img = "/tmp/"+str(mac)+"img_out.png"
        img_generate = imgkit.from_string(img_html, path_img)
        template = get_template("pdf/pdf_template.html")
        nhtml = template.render({"img_path": path_img})
        # pdf = pdfkit.from_file("templates/pdf/pdf_template.html", "output.pdf")
        pdf = pdfkit.PDFKit(img_html, "string").to_pdf()
        response = HttpResponse(pdf)
        response['Content-Type'] = 'application/pdf'
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response  # returns the response.
    else:
        raise Http404("Not found")

def download_json(request):
    query = "select * from guia_expresiones where expresion_estado = 1 order by categoria_expresion_ge"
    data_symbols = query_str(query)
    try:
        file_path = "/tmp/data.json"
        if request.POST.get("equation_data", False):
            f = open(file_path, "w")
            data = {"data": request.POST.get("equation_data", False)}
            print(data)
            f.write(str(data))
            f.close()
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/json")
                    response['Content-Disposition'] = 'attachment; filename=export.json'
                    return response
        raise Http404
    except Exception as e:
        print(e)
        return render(request, 'main/index.html', {"data_symbols": data_symbols})


def import_json(request):
    query = "select * from guia_expresiones where expresion_estado = 1 order by categoria_expresion_ge"
    data_symbols = query_str(query)
    try:
        upload = eval(request.FILES['uploaded_file'].read())
        print(upload)
        return render(request, 'main/index.html',
                      {"mathml_data": "", "latex_form": upload['data'],
                       "name_record": "", "data_symbols": data_symbols, "upload_file": True})
    except:
        return render(request, 'main/index.html', {"data_symbols": data_symbols})



def about(request):
    return render(request, 'main/about.html')


