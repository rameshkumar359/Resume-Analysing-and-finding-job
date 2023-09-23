# importing necessary packages
from streamlit_option_menu import option_menu
from PIL import Image
from selenium import webdriver
import time
from selenium import webdriver
import os
import replicate
from streamlit_tags import st_tags
import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import streamlit as st
import streamlit as st
import base64
from pyresparser import ResumeParser
import streamlit as st
import nltk
import spacy
nltk.download('stopwords')
spacy.load('en_core_web_sm')


icon = Image.open('apple-xxl.png')
st.set_page_config(page_title="Phone pe pulse data visualization",
                   page_icon=icon,
                   layout="wide")


selected = option_menu(None,
                       options=["Resume Analyser"],
                       icons=["bi bi-laptop"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "options": {"margin": "10px"},
                               "icon": {"color": "black", "font-size": "24px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "15px"},
                               })


with st.sidebar:
    replicate_api = st.text_input(
        'Enter Replicate API token:', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
        os.environ['REPLICATE_API_TOKEN'] = replicate_api


def going_through_jobs():
    i = 2
    while i <= 15:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        try:
            send = driver.find_element_by_xpath(
                "//button[@aria-label='Load more results']")
            driver.execute_script("arguments[0].click();", send)
            time.sleep(3)
        except:
            pass
            time.sleep(5)


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()
    # close open handles
    converter.close()
    fake_file_handle.close()
    return text


def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
if pdf_file is not None:
    save_image_path = './Uploaded_Resumes/' + pdf_file.name
    with open(save_image_path, "wb") as f:
        f.write(pdf_file.getbuffer())
    show_pdf(save_image_path)
    resume_data = ResumeParser(save_image_path).get_extracted_data()
    if resume_data:

        resume_text = pdf_reader(save_image_path)

        st.header("**Extracted Resume data**")
        st.write(resume_data)

        st.header("**Resume Analysis**")
        st.write(
            f'####    :red[ Hey how are you doing , {resume_data["name"]}]')
        st.write(f'###### :blue[ Email: {resume_data["email"]}]')
        st.write(f'###### :blue[ Number: {resume_data["mobile_number"]}]')
        st.write(f'###### :blue[ Education: {resume_data["degree"]}]')
        st.write(
            f'###### :blue[ Designation: {resume_data["designation"]}]')
        st.write(f'###### :blue[ Experience: {resume_data["experience"]}]')
        st.write(
            f'###### :blue[ company_names: {resume_data["company_names"]}]')

        # Skill shows
        keywords = st_tags(
            label='# Your Skills 💡:',
            text='Analysed skills',
            value=resume_data['skills'], maxtags=-1, key='1')

        st.header(
            "**Hey,As an employer iam going to show the strength and weakness of your resume click the button below 🦙💬:**")

        if st.button("Click to view strength and weaknesss "):
            with st.spinner('Analysing  almost there...'):
                output = replicate.run(
                    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
                    input={
                        "prompt": f'Can you help to find strength and weakness of this resume ? {resume_text}',
                        "system_prompt": "Answer like your an employer looking for potential candidate"
                    }
                )
                data = ''.join(output)
                st.write(data)

        st.header(
            "**Click the button to analyse and find domains based on this Resume 🦙💬:**")

        if st.button("Find me the right domain "):
            with st.spinner('Analysing  almost there...'):
                output = replicate.run(
                    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
                    input={
                        "prompt": f'suggest me some domains for job based on this resume ? {resume_text}',
                        "system_prompt": "find me some domains for job analysing the resume"
                    }
                )
                data = ''.join(output)
                st.write(data)

        st.header(
            "**You can ask me any question based on this resume 🦙💬 :**")

        text = st.text_input(
            label="Type your query", placeholder="type here", key="query")

        if st.button("Show Custom query "):
            with st.spinner('Analysing almost there...'):
                output = replicate.run(
                    "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
                    input={
                        "prompt": f'{text} ? {resume_text}',
                        "system_prompt": "Answer like your an employer looking for potential candidate"
                    }
                )
                data = ''.join(output)
                st.write(data)

        st.header(
            "**Please fill the form to find the rigth job for you !!!**")

        col1, col2, col3 = st.columns(3)

        with col1:

            domain = st.text_input(
                label="Please give your domain", placeholder="write your domain", key="domain")

        with col2:
            skill = st.selectbox(label="Choose your skills with respect to resume",
                                 options=resume_data['skills'])

        with col3:
            keywords = st.text_input(
                label="Search by postion if any", placeholder="you can mention Entry level or mid senior level", key="keywords")

        col1, col2 = st.columns(2)

        with col1:
            city = st.text_input(
                label="Select city if any", placeholder="write your domain", key="city")

        with col2:
            country = st.text_input(
                label="Select the country", placeholder="write your domain", key="country")

        if st.button("Find me a job"):
            driver = webdriver.Chrome()
            driver.get(
                f'https://www.linkedin.com/jobs/search?keywords={domain}%20{skill}%20{keywords}&location={city}%2C%20{city}%2C%20{country}')
            going_through_jobs()

            # Loop to scroll through all jobs and click on see more jobs button for infinite scrolling
