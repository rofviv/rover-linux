// Función para matar una screen
function killScreen(screenName) {
    if (confirm(`¿Estás seguro de que quieres eliminar la screen ${screenName}?`)) {
        fetch(`/kill_screen/${screenName}`)
            .then(response => response.json())
            .then(data => {
                const output = document.getElementById('output');
                if (data.success) {
                    output.innerHTML = `<strong>Success:</strong>\n${data.message}`;
                    // Refrescar la lista de screens
                    refreshScreens();
                } else {
                    output.innerHTML = `<strong>Error:</strong>\n${data.error}`;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                const output = document.getElementById('output');
                output.innerHTML = `<strong>Error:</strong>\n${error}`;
            });
    }
}

// Función para cargar la lista de screens
function loadScreens() {
    fetch('/get_screens')
        .then(response => response.json())
        .then(data => {
            const screenList = document.getElementById('screen-list');
            screenList.innerHTML = '';
            
            if (data.error) {
                screenList.innerHTML = `<div class="screen-item error">${data.error}</div>`;
                return;
            }

            if (data.screens.length === 0) {
                screenList.innerHTML = '<div class="screen-item">No active screens</div>';
                return;
            }

            data.screens.forEach(screen => {
                const screenElement = document.createElement('div');
                screenElement.className = 'screen-item';
                
                const screenInfo = document.createElement('div');
                screenInfo.className = 'screen-info';
                screenInfo.innerHTML = `
                    <span class="screen-name">${screen}</span>
                    <span class="view-logs-text">Click to view logs</span>
                `;
                screenInfo.onclick = () => viewScreenLog(screen);
                
                const deleteButton = document.createElement('button');
                deleteButton.className = 'delete-btn';
                deleteButton.innerHTML = '<i class="fas fa-trash"></i>';
                deleteButton.onclick = (e) => {
                    e.stopPropagation(); // Prevenir que el click se propague al padre
                    killScreen(screen);
                };
                
                screenElement.appendChild(screenInfo);
                screenElement.appendChild(deleteButton);
                screenList.appendChild(screenElement);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            const screenList = document.getElementById('screen-list');
            screenList.innerHTML = `<div class="screen-item error">Error loading screens</div>`;
        });
}

// Función para refrescar la lista de screens
function refreshScreens() {
    loadScreens();
}

// Función para ejecutar scripts bash
function executeScreen(scriptName) {
    // Mostrar loading en el output
    const output = document.getElementById('output');
    output.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">Executing ${scriptName}...</div>
        </div>
    `;

    fetch(`/execute_screen/${scriptName}`)
        .then(response => response.json())
        .then(data => {
            // Simular 1 segundo de loading
            setTimeout(() => {
                if (data.success) {
                    output.innerHTML = `
                        <div class="success-message">
                            <i class="fas fa-check-circle"></i>
                            <span>Screen executed successfully</span>
                        </div>
                        <div class="output-details">
                            <strong>Output:</strong>\n${data.output}
                            ${data.error ? `\n\n<strong>Errors:</strong>\n${data.error}` : ''}
                        </div>
                    `;
                    // Actualizar la lista de screens después de 1 segundo
                    setTimeout(refreshScreens, 1000);
                } else {
                    output.innerHTML = `
                        <div class="error-message">
                            <i class="fas fa-exclamation-circle"></i>
                            <span>Error executing screen</span>
                        </div>
                        <div class="output-details">
                            <strong>Error:</strong>\n${data.error}
                        </div>
                    `;
                }
            }, 1000);
        })
        .catch(error => {
            setTimeout(() => {
                console.error('Error:', error);
                output.innerHTML = `
                    <div class="error-message">
                        <i class="fas fa-exclamation-circle"></i>
                        <span>Error executing screen</span>
                    </div>
                    <div class="output-details">
                        <strong>Error:</strong>\n${error}
                    </div>
                `;
            }, 1000);
        });
}

// Cargar screens cuando se carga la página
document.addEventListener('DOMContentLoaded', loadScreens);

function viewScreenLog(screenName) {
    const output = document.getElementById('output');
    output.innerHTML = `
        <div class="loading-container">
            <div class="loading-spinner"></div>
            <div class="loading-text">Loading logs for ${screenName}...</div>
        </div>
    `;

    fetch(`/get_screen_log/${screenName}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                output.innerHTML = `
                    <div class="log-header">
                        <i class="fas fa-terminal"></i>
                        <span>Logs for screen: ${screenName}</span>
                    </div>
                    <div class="log-content">
                        ${data.log.replace(/\n/g, '<br>')}
                    </div>
                `;
            } else {
                output.innerHTML = `
                    <div class="error-message">
                        <i class="fas fa-exclamation-circle"></i>
                        <span>Error getting logs: ${data.error}</span>
                    </div>
                `;
            }
        })
        .catch(error => {
            output.innerHTML = `
                <div class="error-message">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>Error: ${error}</span>
                </div>
            `;
        });
}
