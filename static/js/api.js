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
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.redirected) {
            window.location.href = response.url;
            return;
        }

        const data = await handleResponse(response);
    } catch (error) {
        throw error;
    }
}

// Función para agregar un dispositivo
async function addDevice({ name, mac, tag, ip, type }) {
    if (mac === undefined || mac === '') {
        mac = 'none'
    }
    if (ip === undefined || ip === '') {
        ip = 'none'
    }
    try {
        const response = await fetch('/add_device', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, mac, tag, ip, type })
        });

        if(response.redirected) {
            window.location.href = response.url;
            return {sucess: true};
        }

        const data = await handleResponse(response);

        return data;
    } catch (error) {
        throw error;
    }
}

// Función para despertar un dispositivo (Wake-on-LAN)
async function wakeDevice(tag, name) {
    try {
        const queryParams = `?tag=${tag}&name=${name}`;
        const endpoint = '/wake' + queryParams;

        const response = await fetch(endpoint, { method: 'POST' });
        const data = await handleResponse(response);

        // return data;
    } catch (error) {
        throw error;
    }
}

// Función para cerrar sesión
async function logout() {
    try {
        const response = await fetch('/logout', { method: 'POST' });
        if (response.redirected) {
            window.location.href = response.url;
            return;
        }
        await handleResponse(response);
    } catch (error) {
        throw error;
    }
}

async function removeDevice(tag, name) {
    try {
        const queryParams = `?tag=${tag}&name=${name}`;
        const endpoint = '/remove_device' + queryParams;

        const response = await fetch(endpoint, { method: 'DELETE' });
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

async function updateDeviceName(tag, name) {
    try {
        const response = await fetch('/update_device_name', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tag, name })
        });
        const data = await handleResponse(response);
        return data;
    } catch (error) {
        throw error;
    }  
}

export { login, addDevice, wakeDevice, logout, removeDevice, updateDeviceName };
