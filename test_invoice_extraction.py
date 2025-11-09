#!/usr/bin/env python
"""Test script to verify invoice extraction from the sample PDF."""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pos_tracker.settings')
sys.path.insert(0, '/root')
django.setup()

from tracker.utils.pdf_text_extractor import extract_from_bytes, parse_invoice_data
import json

# Read the test PDF
pdf_path = '/root/T 964 DNA.pdf'
if not os.path.exists(pdf_path):
    print(f"PDF file not found at {pdf_path}")
    print("Available PDFs:")
    import glob
    for pdf in glob.glob('/*.pdf'):
        print(f"  {pdf}")
    sys.exit(1)

print(f"Reading PDF from: {pdf_path}")
with open(pdf_path, 'rb') as f:
    file_bytes = f.read()

# Extract and parse
print("\n" + "="*80)
print("TESTING EXTRACTION")
print("="*80)

result = extract_from_bytes(file_bytes, 'T 964 DNA.pdf')

print(f"\nExtraction Success: {result.get('success')}")
print(f"Message: {result.get('message')}")

if result.get('success'):
    header = result.get('header', {})
    items = result.get('items', [])
    
    print("\n" + "-"*80)
    print("EXTRACTED HEADER FIELDS")
    print("-"*80)
    print(f"Invoice No:      {header.get('invoice_no')}")
    print(f"Code No:         {header.get('code_no')}")
    print(f"Customer Name:   {header.get('customer_name')}")
    print(f"Address:         {header.get('address')}")
    print(f"Phone:           {header.get('phone')}")
    print(f"Email:           {header.get('email')}")
    print(f"Reference:       {header.get('reference')}")
    print(f"Date:            {header.get('date')}")
    print(f"Subtotal:        {header.get('subtotal')}")
    print(f"Tax:             {header.get('tax')}")
    print(f"Total:           {header.get('total')}")
    
    print("\n" + "-"*80)
    print("EXTRACTED LINE ITEMS")
    print("-"*80)
    for i, item in enumerate(items, 1):
        print(f"\nItem {i}:")
        print(f"  Description: {item.get('description')}")
        print(f"  Qty:         {item.get('qty')}")
        print(f"  Value:       {item.get('value')}")
    
    print("\n" + "-"*80)
    print("RAW EXTRACTED TEXT (first 500 chars)")
    print("-"*80)
    raw_text = result.get('raw_text', '')
    print(raw_text[:500])
    
    print("\n" + "="*80)
    print("EXPECTED VALUES (from the PDF):")
    print("="*80)
    print("Invoice No:      PI-1765684")
    print("Code No:         A01218")
    print("Customer Name:   SAID SALIM BAKHRESA CO LTD")
    print("Address:         P.O.BOX 2517 DAR-ES-SALAAM TANZANIA")
    print("Phone:           2180007/2861940")
    print("Email:           stm@superdoll-tz.com")
    print("Reference:       FOR T 964 DNA")
    print("Date:            27/10/2025")
    print("Subtotal:        100000.00")
    print("Tax:             18000.00")
    print("Total:           118000.00")
    print("Item 1:          STEERING AXLE ALIGNMENT, Qty: 1, Value: 100000.00")
else:
    print(f"\nError: {result.get('error')}")
    print(f"Message: {result.get('message')}")
