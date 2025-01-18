export function createAlbumForm(container, onSubmitCallback) {
    const albumForm = document.createElement("form");
    albumForm.id = "albumForm";

    albumForm.innerHTML = `
        <label for="albumURL">Spotify Album URL:</label>
        <input type="text" id="albumURL" placeholder="Enter Spotify album URL" required>
        <button type="submit">Download Album</button>
    `;

    container.appendChild(albumForm);

    albumForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const albumURL = document.getElementById("albumURL").value;
        const module = document.getElementById("module").value;
        onSubmitCallback(albumURL, module);
    });
}
