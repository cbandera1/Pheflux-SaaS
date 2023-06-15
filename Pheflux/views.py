import io
import csv
import json
import zipfile
import tempfile
import requests
import pdb
import re
from django.http import *
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import *
from .utils.pheflux import getFluxes


# Create your views here.


def pheflux_prediction(request):
    # Revisa si es que se realiza una request POST en pheflux view
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        # Caso en que se relize POST para el formulario de pheflux
        if form_type == 'formPheflux':
            form = PhefluxForm(request.POST, request.FILES)

            if form.is_valid():

                ## GENEEXP_FILE##
                geneExp_file = request.FILES['geneExp_file']
            # Se genera un archivo temporal para guardar los datos
                geneExp_temp = tempfile.NamedTemporaryFile(delete=False)
                gene_temp_route = geneExp_temp.name

            # Guarda el contenido del archivo geneExp subido en el archivo temporal
                with open(gene_temp_route, 'wb+') as destino:
                    for chunk in geneExp_file.chunks():
                        destino.write(chunk)
                geneExp_temp.close()

                ## MEDIUM_FILE##
                medium_file = request.FILES['medium_file']
            # Se genera un archivo temporal para guardar los datos
                medium_temp = tempfile.NamedTemporaryFile(delete=False)
                medium_temp_route = medium_temp.name

            # Guarda el contenido del archivo Medium  en el archivo temporal
                with open(medium_temp_route, 'wb+') as destino:
                    for chunk in medium_file.chunks():
                        destino.write(chunk)
                medium_temp.close()

                ## NETWORK_FILE##
                network_file = request.FILES['network_file']
            # Se genera un archivo temporal para guardar los datos
                network_temp = tempfile.NamedTemporaryFile(delete=False)
                network_temp_route = network_temp.name

            # Guarda el contenido del archivo subido en el archivo temporal
                with open(network_temp_route, 'wb+') as destino:
                    for chunk in network_file.chunks():
                        destino.write(chunk)
                print(network_temp)
                network_temp.close()
            # Se obtienen los datos de organism y condition
                organism = request.POST["organism"]
                condition = request.POST["condition"]

            # Se genera el archivo input.csv con los datos ingresados
                with open("Pheflux/utils/input.csv", "w") as input_file:
                    writer = csv.writer(input_file, delimiter="\t",
                                        lineterminator="\n")
                    writer.writerow(["Organism", "Condition",
                                    "GeneExpFile", "Medium", "Network",])
                    writer.writerow([organism, condition,
                                    gene_temp_route, medium_temp_route, network_temp_route])

            # Se obtienen los datos de prefix_log y verbosity

                prefix_log = request.POST["prefix_log_file"]
                verbosity = request.POST["verbosity"]
            # Se inicia la ejecucion del algoritmo con el input.csv generado, los datos de prefix_log y verbosity
                predictions = getFluxes(
                    "Pheflux/utils/input.csv", prefix_log, verbosity)
            # Se crean las rutas del archivo de prediction y log
                ruta_solve = f"{predictions[0]}/{predictions[1]}"
                ruta_log = f"{predictions[0]}/{predictions[2]}"
            # Archivo ZIP en memoria
                buffer = io.BytesIO()
                with zipfile.ZipFile(buffer, 'w') as zip_file:
                    # Agregar archivo de prediction al ZIP
                    zip_file.write(ruta_solve, f"{predictions[1]}")

                # Agregar archivo log al ZIP
                    zip_file.write(ruta_log, f"{predictions[2]}")

            # Volver al inicio del archivo ZIP
                buffer.seek(0)

            # Crear una respuesta HTTP con el archivo ZIP
                response = HttpResponse(
                    buffer, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename="results.zip"'

                return response
        # Caso en que se relize POST para realizar una busqueda con BiGG Models API
        elif form_type == 'formSearchBiGG':
            form = SearchBiGGForm(request.POST)
            if form.is_valid():
                # Se obtiene la query ingresada
                query = form.cleaned_data['query']
            # Se realiza la peticion a la base de datos que retorna en formato JSON al cual se le extraen los resultados como opciones
                url = f'http://bigg.ucsd.edu/api/v2/search?query={query}&search_type=models'
                results = requests.get(url).json()
                options = extract_options(results)
            # Se definen los formularios para ser pasados como conexto
                formPheflux = PhefluxForm()
                formSearchBiGG = SearchBiGGForm()
                formSearchTCGA = SearchTCGAForm()

                context = {'options': options,
                           'formPheflux': formPheflux,
                           'formSearchBiGG': formSearchBiGG,
                           'formSearchTCGA': formSearchTCGA
                           }
            # Renderiza nuevamente la vista ahora con los formularios y las opciones resultantes de la busqueda
                return render(
                    request,
                    'pheflux_form.html',
                    context
                )
        elif form_type == 'BiggModelDownload':
            # Obtiene el valor de la seleccion entre las opciones disponibles
            query = request.POST.get('query')
        # Se realiza la peticion a la base de datos para hacer un request del archivo
            url = f'http://bigg.ucsd.edu/static/models/{query}.xml'
            response = requests.get(url)
        # Caso de exito se crea un archivo .xml con el nombre del archivo y se le escribe la informacion
            if response.status_code == 200:
                file_name = f'{query}.xml'
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                print("Archivo descargado exitosamente.")
                formPheflux = PhefluxForm()
                formSearchBiGG = SearchBiGGForm()
                context = {'formPheflux': formPheflux,
                           'formSearchBiGG': formSearchBiGG}
                return render(
                    request,
                    'pheflux_form.html',
                    context
                )
        # Caso error
            else:
                print("Error al descargar el archivo:", response.status_code)
        elif form_type == 'formSearchTCGA':
            form = SearchTCGAForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                file_name = download_file(query)
                with open(file_name, "rb") as file:
                    response = HttpResponse(
                        file.read(), content_type="application/octet-stream")
                    response["Content-Disposition"] = f"attachment; filename={file_name}"
                    print(response)
                    return response

    # Caso de que no sea una peticion POST renderiza los formularios
    else:
        formPheflux = PhefluxForm()
        formSearchBiGG = SearchBiGGForm()
        formSearchTCGA = SearchTCGAForm()
        context = {'formPheflux': formPheflux,
                   'formSearchBiGG': formSearchBiGG,
                   'formSearchTCGA': formSearchTCGA}
        return render(
            request,
            'pheflux_form.html',
            context
        )

# Funcion para extraer las opciones resultantes de la busqueda en BiGG Model API


def extract_options(parsed_data):
    options = []
    for elemento in parsed_data['results']:
        for valor in elemento.values():
            options.append(valor)
    return options


def download_file(file_id):
    data_endpt = "https://api.gdc.cancer.gov/data/{}".format(file_id)

    response = requests.get(data_endpt, headers={
                            "Content-Type": "application/json"})

    # Obtener el nombre del archivo del encabezado Content-Disposition
    response_head_cd = response.headers["Content-Disposition"]
    file_name = re.findall("filename=(.+)", response_head_cd)[0]
    print(file_name)

    with open(file_name, "wb") as output_file:
        output_file.write(response.content)

    return file_name
