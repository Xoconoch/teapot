export function addToDownloadQueue(downloadQueueDiv, albumURL) {
    const queueItem = document.createElement("div");
    queueItem.className = "download-item";
    queueItem.innerHTML = `
        <p><strong>Album:</strong> ${albumURL}</p>
        <div class="progress-bar">0%</div>
    `;
    downloadQueueDiv.appendChild(queueItem);
    return queueItem;
}

export function updateQueueItem(queueItem, progress, message, album, artist) {
    const progressBar = queueItem.querySelector(".progress-bar");

    if (album && artist) {
        queueItem.querySelector("p").innerHTML = `<strong>${album}</strong> by ${artist}`;
    }

    if (message === "Download complete") {
        progressBar.style.width = "100%";
        progressBar.textContent = "Complete";
        progressBar.style.backgroundColor = "#4caf50";
    } else if (progress) {
        const { downloaded, total } = progress;
        const percentage = (downloaded / total) * 100;
        progressBar.style.width = `${percentage}%`;
        progressBar.textContent = `${Math.round(percentage)}%`;
    }
}
