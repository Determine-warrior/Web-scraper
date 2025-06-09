

# 📦 EcommerceScraper

A Python-based scraper that compares product prices (above ₹50,000) across **Amazon India** and **Flipkart**, and categorizes them into price bands for easier comparison.

## 🔍 Features

* Scrapes product listings for specific search terms
* Supports both **Amazon.in** and **Flipkart.com**
* Filters products by price (₹50,000 and above)
* Categorizes products into predefined price bands:

  * **Band 1**: ₹50,000 – ₹69,999
  * **Band 2**: ₹70,000 – ₹99,999
  * **Band 3**: ₹100,000 and above
* Extracts and displays key specifications when available
* Multithreaded scraping for faster results
* Outputs a clean, formatted report to the console

---

## 🧾 Requirements

Install dependencies using:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
requests
beautifulsoup4
pandas
```

---

## 🚀 Usage

Run the script with:

```bash
python scraper.py
```

Make sure the script is saved as `scraper.py`, or update the filename as needed.

### Example Output

```
Scraping prices for: iPhone 15, iPhone 14, Samsung S24, Samsung S23

--- Price Band: Band 2 ---
Platform        Title                                             Price        Specifications
----------------------------------------------------------------------------------------------------
Amazon          iPhone 15 (128 GB) - Blue                         ₹79,999.00   Display: 6.1", RAM: 6GB, Storage: 128GB
Flipkart        iPhone 14 Plus (Starlight, 128 GB)               ₹71,999.00   RAM: 6GB, Display: 6.7"

--- Price Band: Band 3 ---
Platform        Title                                             Price        Specifications
----------------------------------------------------------------------------------------------------
Amazon          Samsung Galaxy S24 Ultra 5G (512 GB)             ₹1,29,999.00 Display: 6.8", RAM: 12GB, Camera: 200MP
Flipkart        Samsung Galaxy S24 Ultra (Titanium Black, 1TB)   ₹1,59,999.00 RAM: 12GB, Storage: 1TB

--- End of Report ---
```

---

## ⚙️ Project Structure

```
.
├── scraper.py              # Main script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 📌 Notes

* This tool **only scrapes publicly available data**.
* Websites may change their HTML structure. If the script stops working, inspect the pages and update the HTML selectors accordingly.
* Flipkart and Amazon may block bots; use responsibly and avoid frequent or aggressive scraping.

---

## 📄 License

This project is open-source and free to use for personal and educational purposes.

