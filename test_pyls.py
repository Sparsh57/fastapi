import os
import time

import pytest
from datetime import datetime
from pyls import getDescriptionsOfFilesInDir, formatResults, displayResults

def test_getDescriptionsOfFilesInDir(tmpdir):
    # Create a sample file and directory
    sample_file = tmpdir.join("test_file.txt")
    sample_file.write("Sample content")
    sample_dir = tmpdir.mkdir("test_dir")

    # Call the function
    results = getDescriptionsOfFilesInDir(tmpdir)

    # Check the results
    assert len(results) == 2
    assert results[0]["filename"] == "test_file.txt"
    assert results[0]["filetype"] == "f"
    assert results[1]["filename"] == "test_dir"
    assert results[1]["filetype"] == "d"

def test_formatResults():
    # Sample input
    sample_results = [
        {"filename": "file1.txt"},
        {"filename": "dir1"}
    ]

    # Call the function
    formatted = formatResults(sample_results)

    # Check the output
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

