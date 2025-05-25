# Scrape Logic App

The Scrape Logic App is a simple utility tool, which is a hybrid of a basic calculator, a history tracker, and a web scraper. Users can perform arithmetic computations and store the results, as well as headline and link extraction from specified website URLs.

# Features

Basic arithmetic operations (+, -, *, /)
Save calculator history in SQLite
Scrape website text and links
Export scraped data to CSV & JSON

# Requirements

Python 3.x  
Install dependencies: pip install requests beautifulsoup4 pandas

# Run the app

python main.py

# Check Output Files

After scraping or calculations:
Scraped data → scraped_data.csv and scraped_data.json
Calculator history → calculator_history.db
