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

    function updateCameraStatus() {
        $.get('/get_active_camera', function(response) {
            const activeCamera = response.camera;
            $('#activeCamera').text(
                activeCamera === 'front' ? 'Frontal' :
                activeCamera === 'back' ? 'Trasera' :
                'Ninguna'
            );
            
            // Actualizar estado visual de los botones
            $('#frontCameraBtn').toggleClass('active', activeCamera === 'front');
            $('#backCameraBtn').toggleClass('active', activeCamera === 'back');
        });
    }

    // Actualizar estado cada 60 segundos
    setInterval(updateCameraStatus, 60 * 1000);

    $('#frontCameraBtn').click(function() {
        const btn = $(this);
        btn.prop('disabled', true);
        
        $.ajax({
            url: '/enable_front_camera',
            type: 'POST',
            success: function(response) {
                console.log('Cámara frontal activada');
                updateCameraStatus();
            },
            error: function(error) {
                console.error('Error al activar la cámara frontal', error);
            },
            complete: function() {
                btn.prop('disabled', false);
            }
        });
    });

    $('#backCameraBtn').click(function() {
        const btn = $(this);
        btn.prop('disabled', true);
        
        $.ajax({
            url: '/enable_back_camera',
            type: 'POST',
            success: function(response) {
                console.log('Cámara trasera activada');
                updateCameraStatus();
            },
            error: function(error) {
                console.error('Error al activar la cámara trasera', error);
            },
            complete: function() {
                btn.prop('disabled', false);
            }
        });
    });

    // Actualizar estado inicial
    updateCameraStatus();

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
