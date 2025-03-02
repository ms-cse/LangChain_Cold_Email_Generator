### Streamlit App Main File##
import streamlit as st
from utils import job_email


#### Streamlit App ####
st.set_page_config(page_title='Cold Email Generator App', page_icon='📧', layout="wide", initial_sidebar_state="collapsed", menu_items=None)

with st.sidebar:
    st.markdown('### **About**')
    st.info('A Generative AI App built using ***LangChain and Streamlit.***')
    st.info("This app extracts the job data from a web page and generates the cold email for the hiring manager.")
    st.info("App automatically searches and adds the most relevant portfolio links into the email content.")
    st.divider()
    st.success('Created by: Manish Sharma 🤖')


st.markdown(f"## **📧 Cold Email Generator App**")
st.divider()

l,m,r = st.columns([8,1,10])

with l:
    input_url = st.text_input(label='Job Page URL', placeholder='Enter / Paste a Job Page URL here', 
                              label_visibility='hidden')

    sub_btn = st.button(label='Generate Email')

with r:
    st.write(f'#### Email')
    empty = st.empty()
    empty.info('Please, provide a valid URL, and click the button')
    #st.divider()

    if sub_btn:
        if input_url:    
            empty.write('Generating Email, Please wait ...')

            email = job_email(input_url)                              ### email generation function

            empty.code(email, language='markdown')                    ### displaying cold email content
        else:
            empty.warning('Please, provide a valid URL, and click the button')
