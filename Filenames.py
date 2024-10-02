import os
def generateFilename(filename): # Give Value like ABC.jpg
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}0{ext}"
    while os.path.exists(new_filename):
        new_filename = f"{base}{counter}{ext}"
        counter += 1
    return new_filename

def getFilename(filename1):
    # Get list of filenames in the current working directory
    base, ext = os.path.splitext(filename1)
    filenames = os.listdir()
    # Filter filenames that start with the specified prefix
    relevant_filenames = [os.path.splitext(filename)[0] for filename in filenames if filename.startswith(base) and filename.endswith(ext)]
    # Extract numerical part of filenames and convert to integers
    indices = [int(filename[len(base):]) if filename[len(base):] != '' else 0 for filename in relevant_filenames]
    # If no relevant filenames are found, return None
    if not indices:
        return None
    # Find the maximum numerical index
    latest_index = max(indices)
    # Construct the latest filename with extension
    latest_filename = f"{base}{latest_index}{ext}"

    return latest_filename
def getFilenameFormat( filename, directory):
    import os, re
    base, ext = os.path.splitext(filename)

    filenames = []
    pattern = re.compile(f"{re.escape(base)}+{re.escape(ext)}", re.IGNORECASE)
    for filename in os.listdir(directory):
        if pattern.match(filename):
            filenames.append(os.path.join(directory, filename))
    return filenames
