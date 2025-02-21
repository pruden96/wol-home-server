// Función para manejar errores de respuesta
async function handleResponse(response) {
    if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
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

        if (data && !data.success) {
            alert(data.message);
        }
        // return data;
    } catch (error) {
        throw new Error(`Error al iniciar sesión: ${error.message}`);
    }
}

// Función para agregar un dispositivo
async function addDevice({ name, mac, tag }) {
    try {
        const response = await fetch('/add_device', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, mac, tag })
        });

        if(response.redirected) {
            window.location.href = response.url;
            return {sucess: true};
        }

        const data = await handleResponse(response);

        /*if (data && !data.success) {
            throw new Error(data.message);
        }*/
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
        throw new Error(`Error al encender el dispositivo: ${error.message}`);
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
        throw new Error(`Error al eliminar el dispositivo: ${error.message}`);
    }
}

export { login, addDevice, wakeDevice, logout, removeDevice };
