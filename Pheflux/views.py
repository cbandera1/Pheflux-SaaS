from django.shortcuts import render
from .forms import PhefluxForm
from .utils.pheflux import getFluxes


# Create your views here.

def pheflux_prediction(request):
    if request.method == 'POST':
        form = PhefluxForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data
            predictions = predict_fluxes(input_data)
            return render(request, 'results.html', {'predictions': predictions})
    else:
        form = PhefluxForm()

    return render(request, 'pheflux.html', {'form': form})
