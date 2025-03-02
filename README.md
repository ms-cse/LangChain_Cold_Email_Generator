## LangChain: Cold Email Generator App


### Overview:
- A generative AI app to help Executives/Business Development Teams to write cold emails regarding job posts to the hiring managers.
- This app is created using the LangChain framework and the ChromaDB vector store.
- App automatically extracts the job skillset from the job webpage provided by the user and generates a convincing cold email for the hiring manager.
- It works by extracting the skillset from the job posting and making a semantic search query to the ChromaDB vector store. It finds the most relevant project links from the metadata of vector store and adds them to the email to showcase the expertise or project portfolios.
- App makes simple LLM calls to extract the job details and generate the email.


### Dataset:
- Input Data: CSV file provided in the 'data' folder
- Input Job Post Page: Current/Existing Job Posting Web Page URL
- Vector Store: Inside 'chroma_db' folder.


### Implementation Process:
- Follow the Jupyter Notebook to see the implementation process in detail.


### App:
- Inside the 'app' folder.
- Install the necessary packages using 'requirements.txt'
- Set the GROQ_API_KEY in the '.env' file to run the app.


### Tech Stack:
- LangChain
- ChromaDB
- Groq API
- Streamlit
- Pandas
