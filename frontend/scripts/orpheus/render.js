export function renderResults(results, type) {
    const resultsContainer = document.getElementById("results");

    if (results.length === 0) {
        resultsContainer.innerHTML = "<p>No results found.</p>";
        return;
    }

    // Render results within a container with the grid layout
    resultsContainer.innerHTML = `
        <div class="result-container">
            ${results.map(result => {
                const title = type === 'album' ? result.album : result.title;
                const yearInfo = type === 'album' ? `(${result.year})` : '';

                return `
                    <div class="result-card">
                        <h3>${title} ${yearInfo}</h3>
                        <p><strong>Artist:</strong> ${result.artist}</p>
                        <p><strong>ID:</strong> ${result.id}</p>
                        <button class="download-btn" data-id="${result.id}">Download</button>
                    </div>
                `;
            }).join("")}
        </div>
    `;
}

// Clear results functionality remains the same
document.addEventListener("DOMContentLoaded", () => {
    const moduleSelect = document.getElementById("module");
    const typeSelect = document.getElementById("type");
    const resultsContainer = document.getElementById("results");

    const clearResults = () => {
        resultsContainer.innerHTML = ""; // Clear the results container
    };

    moduleSelect.addEventListener("change", clearResults);
    typeSelect.addEventListener("change", clearResults);
});
