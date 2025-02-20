import { addDevice, logout, wakeDevice, login } from "./api.js";

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

