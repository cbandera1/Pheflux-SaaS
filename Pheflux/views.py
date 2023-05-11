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
        temp_route = geneExp_temp.name

        # Guarda el contenido del archivo subido en el archivo temporal
        with open(temp_route, 'wb+') as destino:
            for chunk in geneExp_file.chunks():
                destino.write(chunk)
        geneExp_temp.close()

        print(temp_route)

        with open(temp_route, 'r') as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                print(fila)

        if form.is_valid():
            geneExp_file = request.FILES['geneExp_file']
            medium_file = request.FILES['medium_file']
            print(geneExp_file.name)
            # CREAR INPUT FILE
            input_data = form.cleaned_data
            # predictions = getFluxes(input_data)
            # return render(request, 'results.html', {'predictions': predictions})
            return render(
                request,
                'pheflux.html',
                context={'geneExp_file': geneExp_file}
            )
    else:
        form = PhefluxForm()
    return render(
        request,
        'pheflux_form.html',
        {'form': form}
    )
