import argparse
from _datetime import datetime
import os

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

parser.add_argument(
    "-l",
    "--long-format",
    help="Presents more details about files in columnar format",
    action="store_true",
)

parser.add_argument(
    "-F",
    "--filetype",
    help="""Adds an extra character to the end of the printed
                            filename that indicates its type.""",
    action="store_true",
)

args = parser.parse_args()

# Now, `args` has three fields that control the input gathering step
# and the presentation modes.
#
# .dirname   :: str
# .long_format :: bool
# .filetype :: bool

def main(args):
    lines = getDescriptionsOfFilesInDir(args.dirname)
    result_list = formatResults(lines, args.long_format, args.filetype)
    displayResults(result_list)


"""    
    directory_files = os.listdir()
    if parser.file == False and parser.longformat == False:
        print(os.listdir())
    elif not parser.longformat:
        for i in directory_files:
            if os.path.isdir(i):
                print(i + "/")
            if os.path.isfile(i):
                if os.access(i, os.X_OK):
                    print(i + "*")
                else:
                    print(i)
    
    else:
        for i in directory_files:
            modified_time = str(datetime.fromtimestamp(os.path.getmtime(i)).replace(microsecond=0))
            if os.path.isdir(i):
                filesize = '0'
            else:
                filesize = str(os.path.getsize(i))
            print(modified_time + "\t" + filesize + "\t" + i)

"""
def getDescriptionsOfFilesInDir(dirname):
    """
    Lists the files and folders in the given directory
    and constructs a list of dicts with the required
    information. Always fetches all the details required for
    "long format" presentation for simplicity.

    dirname = The directory whose contents are to be listed.
    long_format = True if the user has asked for the long format.
    filetype = True if the user has asked for file type info as well.

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

def formatResults(results, long_format, filetype):
    """
    Takes a list of file descriptions and display control flags
    and returns a list of formatted strings, one per line of output.

    Inputs -
    results = List of dictionaries, like returned by getDescriptionsOfFilesInDir()
    long_format = Boolean that indicates long format output.
    filetype = Boolean that indicates ask for extra type descriptor character at end.

    Outputs:
    List of strings.
    """
    list_result = []
    if long_format and filetype:
        for i in results:
            filesize = str(i["filesize"])
            modtime = str(i["modtime"])
            if i["filetype"] == 'd':
                filename = i["filename"]+"/"
            elif i["filetype"] == 'x':
                filename = i["filename"]+"*"
            else:
                filename = i["filename"]
            list_result.append(modtime+"\t"+filesize+"\t"+filename)
    elif long_format:
        for i in results:
            filesize = str(i["filesize"])
            modtime = str(i["modtime"])
            filename = i["filename"]
            list_result.append(modtime + "\t" + filesize + "\t" + filename)
    elif filetype:
        for i in results:
            if i["filetype"] == 'd':
                filename = i["filename"]+"/"
            elif i["filetype"] == 'x':
                filename = i["filename"]+"*"
            else:
                filename = i["filename"]
            list_result.append(filename)
    else:
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