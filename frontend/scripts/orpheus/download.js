const MAX_CONCURRENT_DOWNLOADS = 5;
const downloadQueue = [];
let activeDownloads = 0;

/**
 * Controla la ejecución de descargas de manera limitada.
 */
async function processDownloadQueue() {
    while (activeDownloads < MAX_CONCURRENT_DOWNLOADS && downloadQueue.length > 0) {
        const nextTask = downloadQueue.shift(); // Obtiene la próxima descarga de la cola
        activeDownloads++;

        try {
            await nextTask(); // Ejecuta la descarga
        } catch (error) {
            console.error("Error in download task:", error);
        } finally {
            activeDownloads--;
            processDownloadQueue(); // Llama recursivamente para continuar procesando
        }
    }
}

function startLogarithmicProgress(progressBar, current, target, autoProgressIntervalRef) {
    const duration = 1000; // Duración total para alcanzar el próximo paso
    const steps = 20; // Dividir en 20 pasos
    const interval = duration / steps;
    let progressStep = 0;

    clearInterval(autoProgressIntervalRef.current);
    autoProgressIntervalRef.current = setInterval(() => {
        if (progressStep < steps) {
            const fraction = progressStep / steps;
            const nextValue = current + (target - current) * (Math.log1p(fraction) / Math.log1p(1));
            progressBar.style.width = `${nextValue}%`;
            progressBar.textContent = `${Math.floor(nextValue)}%`;
            progressStep++;
        } else {
            clearInterval(autoProgressIntervalRef.current);
        }
    }, interval);
}

async function processStream(reader, progressBar) {
    const decoder = new TextDecoder();
    let total = 1;
    let downloaded = 0;
    let lastReportedProgress = 0;
    const autoProgressIntervalRef = { current: null };

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const text = decoder.decode(value);
        const lines = text.split("\n");

        lines.forEach((line) => {
            if (line.startsWith("data:")) {
                const data = JSON.parse(line.replace("data: ", ""));

                if (data.downloaded && data.total) {
                    downloaded = data.downloaded;
                    total = data.total;

                    const nextProgress = Math.round((downloaded / total) * 100);
                    startLogarithmicProgress(progressBar, lastReportedProgress, nextProgress, autoProgressIntervalRef);
                    lastReportedProgress = nextProgress;
                }

                if (data.message === "Download complete") {
                    clearInterval(autoProgressIntervalRef.current);
                    progressBar.style.width = "100%";
                    progressBar.textContent = "Complete";
                    progressBar.classList.add("progress-complete");
                }
            }
        });
    }
}

export function setupDownloadButtons() {
    document.addEventListener("click", (event) => {
        if (
            event.target.classList.contains("download-btn") ||
            event.target.classList.contains("retry-btn")
        ) {
            const button = event.target;
            const resultCard = button.closest(".result-card");
            const id = button.getAttribute("data-id");
            const type = document.getElementById("type").value;
            const moduleAndAccount = document.getElementById("module").value;

            const [module, account] = moduleAndAccount.includes(" ")
                ? moduleAndAccount.split(" ")
                : [moduleAndAccount, "default"];

            const baseUrl = window.location.origin;
            const endpoint = `${baseUrl}/orpheus/download/${type}?module=${module}&account=${account}&id=${id}`;

            // Crear barra de progreso
            const progressBar = document.createElement("div");
            progressBar.className = "progress-bar";
            progressBar.textContent = "0%";

            // Reemplazar el botón por la barra de progreso
            button.remove();
            resultCard.appendChild(progressBar);

            // Mover el contenedor a la cola de descargas si aún no está ahí
            const downloadContainer = document.getElementById("downloadQueue");
            if (!downloadContainer.contains(resultCard)) {
                downloadContainer.appendChild(resultCard);
            }

            // Agregar la tarea de descarga a la cola
            downloadQueue.push(async () => {
                try {
                    const response = await fetch(endpoint, {
                        method: "GET",
                        headers: {
                            Accept: "text/event-stream",
                        },
                    });

                    if (!response.ok) {
                        throw new Error(`Error: ${response.statusText}`);
                    }

                    const reader = response.body.getReader();
                    await processStream(reader, progressBar);
                } catch (error) {
                    console.error("Download failed:", error);

                    // Crear botón de reintentar
                    const retryButton = document.createElement("button");
                    retryButton.className = "retry-btn";
                    retryButton.setAttribute("data-id", id);
                    retryButton.textContent = "Retry";

                    // Reemplazar barra de progreso con botón de reintentar
                    progressBar.remove();
                    resultCard.appendChild(retryButton);
                }
            });

            // Procesar la cola de descargas
            processDownloadQueue();
        }
    });
}
