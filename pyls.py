import os
from _datetime import datetime
import argparse

parser = argparse.ArgumentParser(
    prog="pyls",
    description="Lists files in given or current directory",
    epilog="Poor man's ls",
)

parser.add_argument(
    "dirname",
    help="Name of directory to list the contents of",
    action="store",
    nargs="?",
    default=".",
)

args = parser.parse_args()

def main(args):
    """
    Processes the whole program and assigns it to functions
    :param args:
    """
    lines = getDescriptionsOfFilesInDir(args.dirname)
    result_list = formatResults(lines)
    displayResults(result_list)

def getDescriptionsOfFilesInDir(dirname):
    """
    Lists the files and folders in the given directory
    and constructs a list of dicts with the required
    information. Always fetches all the details required for
    "long format" presentation for simplicity.
    dirname = The directory whose contents are to be listed.
    The return value is a list of dictionaries each with the following
    keys -
    "filename" = The name of the file.
    "filetype" = "d", "f", or "x" indicating "directory", "plain file",
                 or "executable file" respectively.
    "modtime" = Last modified time of the file as a `datetime` object.
    "filesize" = Number of bytes in the file.
    """
    descriptions = []

    # Iterate over all items in the directory
    for entry in os.listdir(dirname):
        # Get full path of the item
        path = os.path.join(dirname, entry)

        # Check if it's a file or directory
        if os.path.isdir(path):
            filetype = "d"  # Directory
            filesize = 0  # Size is not relevant for directories
        elif os.path.isfile(path):
            filetype = "f"  # Plain file
            filesize = os.path.getsize(path)  # Size of the file
        else:
            continue  # Skip other types like symbolic links

        # Check if the file is executable
        if os.path.isfile(path) and os.access(path, os.X_OK):
            filetype = "x"  # Executable file

        # Get the last modified time
        modtime = datetime.fromtimestamp(os.path.getmtime(path)).replace(microsecond=0)

        # Append the description dictionary to the list
        descriptions.append({
            "modtime": modtime,
            "filesize": filesize,
            "filetype": filetype,
            "filename": entry
        })

    return descriptions

def formatResults(results):
    """
    Takes a list of file descriptions and display control flags
    and returns a list of formatted strings, one per line of output.

    Inputs -
    results = List of dictionaries, like returned by getDescriptionsOfFilesInDir()
    Outputs:
    List of strings.
    """
    list_result = []
    for i in results:
        filename = i["filename"]
        list_result.append(filename)
    return list_result

def displayResults(lines):
    """
    Takes a list of lines and prints them all to the standard output.

    Input:
    lines = List of strings

    Output:
    On standard output
    """
    for line in lines:
        print(line)

if __name__ == '__main__':
    main(args)