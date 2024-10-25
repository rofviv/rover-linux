$(document).ready(function() {
    $('#sonarStatus').change(function() {
        updateSensor('front_status', this.checked);
        $('#frontStatus').text(this.checked ? 'Activo' : 'Inactivo');
    });

    $('#sonarBackStatus').change(function() {
        updateSensor('back_status', this.checked);
        $('#backStatus').text(this.checked ? 'Activo' : 'Inactivo');
    });

    $('#sonarDistance').on('input', function() {
        $('#distanceValue').text(this.value);
    });

    $('#sonarDistance').change(function() {
        updateSensor('distance', this.value);
    });

    $('#latencyStatus').change(function() {
        var isChecked = $(this).is(':checked');
        $('#latencyStatusText').text(isChecked ? 'Activo' : 'Inactivo');
        updateSensor('latency_status', isChecked);
    });

    function updateSensor(key, value) {
        var data = {};
        data[key] = value;
        $.ajax({
            url: '/update_sensor',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                console.log('Sensor actualizado con éxito:', key, value);
            },
            error: function(error) {
                console.error('Error al actualizar el sensor', error);
            }
        });
    }
});
