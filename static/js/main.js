import {
    addDevice,
    logout,
    wakeDevice,
    removeDevice,
    updateDeviceName,
    stopStreaming,
} from "./api.js";

document.addEventListener("DOMContentLoaded", async function () {
    // onSubmit event to handling POST on add_device
    const deviceForm = document.getElementById("device-form");
    if (deviceForm) {
        deviceForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(deviceForm);
            const deviceData = {};

            formData.forEach((value, key) => {
                deviceData[key] = value;
            });

            const deviceTypeSelector = document.getElementById("device-type");
            if (deviceTypeSelector) {
                const typeSelected = deviceTypeSelector.value;
                deviceData["type"] = typeSelected;
            } else {
                deviceData["type"] = "wol";
            }

            try {
                const response = await addDevice(deviceData);
                if (response.success) {
                    alert("Dispositivo agregado exitosamente");
                    deviceForm.reset();
                }
            } catch (error) {
                const errorKeys = Object.keys(error);
                console.log(errorKeys);
                switch (errorKeys[0]) {
                    case "error_mac":
                        document.getElementById("errorMAC").textContent =
                            error.error_mac;
                        break;
                    case "error_tag":
                        document.getElementById("error-tag-text").textContent =
                            error.error_tag;
                        break;
                    case "error_ip":
                        document.getElementById("errorIP").textContent =
                            error.error_ip;
                        break;
                    case "error":
                        alert(
                            "Error al agregar el dispositivo. No se proporcionaron datos suficientes"
                        );
                        break;
                }
            }
        });
    }

    // Evento para el control de cierre de sesión Log-Out
    const logoutButton = document.getElementById("logout-button");
    if (logoutButton) {
        logoutButton.addEventListener("click", async function () {
            try {
                await logout();
            } catch (error) {
                alert("Error al cerrar sesión: " + error.message);
            }
        });
    }

    // Funcion para el renderizado de página
    function gotoPage(url) {
        window.location.href = url;
    }

    // Evento para el retorno al Dashboard desde el menú lateral
    const gotoDashboardButton = document.getElementById(
        "goto-dashboard-button"
    );
    if (gotoDashboardButton) {
        gotoDashboardButton.addEventListener("click", () => gotoPage("/"));
    }

    // Evento para el retorno al Dashboard desde el footer home
    const gotoHome = document.getElementById("goto-home-button");
    if (gotoHome) {
        gotoHome.addEventListener("click", () => gotoPage("/"));
    }

    // Evento para ir a add_device.html desde el boton + del footer
    const gotoAddDevice = document.getElementById("goto-add-device-button");
    if (gotoAddDevice) {
        gotoAddDevice.addEventListener("click", () => gotoPage("/add_device"));
    }

    // Evento para controlar el encendido de dispositivos WoL
    const wakeButtons = document.querySelectorAll(".wake-btn");
    if (wakeButtons) {
        wakeButtons.forEach((button) => {
            button.addEventListener("click", async function (event) {
                const deviceName = event.target.getAttribute("data-name");
                const deviceTag = event.target.getAttribute("data-tag");
                try {
                    await wakeDevice(deviceTag, deviceName);
                } catch (error) {
                    alert(`Error al encender el dispositivo. ${error.message}`);
                }
            });
        });
    }

    // Seleccion de los botones de "VER" para abrir un pop-up de streaming de la cámara
    const playStreamingButtons = document.querySelectorAll(".play-btn");
    if (playStreamingButtons) {
        playStreamingButtons.forEach((button) => {
            let popup;
            let videoPlayer;
            let deviceId;
            button.addEventListener("click", function (event) {
                const deviceName = event.target.getAttribute("data-name");
                deviceId = event.target.getAttribute("data-id");
                const streamingUrl = `/stream/${deviceId}`;
                const deviceNameElement =
                    document.getElementById("streaming-device");
                popup = document.getElementById("pop-up-streaming");
                videoPlayer = document.getElementById("video-player");
                deviceNameElement.textContent = deviceName;
                videoPlayer.src = streamingUrl;
                popup.style.display = "flex";
            });

            const closeStreamingBtn = document.getElementById(
                "close-streaming-btn"
            );
            if (closeStreamingBtn) {
                closeStreamingBtn.addEventListener("click", async function () {
                    videoPlayer.src = "";
                    popup.style.display = "none";
                    try {
                        await stopStreaming(deviceId);
                    } catch (error) {
                        alert(`Error al terminar el streaming. ${error.error}`);
                    }
                });
            }
        });
    }

    // Evento para validar el ingreso de la dirección MAC
    const macInput = document.getElementById("device-mac");
    if (macInput) {
        macInput.addEventListener("input", function () {
            validarMAC(this);
        });
    }

    // Evento para validar el ingreso del TAG del dispositivo
    const tagInput = document.getElementById("device-tag");
    if (tagInput) {
        tagInput.addEventListener("input", function () {
            formatearCampo(this);
        });
    }

    // Evento para validar el ingreso de un nuevo usuario en register.html
    const usernameInput = document.getElementById("reg-username");
    if (usernameInput) {
        usernameInput.addEventListener("input", function () {
            validarNombreUsuario(this);
        });
    }

    // Evento para validar el ingreso de email para un nuevo usuario en register.html
    const emailInput = document.getElementById("reg-email");
    if (emailInput) {
        emailInput.addEventListener("input", function () {
            validarEmail(this);
        });
    }

    // Evento para eliminar un dispositivo. Se levanta un PopUp de confirmación
    const removeDeviceBtn = document.querySelectorAll(".remove-device");
    if (removeDeviceBtn) {
        removeDeviceBtn.forEach((button) => {
            button.addEventListener("click", function () {
                const deviceTag = this.getAttribute("data-tag");
                const deviceName = this.getAttribute("data-name");

                // Mostrar el popup
                const popup = document.getElementById("pop-up-confirmacion");
                document.getElementById(
                    "mensaje-confirmacion"
                ).textContent = `¿Estás seguro que deseas eliminar este elemento: ${deviceName}?`;
                popup.style.display = "flex";

                // Configurar el botón de confirmar para este dispositivo
                document.getElementById("boton-confirmar").onclick =
                    async function () {
                        console.log(
                            `Eliminar dispositivo: ${deviceName} (${deviceTag})`
                        );
                        try {
                            await removeDevice(deviceTag, deviceName);
                            popup.style.display = "none";
                            window.location.reload();
                        } catch (error) {
                            alert(
                                `Error al eliminar el dispositivo. ${error.error}`
                            );
                        }
                    };

                // Configurar el botón de cancelar
                document.getElementById("boton-cancelar").onclick =
                    function () {
                        popup.style.display = "none";
                    };
            });
        });
    }

    // Evento para personalizar los campos de entrada de registro de un nuevo dispositivo de acuerdo al tipo de dispositivo seleccionado. (Add_device.html)
    const deviceTypeSelector = document.getElementById("device-type");
    if (deviceTypeSelector) {
        deviceTypeSelector.addEventListener("change", function () {
            const selectedType = this.value;
            const macInput = document.getElementById("device-mac");
            const ipInput = document.getElementById("device-ip");
            const macContainer = document.getElementById("mac-container");
            const ipContainer = document.getElementById("ip-container");

            if (selectedType === "wol") {
                macInput.disabled = false;
                ipInput.disabled = false;
                macContainer.style.display = "block";
                ipContainer.style.display = "block";
            } else {
                ipInput.required = true;
                macInput.disabled = true;
                ipInput.disabled = false;
                macContainer.style.display = "none";
                ipContainer.style.display = "block";
            }
            if (selectedType === "camera-usb") {
                ipInput.placeholder = "ID de Cámara USB [0-3]";
            }
        });
    }

    // Evento para editar el nombre de un dispositivo existente. Lanza un PopUp de cambio de nombre que contiene botones de guardar cambios y cancelar
    const optionsButtons = document.querySelectorAll(".edit-name-button");
    if (optionsButtons) {
        optionsButtons.forEach((button) => {
            button.addEventListener("click", function (event) {
                event.stopPropagation(); // Evita conflictos con otros eventos
                const nameEditPopup =
                    document.getElementById("pop-up-name-edit");
                const editedName = document.getElementById("edited-name");

                const card = button.closest(".card-container"); // Encuentra la card padre
                const deviceNameSpan = card.getAttribute("data-name"); // Obtiene el nombre del dispositivo

                nameEditPopup.style.display = "flex";
                editedName.disabled = false;
                editedName.value = deviceNameSpan;

                // Guardamos el tag del dispositivo
                editedName.setAttribute(
                    "data-tag",
                    card.getAttribute("data-tag")
                );
                const saveNameBtn = document.getElementById("save-name-btn");
                const cancelNameBtn =
                    document.getElementById("cancel-name-btn");
                console.log(`Nombre del dispositivo: ${deviceNameSpan}`);
                saveNameBtn.addEventListener("click", async function () {
                    const newName = editedName.value;
                    const deviceTag = editedName.getAttribute("data-tag");
                    try {
                        await updateDeviceName(deviceTag, newName);
                        console.log(
                            `Actualizar nombre del dispositivo: ${deviceTag} a ${newName}`
                        );
                        // Buscamos el dispositivo correspondiente en la lista y actualizamos su nombre
                        document
                            .querySelectorAll(".card-container")
                            .forEach((card) => {
                                if (
                                    card.getAttribute("data-tag") === deviceTag
                                ) {
                                    const deviceNameSpan =
                                        card.querySelector(".card-name");
                                    deviceNameSpan.textContent = newName;
                                }
                            });
                        nameEditPopup.style.display = "none";
                        editedName.disabled = true;
                        editedName.removeAttribute("data-tag");
                    } catch (error) {
                        if (error.error_tag_name) {
                            alert(
                                `Error al actualizar el nombre del dispositivo: ${error.error_tag_name}`
                            );
                        } else if (error.error) {
                            alert(
                                `Error al actualizar el nombre del dispositivo: ${error.error}`
                            );
                        }
                    }
                });

                cancelNameBtn.addEventListener("click", function () {
                    nameEditPopup.style.display = "none";
                    editedName.disabled = true;
                    editedName.removeAttribute("data-tag");
                });
            });
        });
    }

    // Evento para validar el ingreso de la dirección IP
    const ipInputField = document.getElementById("device-ip");
    if (ipInputField) {
        ipInputField.addEventListener("input", function () {
            validarIP(
                //this.value,
                this,
                deviceTypeSelector ? deviceTypeSelector.value : "wol"
            );
        });
    }
});

function validarIP(input, type) {
    const ip = input.value;
    const error = document.getElementById("errorIP");
    const ipRegex =
        /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    const cameraIdRegex = /^([0-3])$/;
    if (
        (type === "camera-usb" && !cameraIdRegex.test(ip)) ||
        (type !== "camera-usb" && !ipRegex.test(ip))
    ) {
        error.textContent =
            type === "camera-usb"
                ? "Formato de dirección ID inválido. Debe ser [0-3]"
                : "Formato de dirección IP inválido. Debe ser XXX.XXX.XXX.XXX";
        input.setCustomValidity("Formato inválido");
    } else {
        error.textContent = "";
        input.setCustomValidity("");
    }
}

function validarMAC(input) {
    let cursorPos = input.selectionStart; // Guardar posición del cursor
    let mac = input.value;
    let error = document.getElementById("errorMAC");

    // Eliminar espacios en blanco y convertir a mayúsculas
    mac = mac.trim().toUpperCase();

    // Expresión regular para validar el formato de la dirección MAC
    let regex = /^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$/;

    if (!regex.test(mac)) {
        error.textContent =
            "Formato de dirección MAC inválido. Debe ser XX:XX:XX:XX:XX:XX";
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
    valor = valor.replace(/[^a-z0-9]/g, ""); // Eliminar caracteres no alfanuméricos
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
        error.textContent =
            "Nombre de usuario inválido. Debe tener entre 4 y 20 caracteres alfanuméricos o guiones bajos.";
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
        error.textContent =
            "Formato de email inválido. Debe ser algo@exemplo.com";
        input.setCustomValidity("Formato inválido");
    } else {
        error.textContent = "";
        input.setCustomValidity("");
    }

    input.value = email;
    input.setSelectionRange(cursorPos, cursorPos);
}
