import re

def parse_track_output(line):
    track_pattern = re.compile(r'Track (\d+)/(\d+)')
    detailed_track_pattern = re.compile(r'Downloading track (.+?) \((\d+)\)')
    detailed_artist_pattern = re.compile(r'Artists: (.+?) \(\d+\)')
    skipped_or_downloaded_pattern = re.compile(r'Track \d+ (skipped|downloaded)')

    # Match track progress
    if 'Track' in line and not ('===' in line):
        match = track_pattern.search(line)
        if match:
            return {"downloaded": int(match.group(1)), "total": int(match.group(2))}

    # Match detailed track download
    if 'Downloading track' in line:
        match = detailed_track_pattern.search(line)
        if match:
            return {"track": match.group(1)}

    # Match detailed artist information
    if 'Artists:' in line:
        match = detailed_artist_pattern.search(line)
        if match:
            return {"artist": match.group(1)}

    # Match track skipped or downloaded
    if 'Track' in line and ('skipped' in line or 'downloaded' in line):
        match = skipped_or_downloaded_pattern.search(line)
        if match:
            return {"message": "Download complete"}

    return None
