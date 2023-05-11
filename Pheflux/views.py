from django.shortcuts import render
from .forms import PhefluxForm
from .utils.pheflux import getFluxes
from .utils.phefluxParser import *
import tempfile
import csv

# Create your views here.


def pheflux_prediction(request):
    if request.method == 'POST':
        form = PhefluxForm(request.POST)

        geneExp_file = request.FILES['geneExp_file']
        geneExp_temp = tempfile.NamedTemporaryFile(delete=False)
        gene_temp_route = geneExp_temp.name
        print(gene_temp_route)

        # Guarda el contenido del archivo subido en el archivo temporal
        with open(gene_temp_route, 'wb+') as destino:
            for chunk in geneExp_file.chunks():
                destino.write(chunk)
            geneExp_temp.close()
        if form.is_valid():

            medium_file = request.FILES['medium_file']
            medium_temp = tempfile.NamedTemporaryFile(delete=False)
            medium_temp_route = medium_temp.name

        # Guarda el contenido del archivo Medium  en el archivo temporal
            with open(medium_temp_route, 'wb+') as destino:
                for chunk in medium_file.chunks():
                    destino.write(chunk)
            medium_temp.close()

            network_file = request.FILES['network_file']
            network_temp = tempfile.NamedTemporaryFile(delete=False)
            network_temp_route = network_temp.name

        # Guarda el contenido del archivo subido en el archivo temporal
            with open(network_temp_route, 'wb+') as destino:
                for chunk in network_file.chunks():
                    destino.write(chunk)
            network_temp.close()

            print(gene_temp_route)
            print(medium_temp_route)
            print(network_temp_route)

            # predictions = getFluxes(input_data)
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
