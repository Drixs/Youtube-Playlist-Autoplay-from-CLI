# Youtube Playlist Chooser from CLI
Youtube Playlist Chooser from CLI, from specific channel.
Once executed, it would play a shuffled playlist with random song, at loop.

# About
I own a hundreds of youtube playlists online,
And i've wanted to pick any of them quickly from cli.

# Installation

	1.	pip install -r requirements.txt
	2.	Download ChromeDriver from: http://chromedriver.chromium.org/downloads
		Put chromedriver.exe accesible in %PATH% env.



# Usage

	python play-youtube-playlist-by-name.py <PLAYLIST_NAME>

# Tested on
 * Windows 10
 * Chrome 68.0.3440.106

# Optional 
 * Make Python window hidden, at https://stackoverflow.com/a/36295010
 * Make "ChromeDriver" window hidden, at https://stackoverflow.com/a/48802883
 * Create a shortcut to python, and put it containing directory on %PATH%.
 * Get an updated "uBlock" extension-crx at https://chrome-extension-downloader.com/

# TODO
 - [x] chrome minimize.
 - [x] kill previous script instances.
 - [x] kill previous script instances.
 - [ ] Telegram bot: Recieve playlist name to play form pc.
 - [ ] Telegram bot: Navigation: Stop song, next song, previous song.