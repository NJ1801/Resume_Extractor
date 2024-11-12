import streamlit as st
import google.generativeai as genai
import serpapi
import mysql.connector as sql
import csv 
import re 
import pandas as pd
import base64
import datetime

# Initialize df as an empty DataFrame
df = pd.DataFrame(columns=['Name', 'Link','SourceType', 'Query'])

# Function to generate boolean search query
def generate_search_query(user_input):
    # Configure GenerativeAI
    genai.configure(api_key="API-KEY")

    # Initialize the GenerativeAI model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(
    f'''
    Prompt: As a recruiter, your goal is to source resumes directly from Google search results. Use Boolean search operators to find relevant resumes in formats like PDF, DOC, and TXT files. Avoid job listings, sample resumes, and templates by excluding certain keywords. Remember to include the job role and relevant skills in each query.

    Examples:
    
    Desired Role and Skills:
    
    Question: I need a Rails developer resume
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) “Ruby on Rails developer” -job -jobs -sample -templates -template

    Question: Find me a Data Scientist resume with skills in Python, machine learning, and deep learning.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "Data Scientist" (Python OR "machine learning" OR "deep learning") -job -jobs -sample -templates -template

    Question: I need a resume for a Front-end developer with expertise in HTML, CSS, and JavaScript.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "Front-end Developer" (HTML OR CSS OR JavaScript) -job -jobs -sample -templates -template

    Question: Look for a Java Developer resume with experience in Spring and Hibernate frameworks.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "Java Developer" (Spring OR Hibernate) -job -jobs -sample -templates -template

    Question: Provide resumes for Marketing Managers specializing in digital marketing and content strategy.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "Marketing Manager" ("digital marketing" OR "content strategy") -job -jobs -sample -templates -template

    Question: I need resumes of Cloud Engineers with AWS, Azure, or Google Cloud skills.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "Cloud Engineer" (AWS OR "Azure" OR "Google Cloud") -job -jobs -sample -templates -template

    Question: Find resumes of HR professionals with a background in talent acquisition and onboarding.
    Answer: (intitle:resume OR inurl:cv) (filetype:pdf OR filetype:doc OR filetype:txt) "HR" ("talent acquisition" OR onboarding) -job -jobs -sample -templates -template

    Instructions:
    
    1. Start with the relevant job title or profession, like "Data Scientist" or "Front-end Developer."
    2. Include specific skills or expertise in parentheses, separated by OR operators.
    3. Use file types like PDF, DOC, and TXT to specify document formats.
    4. Avoid irrelevant job listings or sample resumes by excluding keywords like -job, -jobs, -sample, -templates, and -template.
    5. Structure each query as shown in the examples.

    Question: {user_input}
    
    Answer:
    
    '''
)
    response_text = response.text
    response_text = response_text.replace("*", "").strip()
    print(response_text)
    st.write(f"Generated boolean query: ",{response_text})
    return response_text

def search_google(query, num_results, api_keys):
    for api_key in api_keys:
        print(f"Using API Key: {api_key}")
        params = {
            "api_key": api_key,
            "q": query,
            "engine": "google",
            "num": num_results
        }
        try:
            results = serpapi.search(params)
            if results.get("search_metadata"):
                return results
        except Exception as e:
            print(f"API Key {api_key} failed with error: {e}")
            continue
    return {"error": "All API keys failed"}

# Function to save data to MySQL database 
# store in local database
def save_to_database(name, link, user_query):
    db = sql.connect(
        host="localhost",
        user="root",
        password="root123",
        database="antony"
    )
    cursor = db.cursor()
    sql_query = "INSERT INTO link_extractor (name, link, jd, Event_Timestamp) VALUES (%s, %s, %s, %s)"
    sql_values = (name, link, user_query,datetime.datetime.now())
    cursor.execute(sql_query, sql_values)
    db.commit()

# store in common database
def connect_to_mysql(name, link, user_query):
    db = sql.connect(
        host="192.168.0.172",
        user="root",
        password="root123",
        database="data"
    )
    cursor = db.cursor()
    sql_query = "INSERT INTO link_extractor (name, link, jd, Event_Timestamp) VALUES (%s, %s, %s, %s)"
    sql_values_THH = (name, link, user_query,datetime.datetime.now())
    cursor.execute(sql_query, sql_values_THH)
    db.commit()

def save_to_csv(results):
    with open('search_results.csv', mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Snippet', 'Link'])
        if "organic_results" in results:
            for result in results["organic_results"]:
                writer.writerow([result.get('title', ''), result.get('snippet', ''), result.get('link', '')])


def categorize_link(link):
    """Categorizes link by its source type."""
    if re.search(r"(resume|cv|portfolio|experience|bio)", link, re.IGNORECASE):
        return "Personal Website"
    elif re.search(r"(drive\.google|dropbox|onedrive)", link, re.IGNORECASE):
        return "Cloud Storage"
    elif re.search(r"(publications|files|docs)", link, re.IGNORECASE):
        return "Directory"
    elif re.search(r"\.edu|\.org|linkedin|github", link, re.IGNORECASE):
        return "Organizational Site"
    else:
        return "Other"


# Streamlit UI
def main():
    global df  # Accessing the global variable df
    st.title("Resume Link Extractor")
    user_input = st.text_input("Enter your prompt:")
    file_name = st.text_input("Enter the file name to save : ")
    if st.button("Search"):
        boolean_query = generate_search_query(user_input)
        api_keys = [
            "ea07a3c37f690319b935d3d544d9569357871e77075e98a1a453a4b84b0e6958",
            "1c31b579bef73a71c97ed83d9daa5c2548eb91687a63bb771749b20034e41fd5",
            "fc37e93a1819bd6f9f164d737e74579deaff8026f9415f02fed3eed2aa2f7cad",
            "d7d7ee684726b9d7c3cc270be8377c23eba0c5328bb9273ede1ef24ee3284cbf",
            "547105fc3151874c26a09dfbc32fbac6dc3ae999a55516d6333816aefebb1f27",
            "e21f059fec89d8e49a2053ae67955ce892a81f091c018be65ad54d02bffd60fe",
            "754e0b31534e16625470fd1c9bfc02387f5c6f4c7846e686fedbbd59e51b2e90",
            "4744a35061a0be80d2cda9730ed4b7d1cae93652bda6f6cc945d150ae40ebf3c",
            "851c0521790a60e6756c669cb64444e5725f48a8d7946ab3507e88b949f985b0",
            "1f197df48d7ea0a42278c0e3d73da7f57bccd6bb671bf1f4168119ff853663c6",
            "75721bc7a9e2622abfdd979de405c016e9f0e8652516e7a66b56828e2e0f3f34"  
        ]
        results = search_google(boolean_query, num_results=300, api_keys=api_keys)
        if "error" not in results:
            if "organic_results" in results:
                for result in results["organic_results"]:
                    name = result.get('title', '')
                    link = result.get('link', '')
                    source_type = categorize_link(link)

                        # Append data as a dictionary to a list
                    df_list = [{'Name': name,'Link': link,'SourceType': source_type,'Query': user_input}]
                        # Concatenate the list of dictionaries with the existing DataFrame
                    df = pd.concat([df, pd.DataFrame(df_list)], ignore_index=True)
                        #save_to_database(name, link, user_input)
                        # try:
                        #     connect_to_mysql(name,link,user_input)
                        # except:
                        #     pass

                file_ext_pattern = re.compile(r".*\.(pdf|doc|txt|resume|cv|portfolio|experience|bio)$", re.IGNORECASE)
                filtered_df = df[df['Link'].apply(lambda x: bool(file_ext_pattern.match(x)))]

                print(filtered_df)

        # Display output 17,20,142
            st.subheader("Filtered Results")
            if not filtered_df.empty:
                st.dataframe(filtered_df)

            # Save data as CSV
            csv_filename = f"{file_name}.csv"
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # Convert DataFrame to bytes
            href = f'<a href="data:file/csv;base64,{b64}" download="{csv_filename}">Download CSV file</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


# 1. Links from personal websites or unique subdomains
# 2. Links from miscellaneous or general websites
# 3. Cloud storage services
# 4. Company or organizational websites

