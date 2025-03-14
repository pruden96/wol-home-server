// Función para manejar errores de respuesta
async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json();
        throw errorData;
    }
    return response.json();
}

// Función para iniciar sesión
async function login({ username, password }) {
    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        const data = await handleResponse(response);
        if (data.redirect_url) {
            console.log(`Redireccionando a ${data.redirect_url}`);
            window.location.href = data.redirect_url;
        }
    } catch (error) {
        throw error;
    }
}

// Función para agregar un dispositivo (protegida con JWT)
async function addDevice({ name, mac, tag, ip, type }) {
    if (mac === undefined || mac === "") {
        mac = "none";
    }
    if (ip === undefined || ip === "") {
        ip = "none";
    }
    try {
        // const token = getToken()
        const response = await fetch("/add_device", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ name, mac, tag, ip, type }),
        });

        if (response.redirected) {
            window.location.href = response.url;
            return { success: true };
        }

        const data = await handleResponse(response);
        return data;
    } catch (error) {
        throw error;
    }
}

// Función para despertar un dispositivo (Wake-on-LAN) - protegida con JWT
async function wakeDevice(tag, name) {
    try {
        const queryParams = `?tag=${tag}&name=${name}`;
        const endpoint = "/wake" + queryParams;
        const response = await fetch(endpoint, {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await handleResponse(response);
        return data;
    } catch (error) {
        console.error("Error en wakeDevice:", error);
        throw error;
    }
}

// Función para cerrar sesión (logout)
async function logout() {
    try {
        const response = await fetch("/logout", {
            method: "POST",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = await handleResponse(response);
        window.location.href = data.redirect_url;
    } catch (error) {
        throw error;
    }
}

// Función para eliminar un dispositivo (protegida con JWT)
async function removeDevice(tag, name) {
    try {
        const queryParams = `?tag=${tag}&name=${name}`;
        const endpoint = "/remove_device" + queryParams;
        const response = await fetch(endpoint, {
            method: "DELETE",
            credentials: "include",
        });

        if (response.status === 204) {
            return { success: true };
        } else {
            const data = await handleResponse(response);
            return data;
        }
    } catch (error) {
        throw error;
    }
}

// Función para actualizar el nombre de un dispositivo (protegida con JWT)
async function updateDeviceName(tag, name) {
    try {
        const response = await fetch("/update_device_name", {
            method: "PUT",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ tag, name }),
        });

        const data = await handleResponse(response);
        return data;
    } catch (error) {
        throw error;
    }
}

// Solicitud para detener el streaming (protegida con JWT)
async function stopStreaming(deviceId) {
    try {
        const response = await fetch(`/release/${deviceId}`, {
            method: "POST",
            credentials: "include",
        });

        if (response.status === 200) {
            return { success: true };
        } else {
            await handleResponse(response);
        }
    } catch (error) {
        throw error;
    }
}

export {
    login,
    addDevice,
    wakeDevice,
    logout,
    removeDevice,
    updateDeviceName,
    stopStreaming,
};
