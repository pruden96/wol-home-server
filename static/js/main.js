import { addDevice, logout, wakeDevice, login, removeDevice, updateDeviceName } from "./api.js";

document.addEventListener("DOMContentLoaded", function () {

    // onSubmit event to handling POST on add_device
    const deviceForm = document.getElementById("device-form");
    if (deviceForm){
        deviceForm.addEventListener("submit", async function (event) {
            event.preventDefault();
        
            const formData = new FormData(deviceForm);
            const deviceData = {};

            formData.forEach((value, key) => {
                deviceData[key] = value;
            });

            try {
                const response = await addDevice(deviceData)
                if (response.success){
                    alert("Dispositivo agregado exitosamente");
                    deviceForm.reset();
                }
            } catch (error){
                document.getElementById("error-tag-text").textContent = 'Tag en uso. Seleccione otro.';
            }
        });
    }
    
    const loginForm = document.getElementById("login-form");
    if (loginForm){
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();
    
            const formData = new FormData(loginForm);
            const loginData = {};
    
            formData.forEach((value, key) => {
                loginData[key] = value;
            });
    
            try {
                await login(loginData)
            } catch (error){
                alert("EROR DE AUTENTICACIÓN:" + error.message);
            }
        });
    }
    
    const logoutButton = document.getElementById("logout-button");
    if(logoutButton){
        logoutButton.addEventListener("click", async function () {
            try {
                await logout();
            } catch (error) {
                alert("Error al cerrar sesión:" + error.message);
            }
        });
    }
    
    const wakeButtons = document.querySelectorAll('.wake-btn');
    if(wakeButtons) {
        wakeButtons.forEach(button => {
            button.addEventListener('click', async function(event) {
                const deviceName = event.target.getAttribute('data-name');
                const deviceTag = event.target.getAttribute('data-tag');
                try {
                    await wakeDevice(deviceTag, deviceName);
                } catch (error) {
                    alert(`Error al encender el dispositivo: ${error.message}`);
                }
            });
        });
    }

    const macInput = document.getElementById("device-mac");
    if(macInput) {
        macInput.addEventListener("input", function() {
            validarMAC(this);
        });
    }

    const tagInput = document.getElementById("device-tag");
    if(tagInput) {
        tagInput.addEventListener("input", function() {
            formatearCampo(this);
        });
    }

    const usernameInput = document.getElementById("reg-username");
    if(usernameInput) {
        usernameInput.addEventListener("input", function() {
            validarNombreUsuario(this);
        });
    }

    const emailInput = document.getElementById("reg-email");
    if(emailInput) {
        emailInput.addEventListener("input", function() {
            validarEmail(this);
        });
    }

    const removeDeviceBtn = document.querySelectorAll('.remove-device');
    if (removeDeviceBtn) {
        removeDeviceBtn.forEach((button) => {
            button.addEventListener('click', function() {
                const deviceTag = this.getAttribute('data-tag');
                const deviceName = this.getAttribute('data-name');
    
                // Mostrar el popup
                const popup = document.getElementById('pop-up-confirmacion');
                document.getElementById('mensaje-confirmacion').textContent = `¿Estás seguro que deseas eliminar este elemento: ${deviceName}?`;
                popup.style.display = 'flex';
    
                // Configurar el botón de confirmar para este dispositivo
                document.getElementById('boton-confirmar').onclick = async function () {
                    console.log(`Eliminar dispositivo: ${deviceName} (${deviceTag})`);
                    try {
                        await removeDevice(deviceTag, deviceName);
                        popup.style.display = 'none';
                        window.location.reload()
                    } catch (error) {
                        alert(`Error al eliminar el dispositivo: ${error.message}`);
                    }
                };
    
                // Configurar el botón de cancelar
                document.getElementById('boton-cancelar').onclick = function () {
                    popup.style.display = 'none';
                };
    
            });
        });
    }
    

    const deviceTypeSelector = document.getElementById("device-type");
    if (deviceTypeSelector) {
        deviceTypeSelector.addEventListener("change", function() {
            const selectedType = this.value;
            const macInput = document.getElementById("device-mac");
            const ipInput = document.getElementById("device-ip");
            const macContainer = document.getElementById("mac-container");
            const ipContainer = document.getElementById("ip-container");
    
            if (selectedType === "wol") {
                macInput.disabled = false;
                ipInput.disabled = true;
                macContainer.style.display = "block";
                ipContainer.style.display = "none";
            } else if (selectedType === "camera") {
                ipInput.required = true;
                macInput.disabled = true;
                ipInput.disabled = false;
                macContainer.style.display = "none";
                ipContainer.style.display = "block";
            }
        });
    }
    

    const optionsButtons = document.querySelectorAll('.options-btn');
    if (optionsButtons) {
        optionsButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                event.stopPropagation(); // Evita conflictos con otros eventos
                console.log('clickeado!');
                const nameEditPopup = document.getElementById('pop-up-name-edit');
                const editedName = document.getElementById('edited-name');
    
                const card = button.closest('.card'); // Encuentra la card padre
                const deviceNameSpan = card.getAttribute('data-name'); // Obtiene el nombre del dispositivo
    
                nameEditPopup.style.display = 'flex';
                editedName.disabled = false;
                editedName.value = deviceNameSpan;
    
                // Guardamos el tag del dispositivo
                editedName.setAttribute('data-tag', card.getAttribute('data-tag'));
                const saveNameBtn = document.getElementById('save-name-btn');
                const cancelNameBtn = document.getElementById('cancel-name-btn');
                console.log(`Nombre del dispositivo: ${deviceNameSpan}`);
                saveNameBtn.addEventListener('click', async function() {
                    const newName = editedName.value;
                    const deviceTag = editedName.getAttribute('data-tag');
                    try {
                        await updateDeviceName(deviceTag, newName);
                        console.log(`Actualizar nombre del dispositivo: ${deviceTag} a ${newName}`)
                        // Buscamos el dispositivo correspondiente en la lista y actualizamos su nombre
                        document.querySelectorAll('.card').forEach(card => {
                            if (card.getAttribute('data-tag') === deviceTag) {
                                const deviceNameSpan = card.querySelector('.card-name');
                                deviceNameSpan.textContent = newName;
                            }
                        });
                        nameEditPopup.style.display = 'none';
                        editedName.disabled = true;
                        editedName.removeAttribute('data-tag');
                        //window.location.reload()
                    } catch (error) {
                        alert(`Error al actualizar el nombre del dispositivo: ${error.message}`);
                    }  
                });
    
                cancelNameBtn.addEventListener('click', function() {
                    nameEditPopup.style.display = 'none';
                    editedName.disabled = true;
                    editedName.removeAttribute('data-tag');
                });
            });
        });
    }

});

function validarMAC(input) {
    let cursorPos = input.selectionStart; // Guardar posición del cursor
    let mac = input.value;
    let error = document.getElementById("errorMAC");

    // Eliminar espacios en blanco y convertir a mayúsculas
    mac = mac.trim().toUpperCase();

    // Expresión regular para validar el formato de la dirección MAC
    let regex = /^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$/;

    if (!regex.test(mac)) {
    error.textContent = "Formato de dirección MAC inválido. Debe ser XX:XX:XX:XX:XX:XX";
    input.setCustomValidity("Formato inválido"); // Para la validación del formulario
    } else {
    error.textContent = "";
    input.setCustomValidity("");
    }

    input.value = mac; // Actualizar el valor del input con el formato correcto
    input.setSelectionRange(cursorPos, cursorPos);
}

function formatearCampo(input) {
    let cursorPos = input.selectionStart;
    let valor = input.value;
    valor = valor.toLowerCase(); // Convertir a minúsculas
    valor = valor.replace(/[^a-z0-9]/g, ''); // Eliminar caracteres no alfanuméricos
    input.value = valor;
    input.setSelectionRange(cursorPos, cursorPos);
}

function validarNombreUsuario(input) {
    let cursorPos = input.selectionStart; // Guardar posición del cursor
    let username = input.value;
    let error = document.getElementById("new-username-error"); // ID del elemento de error

    // Expresión regular para validar el nombre de usuario
    let regex = /^[a-zA-Z0-9_]{4,20}$/;

    if (!regex.test(username)) {
        error.textContent = "Nombre de usuario inválido. Debe tener entre 4 y 20 caracteres alfanuméricos o guiones bajos.";
        input.setCustomValidity("Formato inválido"); // Para la validación del formulario
    } else {
        error.textContent = "";
        input.setCustomValidity("");
    }

    input.value = username; // Actualizar el valor del input 
    input.setSelectionRange(cursorPos, cursorPos); // Restablecer la posición del cursor
}

function validarEmail(input) {
    let cursorPos = input.selectionStart;
    let email = input.value;
    let error = document.getElementById("email-error");

    email = email.trim();

    let regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;

    if (!regex.test(email)) {
        error.textContent = "Formato de email inválido. Debe ser algo@exemplo.com";
        input.setCustomValidity("Formato inválido");
    } else {
        error.textContent = "";
        input.setCustomValidity("");
    }

    input.value = email;
    input.setSelectionRange(cursorPos, cursorPos);
}

