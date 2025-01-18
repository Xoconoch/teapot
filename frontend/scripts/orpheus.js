// Importar automáticamente todos los scripts en la carpeta "orpheus/"
import { search } from './orpheus/search.js';
import { renderResults } from './orpheus/render.js';
import { setupDownloadButtons } from './orpheus/download.js';

// Exportar las funcionalidades para que estén disponibles globalmente si es necesario
export const Orpheus = {
    search,
    renderResults,
    setupDownloadButtons,
};

document.addEventListener("DOMContentLoaded", () => {
    const searchForm = document.getElementById("searchForm");
    const resultsContainer = document.getElementById("results");

    if (!searchForm) {
        console.error("No se encontró el formulario de búsqueda.");
        return;
    }

    searchForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const moduleAndAccount = document.getElementById("module").value;
        const type = document.getElementById("type").value;
        const query = document.getElementById("query").value;

        // Verificar si el query comienza con "https://open.spotify.com"
        if (query.startsWith("https://open.spotify.com")) {
            console.info("Query begins with 'https://open.spotify.com'. No action taken.");
            return;
        }

        resultsContainer.innerHTML = "<p>Loading results...</p>";

        try {
            const results = await Orpheus.search(moduleAndAccount, type, query);

            if (results === null) {
                console.info("Search skipped. Allowing other scripts to handle this case.");
                // Aquí no hacemos nada más, dejando espacio para otros scripts
                return;
            }

            Orpheus.renderResults(results, type);

            // Configura los botones de descarga una vez que se renderizan los resultados
            Orpheus.setupDownloadButtons();
        } catch (error) {
            resultsContainer.innerHTML = "<p>Error during search. Please try again.</p>";
            console.error(error);
        }
    });
});
