from pipeline import main, validate_input_files, process_drugs, setup_logging
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.config.config import Config

def test_validate_input_files_success(test_data_dir):
    """Test input file validation with existing files"""
    files = [test_data_dir / "test.csv"]
    files[0].touch()
    assert validate_input_files(files) is True

def test_validate_input_files_failure():
    """Test input file validation with non-existent files"""
    files = [Path("nonexistent.csv")]
    assert validate_input_files(files) is False

@patch("pipeline.process_file")
def test_process_drugs_success(mock_process_file):
    """Test drug processing with successful execution"""
    mock_process_file.return_value = {
        "valid_rows": [{"drug": "Aspirin", "atccode": "N02BA01"}],
        "invalid_rows": []
    }
    
    result = process_drugs(Path("test.csv"))
    assert "rows" in result
    assert "search_column" in result

@patch("pipeline.process_file")
def test_process_drugs_with_retry(mock_process_file):
    """Test drug processing with retry mechanism"""
    mock_process_file.side_effect = [
        ValueError("Temporary error"),
        {
            "valid_rows": [{"drug": "Aspirin", "atccode": "N02BA01"}],
            "invalid_rows": []
        }
    ]
    
    result = process_drugs(Path("test.csv"))
    assert "rows" in result
    assert mock_process_file.call_count == 2


@patch("pipeline.process_publication")
@patch("pipeline.process_drugs")
@patch("pipeline.find_drug_mentions")
@patch("pipeline.save_to_json")
def test_main_success(
    mock_save,
    mock_find_mentions,
    mock_process_drugs,
    mock_process_publication,
    config_file
):
    """Test successful execution of main pipeline"""
    # Setup mocks
    mock_process_publication.return_value = [{"test": "data"}]
    mock_process_drugs.return_value = {"test": "data"}
    mock_find_mentions.return_value = [{"result": "data"}]
    
    # Run main function
    with patch("src.config.config.Config") as mock_config:
        mock_config.return_value.get.return_value = {"bronze": "test", "gold": "test"}
        main()
    
    # Verify all steps were called
    mock_process_publication.assert_called_once()
    mock_process_drugs.assert_called_once()
    mock_find_mentions.assert_called_once()
    mock_save.assert_called_once()

def test_main_input_validation_failure(config_file):
    """Test main pipeline with input validation failure"""
    with patch("pipeline.validate_input_files") as mock_validate:
        mock_validate.return_value = False
        main()
        mock_validate.assert_called_once()
