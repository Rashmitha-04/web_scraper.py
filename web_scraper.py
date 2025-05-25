import requests
from bs4 import BeautifulSoup
import json
import csv
import sqlite3
import os
# Optional: Create database connection for calculator history
def init_db():
    conn = sqlite3.connect("calculator_history.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT,operation TEXT,result TEXT)''')
    conn.commit()
    return conn
# Save calculator operation to SQLite
def save_to_db(conn, operation, result):
    cur = conn.cursor()
    cur.execute("INSERT INTO history (operation, result) VALUES (?, ?)", (operation, result))
    conn.commit()
# View calculator history from SQLite
def view_history(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")
    records = cur.fetchall()
    if not records:
        print("No history available.")
    else:
        for row in records:
            print(f"{row[0]}. {row[1]} = {row[2]}")
# Calculator logic
def calculator(conn=None):
    print("\nSimple Calculator")
    print("Operations: + - * / or type 'exit' to return to main menu")   
    while True:
        expr = input("Enter expression: ").strip()
        if expr.lower() == 'exit':
            break
        try:
            result = eval(expr)
            print(f"Result: {result}")
            if conn:
                save_to_db(conn, expr, str(result))
        except ZeroDivisionError:
            print("Error: Division by zero.")
        except Exception:
            print("Error: Invalid input.")
# Web scraper logic
def scrape_website():
    url = input("Enter a website URL to scrape: ").strip()    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract titles and links
        headlines = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'a']):
            text = tag.get_text(strip=True)
            href = tag.get('href')
            if text:
                headlines.append({"text": text, "link": href})
        if not headlines:
            print("No data found.")
            return
        # Save to JSON
        with open("scraped_data.json", "w", encoding='utf-8') as f:
            json.dump(headlines, f, indent=4, ensure_ascii=False)
        # Save to CSV
        with open("scraped_data.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["text", "link"])
            writer.writeheader()
            writer.writerows(headlines)
        print(f"\nScraped {len(headlines)} items.")
        print("Data saved to 'scraped_data.json' and 'scraped_data.csv'.")
    except Exception as e:
        print(f"Failed to scrape website: {e}")
# Main interface
def main():
    conn = init_db()
    while True:
        print("\n--- Scrape Logic App ---")
        print("1. Calculator (Console)")
        print("2. View Calculation History")
        print("3. Web Scraper")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()       
        if choice == '1':
            calculator(conn)
        elif choice == '2':
            view_history(conn)
        elif choice == '3':
            scrape_website()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
    conn.close()
if __name__ == "__main__":
    main()