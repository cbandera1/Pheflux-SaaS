function mostrarSpinner() {
    var target = document.getElementById('spinner-container');
    var spinner = new Spinner().spin();
    target.appendChild(spinner.el);
}

function ocultarSpinner() {
    var target = document.getElementById('spinner-container');
    target.removeChild(target.firstChild);
}

document.getElementById('procesar-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevenir el envío automático del formulario
    mostrarSpinner();

    fetch('/ruta-de-tu-vista/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}', // Asegúrate de tener esto para protección CSRF
        },
        body: JSON.stringify({
            form_type: 'formPheflux',
            // Agrega cualquier otro dato que necesites enviar en tu solicitud POST
        }),
    })
        .then(response => response.blob()) // Esperar una respuesta blob (archivo binario)
        .then(data => {
            ocultarSpinner();
            // Crear enlace de descarga para el archivo ZIP recibido
            const url = window.URL.createObjectURL(new Blob([data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'results.zip');
            document.body.appendChild(link);
            link.click();
            link.remove();
        })
        .catch(error => {
            console.error('Error al procesar datos', error);
            ocultarSpinner();
        });
});