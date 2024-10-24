from src.utils.file import process_file, get_encoding, is_csv, is_json, check_row
from src.utils.constants import SCHEMA
import pytest
from pathlib import Path

def test_process_csv_file(sample_csv_file):
    """Test processing a CSV file"""
    result = process_file(sample_csv_file)
    assert "valid_rows" in result
    assert "invalid_rows" in result
    assert len(result["valid_rows"]) == 2
    assert len(result["invalid_rows"]) == 0

def test_process_json_file(sample_json_file):
    """Test processing a JSON file"""
    result = process_file(sample_json_file)
    assert "valid_rows" in result
    assert len(result["valid_rows"]) == 1

def test_invalid_file_extension(test_data_dir):
    """Test processing a file with invalid extension"""
    invalid_file = test_data_dir / "invalid.txt"
    invalid_file.touch()
    with pytest.raises(Exception):
        process_file(invalid_file)

def test_file_encoding_detection(sample_csv_file):
    """Test file encoding detection"""
    encoding = get_encoding(sample_csv_file)
    assert encoding is not None
    assert isinstance(encoding, str)

def test_is_csv_file():
    """Test CSV file detection"""
    assert is_csv(Path("test.csv")) is True
    assert is_csv(Path("test.json")) is False

def test_is_json_file():
    """Test JSON file detection"""
    assert is_json(Path("test.json")) is True
    assert is_json(Path("test.csv")) is False

def test_check_row_valid():
    """Test row validation with valid data"""
    schema = SCHEMA["drugs"]
    row = {"atccode": "N02BA01", "drug": "Aspirin"}
    is_valid, error = check_row(schema, row)
    assert is_valid is True
    assert error is None

def test_check_row_invalid():
    """Test row validation with invalid data"""
    schema = SCHEMA["drugs"]
    row = {"atccode": 123, "drug": "Aspirin"}  # atccode should be string
    is_valid, error = check_row(schema, row)
    assert is_valid is False
    assert error is not None
