# Drug Mentions Pipeline

A data processing pipeline that analyzes medical publications and clinical trials to find drug mentions. The pipeline processes various data sources, performs text analysis, and generates structured output of drug mentions across different medical publications.

## Features

- **Data Processing**: Handle multiple file formats (CSV, JSON)
- **Drug Detection**: Find drug mentions in medical publications
- **Parallel Processing**: Efficient handling of large datasets
- **Error Recovery**: Built-in retry mechanisms for robust processing
- **Extensible**: Modular design for easy feature additions

## Project Structure

```
project_root/
│
├── src/                    # Source code
│   ├── pipeline.py        # Main pipeline orchestration
│   ├── transform.py       # Data transformation logic
│   └── utils/            # Utility functions
│       ├── file.py       # File operations
│       ├── retry.py      # Retry mechanism
│       ├── constants.py  # Constants and configurations
│       └── utils.py      # General utilities
│
├── tests/                 # Test suite
│   ├── conftest.py       # Test configurations
│   ├── test_pipeline.py  # Pipeline tests
│   └── ...              # Other test modules
│
├── config/               # Configuration files
│   └── config.py        # Configuration management
│
├── data/                 # Data directory
│   ├── bronze/          # Raw input data
│   ├── silver/          # Intermediate processed data
│   └── gold/            # Final output data
│
└── docs/                # Documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Make (for using Makefile commands)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/drug-mentions.git
cd drug-mentions
```

2. Set up the development environment:
```bash
make dev-setup
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up the project structure
- Install development tools


## Usage

### Running the Pipeline

With Make:
```bash
make run
```

Without Make:
```bash
python src/pipeline.py
```

### Input Data Format

The pipeline expects the following input files in the `data/bronze/` directory:

1. `drugs.csv`
2. `clinical_trials.csv`
3. `pubmed.csv` or `pubmed.json`

### Output

The pipeline generates a JSON file in `data/gold/drug_mentions.json`:
```json
[
  {
    "drug": "N02BA01",
    "title": [
      {
        "id": 1,
        "date": "2023-01-01"
      }
    ],
    "journal": [
      {
        "name": "Medical Science",
        "date": "2023-01-01"
      }
    ]
  }
]
```

## Development

### Running Tests

Run all tests:
```bash
make test
```

Run tests with coverage:
```bash
make coverage
```

### Code Quality

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Run all checks:
```bash
make check-all
```

### Available Make Commands

- `make help` - Show available commands
- `make install` - Install package
- `make install-dev` - Install development dependencies
- `make test` - Run tests
- `make coverage` - Run tests with coverage
- `make lint` - Run linting
- `make format` - Format code
- `make clean` - Clean build files
- `make requirements` - Generate requirements files


### [1.0.0] - 2024-10-24
- Initial release
- Basic pipeline functionality
- Test suite
- Documentation

### [1.1.0] - Coming Soon
- Performance improvements
- Additional data sources
- Enhanced error handling