# Trendsetter

Trendsetter is a small utility to extract and translate top google trends 
keywords for major countries. When used as a cron job, it compiles a database 
of evolving search trends over time and a window into the past of the internet.

## Installation

### Prerequisites
- Python 3.8+

### Quick Install
```bash
# Clone the repository
git clone https://github.com/yourusername/trendsetter.git
cd trendsetter

# Install dependencies in suitable env
pip install -r requirements.txt
```

### Dependencies
```
pandas       # Data manipulation and analysis
pytrends     # Google Trends API wrapper
googletrans  # Google Translate API wrapper
```

## Usage Guide

### Quick Start
```bash
python save_trending.py
```

## Project Structure

```
trendsetter/
├── src/
│   └── trendsetter.py      # Main Trendsetter class
├── tests/
│   └── test_trendsetter.py # Unit tests
├── data/
│   └── trends.json         # Trend database
├── notebooks/
│   └── trendsetter.ipynb   # Jupyter analysis examples
├── save_trending.py        # Automated trend collection
├── check_kwd.py            # Keyword monitoring
└── requirements.txt        # Python dependencies
```

