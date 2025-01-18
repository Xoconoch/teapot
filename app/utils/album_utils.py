import re

def parse_album_output(line):
    album_pattern = re.compile(r'Downloading album (.+?) \((\d+)\)')
    artist_pattern = re.compile(r'Artist: (.+?) \(\d+\)')
    complete_pattern = re.compile(r'Album (.+?) downloaded')
    track_pattern = re.compile(r'Track (\d+)/(\d+)')

    # Match album download
    if 'Downloading album' in line:
        match = album_pattern.search(line)
        if match:
            return {"album": match.group(1)}

    # Match artist information
    if 'Artist:' in line:
        match = artist_pattern.search(line)
        if match:
            return {"artist": match.group(1)}

    # Match track progress
    if 'Track' in line:
        match = track_pattern.search(line)
        if match:
            return {"downloaded": int(match.group(1)), "total": int(match.group(2))}

    # Match album download completion
    if 'downloaded' in line:
        match = complete_pattern.search(line)
        if match:
            return {"message": "Download complete"}

    return None
