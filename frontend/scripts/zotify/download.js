const baseUrl = window.location.origin; // Base URL is derived from the origin of the loaded frontend.

// Function to handle download requests and update the download queue
async function handleDownloadRequest(module, type, query) {
    if (!module.startsWith("spotify")) {
        return;
    }

    const account = module.split(" ")[1]; // Extract the account part (e.g., 'MX' from 'spotify MX')
    const endpoint = `${baseUrl}/zotify/download/${type}?url=${encodeURIComponent(query)}&account=${account}`;

    const queueContainer = document.getElementById("downloadQueue");
    const downloadItem = document.createElement("div");
    downloadItem.classList.add("result-card");
    downloadItem.innerHTML = `
        <h3>Loading...</h3>
        <p><strong>Status:</strong> Waiting for API response...</p>
    `;
    queueContainer.appendChild(downloadItem);

    let albumTitle = null;
    let artistName = null;
    let totalTracks = 0;
    let downloadedTracks = 0;

    try {
        const response = await fetch(endpoint);

        if (!response.body) {
            throw new Error("Response body is missing.");
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let messageBuffer = "";

        downloadItem.innerHTML = `
            <h3>Loading...</h3>
            <p><strong>Artist:</strong> Loading...</p>
            <div class="progress-container">
                <div class="progress-bar" style="width: 0%;">0%</div>
            </div>
        `;

        const progressBar = downloadItem.querySelector(".progress-bar");

        let currentProgress = 0; // Current progress (percentage)
        let targetProgress = 0; // Target progress for the next step
        let isFirstUpdate = true;

        const updateProgressBar = () => {
            if (currentProgress < targetProgress) {
                const remaining = targetProgress - currentProgress;
                const step = Math.log1p(remaining) / 10; // Logarithmic step calculation
                currentProgress += step;

                if (currentProgress > targetProgress) {
                    currentProgress = targetProgress; // Ensure it doesn't exceed target
                }

                progressBar.style.width = `${currentProgress.toFixed(2)}%`;
                progressBar.innerText = `${Math.floor(currentProgress)}%`;

                if (currentProgress < 100) {
                    requestAnimationFrame(updateProgressBar); // Continue updating
                } else {
                    progressBar.classList.add("complete");
                }
            }
        };

        const completeProgressBar = () => {
            currentProgress = 100;
            targetProgress = 100;
            progressBar.style.width = "100%";
            progressBar.innerText = "Complete";
            progressBar.classList.add("complete");
        };

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            messageBuffer += decoder.decode(value, { stream: true });
            const lines = messageBuffer.split("\n");
            messageBuffer = lines.pop() || "";

            for (const line of lines) {
                if (!line.startsWith("data:")) continue;

                const cleanMessage = line.slice(5).trim();
                try {
                    const data = JSON.parse(cleanMessage);

                    if (data.album) {
                        albumTitle = data.album;
                    } else if (data.track) {
                        albumTitle = data.track;  // Prioriza track si no hay album
                    }
                    if (data.artist) artistName = data.artist;
                    
                    if (albumTitle && artistName) {
                        downloadItem.querySelector("h3").innerText = albumTitle;
                        downloadItem.querySelector("p").innerHTML = `<strong>Artist:</strong> ${artistName}`;
                    }

                    if (data.downloaded !== undefined && data.total !== undefined) {
                        downloadedTracks = data.downloaded;
                        totalTracks = data.total;

                        const newProgress = Math.floor((downloadedTracks / totalTracks) * 100);

                        if (isFirstUpdate) {
                            currentProgress = newProgress - 1; // Start slightly below the first update
                            isFirstUpdate = false;
                        }

                        targetProgress = newProgress;
                        updateProgressBar();
                    }

                    if (data.message === "Download complete") {
                        completeProgressBar();
                        break;
                    }
                } catch (err) {
                    console.error("Failed to parse message:", cleanMessage, err);
                }
            }
        }

        if (messageBuffer.trim()) {
            console.warn("Unprocessed final buffer:", messageBuffer);
        }
    } catch (error) {
        console.error("Error during download:", error);
        downloadItem.innerHTML = `
            <h3>Error</h3>
            <p><strong>Details:</strong> ${error.message}</p>
            <button class="retry-btn">Retry</button>
        `;

        const retryButton = downloadItem.querySelector(".retry-btn");
        retryButton.addEventListener("click", () => {
            queueContainer.removeChild(downloadItem);
            handleDownloadRequest(module, type, query);
        });
    }
}

export { handleDownloadRequest };
