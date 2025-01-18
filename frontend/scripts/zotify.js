// ./scripts/zotify.js

import { handleDownloadRequest } from "./zotify/download.js";

// Attach event listener to the form
const form = document.getElementById("searchForm");
form.addEventListener("submit", (event) => {
    event.preventDefault();

    const module = document.getElementById("module").value;
    const type = document.getElementById("type").value;
    const query = document.getElementById("query").value;

    if (!query.trim()) {
        alert("Please enter a valid query.");
        return;
    }

    handleDownloadRequest(module, type, query);
});
