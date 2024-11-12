# Resume Link Extractor

## Overview
The **Resume Link Extractor** is a Streamlit-based web application that allows users to generate Boolean search queries for extracting resume links from Google search results. The application uses Google Generative AI and SerpApi to scrape relevant resumes in various formats (PDF, DOC, TXT) based on a user's input. The extracted data is displayed in a user-friendly format and can be saved as a CSV file. Additionally, the application allows storing the extracted links in a MySQL database.

## Features
- Generate Boolean search queries for finding resumes on Google search using Generative AI.
- Use multiple API keys to interact with SerpApi and fetch search results.
- Categorize extracted links into different types such as:
  - Personal Website
  - Cloud Storage
  - Directory
  - Organizational Site
- Display filtered results based on file formats (PDF, DOC, TXT).
- Option to download the results as a CSV file.
- Store extracted data in a local or common MySQL database for future reference.

## Requirements
- Python 3.x
- Streamlit
- Google Generative AI (Gemini API)
- SerpApi API Key
- MySQL Connector for Python
- pandas
- csv
- re
- base64
- datetime

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-username/resume-link-extractor.git
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Get your API key for **Google Generative AI** and **SerpApi**:
   - [Google Generative AI API Key](https://developers.google.com/generative-ai)
   - [SerpApi API Key](https://serpapi.com/)

4. Update the `api_key` variable in the script with your API keys.

## Usage

1. Run the application:

    ```bash
    streamlit run app.py
    ```

2. Open your web browser and navigate to the Streamlit app (usually `http://localhost:8501`).

3. Input a search prompt for generating Boolean search queries (e.g., "I need a Rails developer resume").

4. Click on the **Search** button to generate a query and extract the results.

5. View the filtered results that meet the criteria (PDF, DOC, TXT).

6. Optionally, download the extracted data as a CSV file.

7. The data can also be saved to a local or common MySQL database.

## MySQL Database
- The application connects to a MySQL database to store the extracted resume links.
- You can configure the database connection by modifying the `save_to_database` and `connect_to_mysql` functions in the script.

## Code Explanation
### Functions:
- **generate_search_query**: Uses Google Generative AI to generate Boolean search queries based on the user's input.
- **search_google**: Queries SerpApi to retrieve search results using the generated Boolean query.
- **save_to_database**: Stores extracted data (name, link, query, timestamp) in a MySQL database.
- **save_to_csv**: Saves the extracted data in CSV format.
- **categorize_link**: Categorizes the link based on the source type (e.g., personal website, cloud storage, etc.).
- **main**: The main function that runs the Streamlit UI, processes user input, and displays the results.

## Contributing
Feel free to fork the repository, open issues, and create pull requests. Contributions are welcome!

## Acknowledgments
- [Streamlit](https://streamlit.io/) for the interactive UI.
- [SerpApi](https://serpapi.com/) for providing access to Google search results.
- [Google Generative AI](https://developers.google.com/generative-ai) for helping generate Boolean queries based on user input.


## Support the project

<a href="https://www.linkedin.com/in/nagarajanbj/" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-black.png" alt="Buy Me A Coffee" height="45" width="163" ></a>


#### Happy Coding  ♥️
