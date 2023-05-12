import os
import tempfile
import csv
from django.shortcuts import render
from .forms import PhefluxForm
from .utils.pheflux import getFluxes
from .utils.phefluxParser import *


# Create your views here.


def pheflux_prediction(request):
    if request.method == 'POST':
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
        # CREAR INPUT FILE

        # field_names = ['Organism', 'Condition',
        #                'GeneExpFile', 'Medium', 'Network']
        # dict = {'Organism': organism, 'Condition': condition, 'GenExpFile': gene_temp_route,
        #         'Medium': medium_temp_route, 'Network': network_temp_route}
        # with open("Pheflux/utils/input.csv", "w") as input_file:
        #     writer = csv.DictWriter(
        #         input_file, fieldnames=field_names, delimiter='\t')
        #     writer.writeheader()
        #     writer.writerow(dict)
        with open("Pheflux/utils/input.csv", "w") as input_file:
            writer = csv.writer(input_file, delimiter="\t",
                                lineterminator="\n")
            writer.writerow(["Organism", "Condition",
                             "GeneExpFile", "Medium", "Network",])
            writer.writerow([organism, condition,
                             gene_temp_route, medium_temp_route, network_temp_route])

            # Crear ruta temporal para el resultado
            result_temp = tempfile.NamedTemporaryFile(delete=False)
            result_temp_route = network_temp.name

            prefix_log = request.POST["prefix_log_file"]
            verbosity = request.POST["verbosity"]

        predictions = getFluxes(
            "Pheflux/utils/input.csv", result_temp_route, prefix_log, verbosity)
        # return render(request, 'results.html', {'predictions': predictions})
        # os.remove(ruta_temporal)
        return render(
            request,
            'pheflux_form.html',
            {'form': form}
        )
    else:
        form = PhefluxForm()
    return render(
        request,
        'pheflux_form.html',
        {'form': form}
    )


# predictions = getFluxes(input_data)
    # return render(request, 'results.html', {'predictions': predictions})
 # with open("utils/input.csv", "w") as input_file:
    #     writer = csv.writer("Organism", "Condition",
    #                         "GenExpFile", "Medium", "Network")
    #     writer = csv.writer(form.organism, form.condition,
    #                         gene_temp_route, medium_temp_route, network_temp_route)
