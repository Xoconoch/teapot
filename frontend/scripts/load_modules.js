document.addEventListener("DOMContentLoaded", () => {
    const moduleSelect = document.getElementById("module");
    const baseURL = window.location.origin;

    // Función para cargar los módulos dinámicamente desde el servidor
    async function loadModules() {
        try {
            const response = await fetch(`${baseURL}/check`);
            const modules = await response.json();

            // Limpiar las opciones previas de los módulos
            moduleSelect.innerHTML = '';

            // Iterar sobre los directorios y sus contenidos
            for (const [dir, contents] of Object.entries(modules)) {
                contents.forEach(item => {
                    const option = document.createElement('option');

                    // Eliminar extensión si existe (ej: .json)
                    const itemName = item.replace(/\.[^/.]+$/, "");

                    // Formatear el valor (sin capitalización)
                    option.value = `${dir} ${itemName}`;

                    // Capitalizar el display del directorio y contenido
                    const capitalizedDir = dir.charAt(0).toUpperCase() + dir.slice(1);
                    const capitalizedItem = itemName.charAt(0).toUpperCase() + itemName.slice(1);

                    option.textContent = `${capitalizedDir} ${capitalizedItem}`;
                    moduleSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error loading modules:', error);
        }
    }

    // Cargar los módulos cuando la página esté lista
    loadModules();
});
