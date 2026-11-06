
### 📄 `pdf_extractor.py`
```python
import pdfplumber
import pandas as pd
import json
import re
import os
from datetime import datetime

class PDFDataExtractor:
    """
    Extracts structured data from PDF invoices.
    Looks for: product description, unit price, item code.
    """
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.data = []
        
    def extract_text(self):
        """Extract all text from PDF pages."""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    def find_invoices(self, text):
        """
        Find invoice lines using regex patterns.
        Adjust patterns based on your PDF format.
        """
        # Pattern: Code | Description | Unit Price
        # Example: "001234 | Product Name | 29.90"
        pattern = r'(\d{4,})\s*[\|]\s*([^|]+?)\s*[\|]\s*(\d+\.?\d*)'
        
        matches = re.findall(pattern, text)
        
        for match in matches:
            item = {
                'item_code': match[0].strip(),
                'description': match[1].strip(),
                'unit_price': float(match[2]),
                'extraction_date': datetime.now().isoformat()
            }
            self.data.append(item)
    
    def validate_data(self):
        """Check for missing or invalid values."""
        valid_data = []
        for item in self.data:
            if (item['item_code'] and 
                item['description'] and 
                item['unit_price'] > 0):
                valid_data.append(item)
            else:
                print(f"⚠️  Skipped invalid record: {item}")
        return valid_data
    
    def save_to_json(self, output_path):
        """Save extracted data to JSON file."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Extracted {len(self.data)} records to {output_path}")
    
    def run(self, output_path='output/extracted_data.json'):
        """Main execution flow."""
        print(f"📄 Processing: {self.pdf_path}")
        
        text = self.extract_text()
        self.find_invoices(text)
        self.data = self.validate_data()
        self.save_to_json(output_path)
        
        return self.data


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract data from PDF invoices')
    parser.add_argument('--input', required=True, help='Path to PDF file')
    parser.add_argument('--output', default='output/extracted_data.json', help='Output JSON path')
    
    args = parser.parse_args()
    
    extractor = PDFDataExtractor(args.input)
    extractor.run(args.output)
