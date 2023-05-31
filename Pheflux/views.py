import io
import os
import tempfile
import csv
import requests
import zipfile
import pdb
import json
from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import PhefluxForm, SearchBiGGForm
from .utils.pheflux import getFluxes


# Create your views here.


def pheflux_prediction(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'formPheflux':
            form = PhefluxForm(request.POST, request.FILES)

            if form.is_valid():

                ## GENEEXP_FILE##
                geneExp_file = request.FILES['geneExp_file']
                geneExp_temp = tempfile.NamedTemporaryFile(delete=False)
                gene_temp_route = geneExp_temp.name

            # Guarda el contenido del archivo geneExp subido en el archivo temporal
                with open(gene_temp_route, 'wb+') as destino:
                    for chunk in geneExp_file.chunks():
                        destino.write(chunk)
                geneExp_temp.close()

            ## MEDIUM_FILE##
                medium_file = request.FILES['medium_file']
                medium_temp = tempfile.NamedTemporaryFile(delete=False)
                medium_temp_route = medium_temp.name

            # Guarda el contenido del archivo Medium  en el archivo temporal
                with open(medium_temp_route, 'wb+') as destino:
                    for chunk in medium_file.chunks():
                        destino.write(chunk)
                medium_temp.close()

            ## NETWORK_FILE##
                network_file = request.FILES['network_file']
                network_temp = tempfile.NamedTemporaryFile(delete=False)
                network_temp_route = network_temp.name

            # Guarda el contenido del archivo subido en el archivo temporal
                with open(network_temp_route, 'wb+') as destino:
                    for chunk in network_file.chunks():
                        destino.write(chunk)
                print(network_temp)
                network_temp.close()

                organism = request.POST["organism"]
                condition = request.POST["condition"]

                with open("Pheflux/utils/input.csv", "w") as input_file:
                    writer = csv.writer(input_file, delimiter="\t",
                                        lineterminator="\n")
                    writer.writerow(["Organism", "Condition",
                                    "GeneExpFile", "Medium", "Network",])
                    writer.writerow([organism, condition,
                                    gene_temp_route, medium_temp_route, network_temp_route])

                # Crear ruta temporal para el resultado

            prefix_log = request.POST["prefix_log_file"]
            verbosity = request.POST["verbosity"]

            predictions = getFluxes(
                "Pheflux/utils/input.csv", prefix_log, verbosity)

            ruta_solve = f"{predictions[0]}/{predictions[1]}"
            ruta_log = f"{predictions[0]}/{predictions[2]}"
        # Archivo ZIP en memoria
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as zip_file:
                # Agregar archivo 1 al ZIP
                zip_file.write(ruta_solve, f"{predictions[1]}")

            # Agregar archivo 2 al ZIP
                zip_file.write(ruta_log, f"{predictions[2]}")

            # Volver al inicio del archivo ZIP
            buffer.seek(0)

            # Crear una respuesta HTTP con el archivo ZIP
            response = HttpResponse(
                buffer, content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="results.zip"'

            return response
        elif form_type == 'formSearchBiGG':
            form = SearchBiGGForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                url = f'http://bigg.ucsd.edu/api/v2/search?query={query}&search_type=models'
                results = requests.get(url).json()
                # json_data = json.dumps(results)
                # parsed_data = json.loads(results)
                print(type(results))
                options = extract_options(results)
                type(options)
                response = HttpResponse(options)

            # Procesa la respuesta aquí según tus necesidades
                return response
            # Por ejemplo, puedes imprimir el contenido de la respuesta:

    else:
        formPheflux = PhefluxForm()
        formSearchBiGG = SearchBiGGForm()
        context = {'formPheflux': formPheflux,
                   'formSearchBiGG': formSearchBiGG}
        return render(
            request,
            'pheflux_form.html',
            context
        )


def extract_options(parsed_data):
    options = []
    for elemento in parsed_data['results']:
        for valor in elemento.values():
            options.append(valor)

    return options
