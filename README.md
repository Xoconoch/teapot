## What is this?

This is a web command wrapper for orpheusdl and zotify, it is in very early development. Currently only supports album/track downloads for both orpheus and zotify and, in the case of the first, also search.

It works using sysbox, because the orpheus and zotify instances used to search and download are actually docker containers running inside the main docker container (crazy shi).

## Who is this project for?

This is intended for people that have a personal library of music (say, for example a navidrome server) and want to rip from streaming services. DO NOT expose this project to the public internet, it is not properly prepared for that. If you want remote access to it, use a vpn or a cloudflare tunnel with access control enabled.

## Screenshots

![image](https://github.com/user-attachments/assets/9f329e1b-05fb-41d9-a1d8-e577e55a15d5)
![image](https://github.com/user-attachments/assets/00dee160-d815-4189-8add-726af299d08d)

## Usage

For anything that isn't spotify, you first need to enter a search query, which will then show up to 10 results with their corresponding "Download" buttons, I think the rest is pretty straight forward.

For spotify, you need to select one of the spotify accounts available (up to you) and paste an album/track link in the query box, hit Go! and it'll start the download.

## Why did you use DinD?

Because I found that when running multiple instances of orpheusdl (in order to have parallel downloads) they would conflict, because orpheusdl is not made to run multiple instances. I know I could have modified the code and implement it myself, but guess what? I'm a lazy mf!

## What about security?

Don't worry, it uses the most secure aproach to DinD, which is [Sysbox](https://github.com/nestybox/sysbox). Containers created using this runtime can have their own, isolated-from-host's docker daemon, so no --privileged flag, no mounting the host's docker daemon to the container nor other security nightmares.


## Docker Setup

0. First of all, you need to [install sysbox](https://github.com/nestybox/sysbox/blob/master/docs/user-guide/install.md). Currently, there are packages for debian-based distros wether it is amd64 or arm64, for other distros you will need to build from source (I know).
1. Start the application using the `docker-compose.yaml` file in the repository:

```bash
docker-compose up -d
```

From this point, there are two possible paths: Deezer, Tidal and Spotify.

### Deezer Setup

2. Execute the following command to access the container's shell:

```bash
docker exec -it [container_name] bash
```
   Replace `[container_name]` with the name of the created container (you can find it using `docker ps`).

3. Inside the teapot container, for each Deezer account you want to configure, run:

```bash
docker run --rm -it -v /app/credentials/deezer/{account_custom_name}:/app/config orpheusdl bash
```
   Replace `{account_custom_name}` with a custom name for the account (e.g., `account1`, `account2`).  This will open an interactive terminal in a temporary orpheusdl container.

4. Execute the following command to create the settings file:

```bash
python /app/orpheus.py settings refresh
```

   This will create the `/app/config/settings.json` file.  Open this file (e.g., using `nano /app/config/settings.json`) and locate the "deezer" section.  Fill in the relevant credentials (`email`, `password`, `bf_secret`, and `track_url_key`).

5. Still inside the orpheusdl container, execute the following command to test the configuration:

```bash
python /app/orpheus.py search deezer album test
```

   If the process was successful, you should see a list of album results and the account should be loaded in the frontend.

### Tidal Setup

2. Execute the following command to access the container's shell:

```bash
docker exec -it [container_name] bash
```
   Replace `[container_name]` with the name of the created container (you can find it using `docker ps`).

3. Inside the teapot container, for each Tidal account you want to configure, run:

```bash
docker run --rm -it -v /app/credentials/tidal/{account_custom_name}:/app/config orpheusdl bash
```
   Replace `{account_custom_name}` with a custom name for the account (e.g., `account1`, `account2`). This will open an interactive terminal in a temporary orpheusdl container.

4. Execute the following command to create the settings file:

```bash
python /app/orpheus.py settings refresh
```

5. Execute the following command to initiate the login process:

```bash
python /app/orpheus.py search tidal album test
```
   This should display the login menu.  It is recommended to use the TV option, as it is the most reliable.

6. After logging in, execute the same command again:

```bash
python /app/orpheus.py search tidal album test
```

   If the process was successful, you should see a list of album results and the account should be loaded in the frontend.

### Spotify setup

This setup doesn't need nested containers, but it ain't that easy still. In order for zotify to work, it needs proper credentials, however, it isn't meant to run headless (without a monitor and desktop environment), so you need to give it a little help with credentials. 

So basically you need to follow [this beautiful repository](https://github.com/dspearson/librespot-auth?tab=readme-ov-file), using a PC/laptop with spotify client installed, and once it generates the credentials.json, you need to modify it a little bit as follows:

- Replace `"auth_type": 1` with `"type":"AUTHENTICATION_STORED_SPOTIFY_CREDENTIALS"`
- Rename `"auth_data"` to `"credentials"` 

Once you do that, you need to go where your docker-compose.yaml is and create the file `./credentials/spotify/{account_custom_name}/credentials.json` and paste the same contents as the `credentials.json` you modified previously on your PC/laptop.
