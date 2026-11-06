# PDF Data Extractor

Automated data extraction tool that reads PDF invoices and extracts structured information (product description, unit price, item code) into a JSON database.

## Features
- Keyword-based PDF parsing
- Automatic data validation
- JSON output for easy integration

## Tech Stack
- Python 3.8+
- pdfplumber
- pandas

## Usage
python pdf_extractor.py --input sample.pdf --output output/data.json