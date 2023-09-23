# Resume-Analysing-and-finding-job
##Problem Statement: Analyzing and providing a detailed review of a given resume is still an
area of research. In this project,supposed to build an application which takes a resume
(pdf) as an input and provides the following information:

1. A detailed analysis of the resume: should be able to parse the resume and extract
all the relevant information such as education, projects, achievements, etc. After
extracting the information, should be able to provide a detailed analysis of it based
on the domain of the user. For instance the learner might be from data science domain,
then should be able to give a summary report, strengths and weaknesses in the
resume, and on what areas the user can work to improve their resume.
2. Based on the resume,should be able to provide the set of job openings available
through linkedin.

Suggested tools: You can use any set of tools to finish this task. A few suggested tools include
Streamlit, GPT-4 or any LLM, linkedin parser, etc

# Preview
![image](https://github.com/rameshkumar359/Resume-Analysing-and-finding-job/assets/96288285/a6519e3d-cb94-4cc2-a7cf-333873e7a773)

![Screenshot (23)](https://github.com/rameshkumar359/Resume-Analysing-and-finding-job/assets/96288285/65e72e10-892c-4ca1-986d-9929f98b1c07)

# technologies used:
1.reading the uploaded pdf using pdfminer a python library.
2.extracting the data from pdf using python library pyresumeparser and nlp spacy en_core_web_sm.
3.using llm to analyse the resume here i used meta llama 2.
4.prompting llm to extract accurate information as required.
5.finding domain of the resume using llm.
6.then after giving our preferences like job location,domain,city the selenium driver open the tab automatically and scroll down to list jobs.
