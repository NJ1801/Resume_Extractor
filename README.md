# Resume Link Extractor

## Description
This project allows you to extract resume links from Google search results using Boolean search queries. It leverages Generative AI to generate Boolean queries and SerpAPI to fetch Google search results, which are then filtered and categorized. The links are saved in a DataFrame and can be exported as a CSV file. The links are categorized by source type, such as personal websites, cloud storage, directories, or organizational sites.

## Features
- **Generate Boolean search queries**: Uses Generative AI to generate search queries for specific job roles.
- **Google search integration**: Fetches search results from Google using the SerpAPI.
- **Link categorization**: Categorizes links by source type (personal websites, cloud storage, etc.).
- **Save results**: Results can be saved to a MySQL database or exported as a CSV file.
- **Filter results**: The links are filtered to include only relevant documents (e.g., resumes, CVs, portfolios).

## Installation

### Requirements:
- Python 3.x
- Required Python libraries:
  - `streamlit`
  - `google-generativeai`
  - `serpapi`
  - `mysql-connector`
  - `pandas`
  - `base64`
  - `datetime`
  
Install the necessary libraries using pip:

```bash
pip install streamlit google-generativeai serpapi mysql-connector pandas
Set up API keys
To use the Google search functionality, you need to obtain API keys from SerpAPI and configure them in the code. Replace the placeholder API keys in the api_keys list.

MySQL Setup
Ensure you have a running MySQL instance and create a database named antony or data (depending on where you want to save the results). The table link_extractor should have the following columns:

name (VARCHAR)
link (VARCHAR)
jd (TEXT)
Event_Timestamp (DATETIME)
Usage
Start the Streamlit app:
bash
Copy code
streamlit run app.py
Enter the desired job role or profession in the input field.
The app will generate a Boolean search query and fetch relevant resume links from Google.
Filtered results will be displayed in a table, showing the name, link, source type, and the user query.
You can download the filtered results as a CSV file.
Support the project
<a href="https://www.linkedin.com/in/nagarajanbj/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-black.png" alt="Buy Me A Coffee" height="45" width="163" ></a>

Happy Coding ♥️
vbnet
Copy code
