export async function search(moduleAndAccount, type, query) {
    const [module, account] = moduleAndAccount.includes(" ")
        ? moduleAndAccount.split(" ")
        : [moduleAndAccount, "default"];

    // Detecta si el query es un enlace de Spotify
    if (query.startsWith("https://open.spotify.com")) {
        console.info("Detected Spotify URL. Handling as 'spotify' module.");

        // Simula el módulo como "spotify" y omite la búsqueda
        console.info("Search skipped for 'spotify'. Other scripts can handle this case.");
        return null; // Retorna `null` para indicar que no se realizó la búsqueda
    }

    // Verifica si el módulo es "spotify"
    if (module === "spotify") {
        console.info("Search skipped for 'spotify'. Other scripts can handle this case.");
        return null; // Retorna `null` para indicar que no se realizó la búsqueda
    }

    const baseUrl = window.location.origin;
    const endpoint = `${baseUrl}/orpheus/search/${type}`;

    const payload = {
        module,
        query,
        account,
    };

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }

        const data = await response.json();
        
        // Ajusta para manejar datos de álbum o track correctamente
        return data.results.map(result => {
            if (type === 'album') {
                return {
                    album: result.album,
                    artist: result.artist,
                    id: result.id,
                    year: result.year || "Unknown Year"
                };
            } else {
                return {
                    title: result.title,
                    artist: result.artist,
                    id: result.id,
                    year: result.year || "Unknown Year"
                };
            }
        });
    } catch (error) {
        console.error("Search failed:", error);
        return [];
    }
}
