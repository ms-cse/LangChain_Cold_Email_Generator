import streamlit as st

import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.document_loaders import WebBaseLoader

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.documents import Document

import chromadb

from langchain_groq import ChatGroq


# ENV Setup
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')


# Global Settings
llm_model = 'llama-3.1-8b-instant'
groq_llm = ChatGroq(model=llm_model, temperature=0.3) 


##### Function to Extract the Job Data from the Web Page
def job_email(wp):

    print(f'For the given link: "{wp}" \n')
    
    ### Web Page Data Loading
    page_loader = WebBaseLoader(wp)

    page_data = page_loader.load()

    data = page_data[0].page_content        # final page data

    ### Job Data Template
    job_template = """
    ### CONTEXT:
    The following context contains the scrapped data about the job posting from a website.
    {text}
    
    ### STRICT INSTRUCTION:
    Your job is to extract the relevant information from the context provided above and convert it into simple JSON string.
    Do not add anything from your side such as PREAMBLE, etc.
    
    ### OUTPUT JSON STRING FORMAT:
    Create a JSON string with the following keys: 'Role', 'Location', 'Experience', 'Skills'
    """

    ### Setting up Prompt Template for Skill Extraction
    gen_job_template = PromptTemplate.from_template(job_template)
    
    ### Setting up Chain and Invoking it
    chain_job = gen_job_template | groq_llm
    resp_job = chain_job.invoke(input={'text':data})

    ### Parsing the response as JSON output
    json_parser = JsonOutputParser()
    json_dict = json_parser.parse(resp_job.content)

    ### Final Skills as Jobs
    jobs = json_dict['Skills']

    print('Skills Extracted ... \n')

    ###########################################################################################################

    
    ### Loading Existing ChromaDB Vector Database
    client = chromadb.PersistentClient('./chroma_db')
    collection = client.get_collection(name="portfolio")

    ### Extracting Portfolio Links metadata based on the Skillset

    links = []
    for job in jobs:
        resp = collection.query(query_texts=job, n_results=1).get('metadatas', [])
        # print(job)
        # print(resp[0][0]['Links'])
        links.append((job,resp[0][0]['Links']))

    
    ### Cold Email Template
    email_template = """

    ### JOB DESCRIPTION:
    {job_descriptions}
    
    ### INSTRUCTION:
    You are John, working as a Business Development Executive at ABC Corporation. 
    
    ABC is an AI & Software Consulting company dedicated to facilitating the seamless integration of business processes 
    through automated tools. 
    With our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
    process optimization, cost reduction, and improved overall efficiency. 
    
    Your job is to write a convincing cold email to the hiring manager regarding the job description mentioned above 
    describing the capability of ABC in fulfilling their needs.
    
    Also add the most relevant links as list from the following list of links to showcase ABC's portfolio: {links}
    
    Add your formal details with designation at the end as given below:
    John,
    Business Developement Executive,
    ABC Corporation
    
    Do not provide a preamble.
    ### EMAIL (NO PREAMBLE):
            
    """
    
    ### Setting up Email Generation Template
    gen_email_template = PromptTemplate.from_template(email_template)
    gen_email_template

    
    ### Setting up Chain and Invoking it
    chain_email = gen_email_template | groq_llm
    resp_email = chain_email.invoke(input={'job_descriptions':str(jobs), 'links':links})

    ### LLM Response
    response = resp_email.content

    print('Email Generated ... \n\n')

    return response
