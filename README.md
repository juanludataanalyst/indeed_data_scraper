# Indeed Data Scraper using Selenium

Python project that automates the process of scraping job postings from Indeed using Selenium. This tool navigates through job postings, collects job details, and saves them into structured JSON files for analysis.

---

## 🔧 How Scraper Works  

### Step-by-Step Breakdown  

#### Script Execution and Navigation:  
- The script `indeed_scraper.py` is executed with the following syntax:  
  ```bash
  python indeed_scraper.py --role "<Job Title>" --location "<Country Name>"
  ```  
- The script navigates through Indeed's search results for the specified **role** and **location**.  

#### Data Collection and Storage:  
- Selenium opens Indeed in a web browser and iterates through all job postings for the given query.  
- For each job posting:  
  - The browser navigates to the posting's detailed page.  
  - Job details such as **Title**, **Company**, **Description**, **Salary**, and **Employment Type** are extracted.  
  - Random pauses are introduced between scraping job descriptions to simulate human-like behavior.  
- For each page of results:  
  - A JSON file is created with the extracted data.  
  - The files are saved in a directory named after the current date, location, and role, e.g., `2025-01-04_Spain_Data Analyst`.  
  - Each JSON file corresponds to a page, using a naming convention like `2025-01-04_Spain_Data Analyst_0.json`.  

#### Pagination and CAPTCHAs:  
- Selenium clicks the "Next Page" button to proceed to the next page of results.  
- If no "Next Page" button is available, the script terminates for the current role and location.  
- The scraper is designed to handle CAPTCHAs:  
  - When a CAPTCHA is encountered, the script pauses and retries indefinitely until the page is accessible.  

---

## 🌎 Supported Countries  

The scraper supports the same countries as the original project:  
- 🇪🇸 Spain  
- 🇬🇧 United Kingdom  
- 🇨🇦 Canada  
- 🇩🇪 Germany  
- 🇦🇺 Australia  
- 🇸🇬 Singapore  
- 🇮🇳 India  
- 🇨🇴 Colombia  

---

## 🔍 Features  

- Developed using **Selenium** for dynamic web scraping.  
- Automatically navigates through job postings and collects data directly from job detail pages.  
- Random delays between actions to reduce the likelihood of being flagged as a bot.  
- Efficiently handles CAPTCHAs by retrying indefinitely until successful.  
- Saves data in a structured JSON format for each page, enabling easy processing.  
- Includes mechanisms to avoid bot detection:  
  - **Random user agents**.  
  - **Simulated mouse movements**.  
  - **Automatic acceptance of cookies**.  
  - **Random pauses between interactions**.  

---

## 🛠️ Installation  

Follow the steps below to set up the project:  

### 1. Clone the Repository  
```bash
https://github.com/juanludataanalyst/indeed-selenium-scraper.git
cd indeed-selenium-scraper
```  

### 2. Set Up the Virtual Environment  
```bash
python -m venv env  
source env/bin/activate  # On Windows: .\env\Scripts\activate  
```  

### 3. Install Dependencies  
```bash
pip install -r requirements.txt  
```  

### 4. Install Browser Driver  
- Ensure that you have the appropriate WebDriver installed for Selenium (e.g., **ChromeDriver** or **GeckoDriver**) that matches your browser version.  
- Add the WebDriver's executable file to your system's PATH.  

---

## 🔧 Usage  

Run the script using the following syntax:  
```bash
python indeed_scraper.py --role "<Job Title>" --location "<Country Name>"
```  

### Example  
To scrape job postings for **Data Analyst** roles in **Spain**:  
```bash
python indeed_scraper.py --role "Data Analyst" --location "Spain"
```  

---

## 🛠️ Key Configuration Details  

- **Data Storage**: JSON files for each page are saved in a directory named after the date, role, and location.  
- **Blocking Avoidance**: Introduces random delays and handles CAPTCHAs.  

---

## 📚 Contributing  

We welcome contributions! Follow these steps:  
1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature/your-feature`).  
3. Commit your changes (`git commit -m "Add your message"`).  
4. Push to the branch (`git push origin feature/your-feature`).  
5. Open a pull request.  

---

## 🛤 Disclaimer  

This project is for **educational purposes only**. Ensure compliance with Indeed’s [terms of service](https://www.indeed.com/legal) when using this tool.  

---

## 🎨 License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
