import pytest
from pathlib import Path
import yaml
import csv
import json
import shutil

@pytest.fixture
def test_data_dir():
    """Create and return a temporary test data directory"""
    test_dir = Path("tests/test_data")
    test_dir.mkdir(parents=True, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir)

@pytest.fixture
def config_file(test_data_dir):
    """Create a temporary config file for testing"""
    config = {
        "paths": {
            "bronze": "data/bronze",
            "silver": "data/silver",
            "gold": "data/gold",
            "logs": "logs"
        },
        "processing": {
            "batch_size": 1000,
            "max_retries": 3,
            "retry_delay": 1
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "file": "logs/pipeline.log"
        }
    }
    
    config_path = test_data_dir / "test_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return config_path

@pytest.fixture
def sample_csv_file(test_data_dir):
    """Create a sample CSV file for testing"""
    file_path = test_data_dir / "test_drugs.csv"
    data = [
        {"drug": "Aspirin", "atccode": "N02BA01"},
        {"drug": "Paracetamol", "atccode": "N02BE01"}
    ]
    
    with open(file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["drug", "atccode"])
        writer.writeheader()
        writer.writerows(data)
    return file_path

@pytest.fixture
def sample_json_file(test_data_dir):
    """Create a sample JSON file for testing"""
    file_path = test_data_dir / "test_pubmed.json"
    data = [
        {
            "id": 1,
            "title": "Study of Aspirin",
            "date": "2023-01-01",
            "journal": "Medical Journal"
        }
    ]
    
    with open(file_path, "w") as f:
        json.dump(data, f)
    return file_path
