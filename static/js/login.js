import { login } from "./api.js";

document.addEventListener("DOMContentLoaded", function () {
    // onSubmit event for Log-In
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function (event) {
            event.preventDefault();

            const formData = new FormData(loginForm);
            const loginData = {};

            formData.forEach((value, key) => {
                loginData[key] = value;
            });

            try {
                await login(loginData);
                loginForm.reset();
            } catch (error) {
                if (error.error_auth) {
                    alert("Error de autenticación: " + error.error_auth);
                } else {
                    alert("Error al iniciar sesión: " + JSON.stringify(error));
                }
            }
        });
    }
});
