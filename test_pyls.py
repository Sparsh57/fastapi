from datetime import datetime

from pyls import getDescriptionsOfFilesInDir, formatResults, displayResults


def test_getDescriptionsOfFilesInDir(tmpdir):
    # Create a sample file and directory
    sample_file = tmpdir.join("test_file.txt")
    sample_file.write("Sample content")
    tmpdir.mkdir("test_dir")

    # Call the function
    results = getDescriptionsOfFilesInDir(tmpdir)

    # Check the results
    assert len(results) == 2
    assert results[0]["filename"] == "test_file.txt"
    assert results[0]["filetype"] == "f"
    assert results[1]["filename"] == "test_dir"
    assert results[1]["filetype"] == "d"


def test_formatResults_long_format():
    # Sample input
    sample_results = [
        {"filename": "file1.txt", "filetype": "f", "filesize": 1234, "modtime": datetime(2024, 1, 1, 10, 0, 0)},
        {"filename": "dir1", "filetype": "d", "filesize": 0, "modtime": datetime(2024, 1, 1, 11, 0, 0)}
    ]

    # Call the function with long format
    formatted = formatResults(sample_results, long_format=True, filetype=False)
    assert formatted == [
        "2024-01-01 10:00:00\t1234\tfile1.txt",
        "2024-01-01 11:00:00\t0\tdir1"
    ]


def test_formatResults_filetype():
    # Sample input
    sample_results = [
        {"filename": "file1.txt", "filetype": "f"},
        {"filename": "dir1", "filetype": "d"},
        {"filename": "exec.sh", "filetype": "x"}
    ]

    # Call the function with filetype flag
    formatted = formatResults(sample_results, long_format=False, filetype=True)
    assert formatted == ["file1.txt", "dir1/", "exec.sh*"]


def test_formatResults_simple():
    # Sample input
    sample_results = [
        {"filename": "file1.txt", "filetype": "f"},
        {"filename": "dir1", "filetype": "d"}
    ]

    # Call the function without any flags
    formatted = formatResults(sample_results, long_format=False, filetype=False)
    assert formatted == ["file1.txt", "dir1"]


def test_displayResults(capsys):
    # Sample input
    sample_lines = ["file1.txt", "dir1"]

    # Call the function
    displayResults(sample_lines)

    # Capture the output
    captured = capsys.readouterr()

    # Check the output
    assert captured.out == "file1.txt\n" + "dir1\n"
