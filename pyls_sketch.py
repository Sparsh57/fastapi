import argparse
from datetime import datetime

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
    results = getDescriptionsOfFilesInDir(args.dirname)
    lines = formatResults(results, long_format, filetype)
    printResults(lines)


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
    return [
        {
            "filename": "file1.txt",
            "filetype": "f",
            "modtime": datetime(2024, 8, 8, 10, 12, 22),
            "filesize": 3658,
        },
        {
            "filename": "pyls",
            "filetype": "x",
            "modtime": datetime(2024, 8, 9, 14, 33, 25),
            "filesize": 2554,
        },
        {
            "filename": "tests",
            "filetype": "d",
            "modtime": datetime(2024, 8, 9, 15, 15, 15),
            "filesize": 355,
        },
    ]


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
    return [
        "2024-08-08 14:12:22  4533 sample-file.pdf",
        "2024-08-07 10:24:32   104 myprog*",
    ]


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
