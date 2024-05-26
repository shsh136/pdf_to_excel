import base64
import io
import os
import re
from typing import List

import pandas as pd
import pypdf
import streamlit as st


def getSubjectNames(text):
    pattern = r"\d{6}\s(.+?)\s\s\*"
    subject_names = re.findall(pattern, text)
    return subject_names


def getSubjectCodes(text: str,subjectCodeCount:int) -> list:
    pattern = re.findall(r'[1-4]{1}\d{4,6}\w{1}', text)
    # return a list of top 10 element having maximum occurence
    d = {}
    for i in pattern:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return list(dict(sorted(d.items(), key=lambda item: item[1], reverse=True)).keys())[:subjectCodeCount]


def studentDetails(text: str):
    l = []
    pattern = re.findall(
        r'[FSTB]\d{9}\s*\w*\s*\w*\s*\w*\s*\w*\w*\s*\w*\s*\w*\s*\w*\s*', text)
    d = {'seat_no': [], 'name': []}
    for i in pattern:
        # split the string
        temp = i.split()
        d['seat_no'].append(temp[0])
        d['name'].append(temp[1]+' '+temp[2]+' '+temp[3])
        dataframe = pd.DataFrame(d)
    return dataframe


def studentSgpa(text: str):
    pattern = re.findall(r'SGPA1\W*\d*\W*\d*', text)
    # SGPA1: 8.3
    d = {'sgpa':[],'score':[]}
    for i in pattern:
        temp = i.split()
        d['sgpa'].append(temp[0])
        d['score'].append(temp[1])
    return pd.DataFrame(d)

def getTabledownloadLink(df: pd.DataFrame,fileName=str):
    """Generates a link allowing the data in a given panda dataframe to be downloaded as an Excel file.
    """
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    b64 = base64.b64encode(excel_buffer.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{fileName}">Download Excel file</a>'
    return href


def cleanText(text: str, year: str = 'SE') -> str:
    SE_SUBJECTS_END = [
        "DISCRETE MATHEMATICS",
        "DIGITAL ELEC. & LOGIC DESIGN ",  
        "FUND. OF DATA STRUCTURES ",       
        " OBJECT ORIENTED PROGRAMMING",                       
        "DIGITAL ELEC. LABORATORY",               
        " DATA STUCTURES LABORATORY",                   
        " OOP & COMP. GRAPHICS LAB. ",         
        "BUSINESS COMMUNICATION SKILLS",                           
        " HUMANITY & SOCIAL SCIENCE",
        " ENVIRONMENTAL STUDIES",
        "SMART CITIES ",                  
        "ENGINEERING MATHEMATICS III",                      
        "MICROPROCESSOR",                        
        "DATA STRUCTURES & ALGO.",           
        " SOFTWARE ENGINEERING",                    
        "PRINCIPLES OF PROG. LANG. ",   
        " DATA STRUCTURES & ALGO. LAB.",    
        " MICROPROCESSOR LABORATORY",                    
        " PROJECT BASED LEARNING II",                 
        "CODE OF CONDUCT ", 
        "WATER MANAGEMENT ","THE SCIENCE OF HAPPINESS",
    ]

    subjects = [
        'DISCRETE MATHEMATICS', 
        'FUND. OF DATA STRUCTURES', 
        'OBJECT ORIENTED PROGRAMMING', 
        'COMPUTER GRAPHICS', 
        'DIGITAL ELEC. & LOGIC DESIGN', 
        'DATA STUCTURES LABORATORY', 
        'OOP & COMP. GRAPHICS LAB.', 
        'DIGITAL ELEC. LABORATORY', 
        'BUSINESS COMMUNICATION SKILLS', 
        'HUMANITY & SOCIAL SCIENCE', 
        'ENVIRONMENTAL STUDIES',
        'SMART CITIES ',
        'ENGINEERING MATHEMATICS III', 
        'ENGINEERING MATHEMATICS III', 
        'DATA STRUCTURES & ALGO.', 
        'SOFTWARE ENGINEERING', 
        'MICROPROCESSOR', 
        'PRINCIPLES OF PROG. LANG.', 
        'DATA STRUCTURES & ALGO. LAB.', 
        'MICROPROCESSOR LABORATORY', 
        'PROJECT BASED LEARNING II', 
        'CODE OF CONDUCT',
        'THE SCIENCE OF HAPPINESS',
        'WATER MANAGEMENT'
    ]
    
    if year == 'SE':
        for subject in SE_SUBJECTS_END:
            text = text.replace(subject, '')

        for i in subjects:
            text = text.replace(i, '')   
    else:
        for i in subjects:
            text = text.replace(i, '')
        for subject in SE_SUBJECTS_END:
            text = text.replace

    text = text.replace('SYSTEMS IN MECH. ENGG.', '')
    text = text.replace('SYSTEMS IN MECH. ENGG.', '')
    text = text.replace('BASIC ELECTRONICS ENGG.', '')
    text = text.replace('BASIC ELECTRONICS ENGG.', '')
    text = text.replace('ENGINEERING MATHEMATICS I', '')
    text = text.replace('ENGINEERING MATHEMATICS I', '')
    text = text.replace('ENGINEERING CHEMISTRY', '')
    text = text.replace('ENGINEERING CHEMISTRY', '')
    text = text.replace('PROG. & PROBLEM SOLVING', '')
    text = text.replace('PROG. & PROBLEM SOLVING WORKSHOP', '')
    text = text.replace('ENVIRONMENTAL STUDIES-I', '')
    text = text.replace('ENGINEERING MECHANICS', '')
    text = text.replace('ENGINEERING MECHANICS', '')
    text = text.replace('ENGINEERING GRAPHICS', '')
    text = text.replace('ENGINEERING GRAPHICS', '')
    text = text.replace('BASIC ELECTRICAL ENGG.', '')
    text = text.replace('BASIC ELECTRICAL ENGG.', '')
    text = text.replace('ENGINEERING PHYSICS', '')
    text = text.replace('ENGINEERING PHYSICS', '')
    text = text.replace('ENGINEERING MATHEMATICS II', '')
    text = text.replace('ENGINEERING MATHEMATICS II', '')
    text = text.replace('PROJECT BASED LEARNING', '')
    text = text.replace('ENVIRONMENTAL STUDIES-II', '')
    text = text.replace('PHY.EDU. -EXER. & FIELD ACTI.', '')
    text = text.replace('DEMORACY, ELECTION AND GOV.', '')
    text = text.replace(
        'COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP ', '')
    text = text.replace('DYPP', '')

    # text = text.replace('DESIGN AND ANALYSIS OF ALGORITHMS', '')
    # text = text.replace('MACHINE LEARNING', '')
    # text = text.replace('BLOCKCHAIN TECHNOLOGY', '')
    # text = text.replace('CYBER SECURITY AND DIGITAL FORENSICS', '')
    # text = text.replace('SOFTWARE TESTING AND QUALITY ASSURANCE', '')
    # text = text.replace('LABORATORY PRACTICE IIII', '')
    # text = text.replace('LABORATORY PRACTICE IV', '')
    # text = text.replace('PROJECT STAGE I', '')
    # text = text.replace('AUDIT COURSE 7', '')
    # text = text.replace('HIGH PERFORMANCE COMPUTING', '')
    # text = text.replace('DEEP LEARNING', '')
    # text = text.replace('NATURAL LANGUAGE PROCESSING', '')
    # text = text.replace('PATTERN RECOGNITION', '')
    # text = text.replace('BUSINESS INTELLIGENCE', '')
    # text = text.replace('LABORATORY PRACTICE V', '')
    # text = text.replace('LABORATORY PRACTICE VI', '')
    # text = text.replace('PROJECT STAGE II', '')
    # text = text.replace('AUDIT COURSE 8', '')


    # BE subjects
    text = text.replace(' DESIGN & ANALYSIS OF ALGO.', '')
    text = text.replace('MACHINE LEARNING', '')
    text = text.replace('BLOCKCHAIN TECHNOLOGY', '')
    text = text.replace('CYBER SEC. & DIG. FORENSICS.', '')
    text = text.replace('OBJ. ORIENTED MODL. & DESG. ', '')
    text = text.replace('SOFT. TEST. & QLTY ASSURANCE', '')
    text = text.replace('LABORATORY PRACTICE - III', '')
    text = text.replace('LABORATORY PRACTICE - IV', '')
    text = text.replace('PROJECT STAGE - I', '')
    text = text.replace('ENTERPRENEURSHIP DEVELOPMENT', '')
    text = text.replace('BOTNET OF THINGS', '')
    text = text.replace('3D PRINTING', '')
    text = text.replace('HIGH PERFORMANCE COMPUTING', '')
    text = text.replace('DEEP LEARNING', '')
    text = text.replace('NATURAL LANGUAGE PROCESSING', '')
    text = text.replace('PATTERN RECOGNITION', '')
    text = text.replace('BUSINESS INTELLIGENCE', '')
    text = text.replace('LABORATORY PRACTICE - V', '')
    text = text.replace('LABORATORY PRACTICE - VI', '')
    text = text.replace('PROJECT STAGE II','')
    text = text.replace('CONVERSATIONAL INTERFACES', '')
    text = text.replace('SOCIAL MEDIA AND ANALYTICS ', '')   
    text = text.replace('TOTAL GRADE POINTS / TOTAL CREDITS','')
    text = text.replace('FOURTH YEAR','')
    text = text.replace('SE SGPA','')
    text = text.replace('FE SGPA','')
    text = text.replace('TE SGPA','')
    text = text.replace('FIRST CLASS WITH DISTINCTION','')
    text = text.replace('CGPA','')
   

    # text = text.replace('TOTAL GRADE POINTS / TOTAL CREDITS', '')
    # text = text.replace('FOURTH YEAR', '')
    # text = text.replace('SE SGPA', '')
    # text = text.replace('FE SGPA', '')
    # text = text.replace('TE SGPA', '')
    # text = text.replace('BE SGPA', '')

    # text = text.replace('FIRST CLASS WITH DISTINCTION', '')
    # text = text.replace('CGPA', '')

    text = text.replace('DATABASE MANAGEMENT SYSTEMS', '')
    text = text.replace('THEORY OF COMPUTATION', '')
    text = text.replace('SYS. PROG & OPERATING SYS.', '')
    text = text.replace('COMPUTER NETWORKS AND SEC.', '')
    text = text.replace('INT. OF THINGS & EBD. SYS ', '')
    text = text.replace('SOFTWARE PROJECT MANAGEMENT', '')
    text = text.replace('DATABASE MGMT. SYS. LAB.', '')
    text = text.replace('COMP. NET. AND SEC. LAB.', '')
    text = text.replace('LABORATORY PRACTICE I', '')
    text = text.replace('SEMINAR AND TECH. COMN. ', '')
    text = text.replace('CYBER SECURITY ', '')
    text = text.replace('PROF. ETH. & ETIQUETTES 3.', '')
    text = text.replace('LEARN NEW SKILLS ', '')
    text = text.replace('DATA SCI & BIG DATA ANA.', '')
    text = text.replace('WEB TECHNOLOGY', '')
    text = text.replace('ARTIFICIAL INTELLIGENCE', '')
    text = text.replace('CLOUD COMPUTING', '')
    text = text.replace('SOFTWARE MODELING AND ARCHITECTURES', '')
    text = text.replace('INTERNSHIP', '')
    text = text.replace('DATA SCI & BIG DATA ANA.', '')
    # text = text.replace('DATA SCI & BIG DATA ANA. LAB.', '')
    text = text.replace('WEB TECHNOLOGY', '')      
    text = text.replace('LABORATORY PRACTICE-II ', '')
    text = text.replace('SUSTAINABLE ENERGY SYSTEMS', '')
    text = text.replace('LEARN NEW SKILLS', '')
    text = text.replace('LAB.', '')

    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,S.E.(2019 CREDIT PAT.) EXAMINATION,  APR/MAY 2023', '')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,F.E.(2019 CREDIT PAT.) EXAMINATION, MAY 2021', '')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY, S.E.(2019 COURSE) EXAMINATION,MAY 2019', '')
    text = text.replace('SAVITRIBAI PHULE PUNE UNIVERSITY ,T.E.(2019 COURSE) EXAMINATION, OCT/NOV 2021', '')
    text = text.replace('COLLEGE    : D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace('COLLEGE: [CEGP010530] - D.Y. PATIL COLLEGE OF ENGINEERING,  PUNE', '')
    text = text.replace('BRANCH CODE:  05', '')
    text = text.replace(' BRANCH CODE:  19-S.E.(2019 PAT.)(COMPUTER)  ', '')
    text = text.replace('BRANCH CODE: 19-T.E.(2019 PAT.)(COMPUTER)', '')
    text = text.replace('DATE       : 23 JUL 2019', '')
    text = text.replace('DATE : 06 MAY 2022', '')
    text = text.replace('............CONFIDENTIAL- FOR VERIFICATION AND RECORD ONLY AT COLLEGE, NOT FOR DISTRIBUTION.......................................', '')
    text = text.replace('....................................................................................................', '')
    text = text.replace('............                  .......  .......  .......  .......  .......  .......  ...  ...  ...   ... ...  ... ...', '')

    text = text.replace('PAGE :-', '')
    text = text.replace('SEAT NO.', '')
    text = text.replace('SEAT NO.:', '')
    text = text.replace('NAME :', '')
    text = text.replace('MOTHER :', '')
    text = text.replace('PRN :', '')
    text = text.replace('CLG.: DYPP[8]', '')

    text = text.replace('..............................', '')
    text = text.replace('SEM.:1', '')
    text = text.replace('SEM.:2', '')
    text = text.replace('COURSE NAME                      ISE      ESE     TOTAL      TW       PR       OR    Tot% Crd  Grd   GP  CP ', '')
    text = text.replace('DYPP', '')
    text = text.replace('Grd   Crd', '')
    text = text.replace('SEM. 2', '')
    text = text.replace('SEM. 1', '')
    text = text.replace('~', '')
    text = text.replace(' .', '')
    text = text.replace('*', ' ')
    text = text.replace(':', ' ')
    text = text.replace('-', 'n')
    text = text.replace('FIRST YEAR SGPA :', '')
    text = text.replace('TOTAL CREDITS EARNED ', '')
    text = text.replace('SECOND YEAR SGPA', '')
    text = text.replace('TOTAL CREDITS EARNED ', '')
  
    text = text.strip()
    return text


def displayPDF(file):
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_resource
def pdfToText(path):
    reader = pypdf.PdfReader(path)
    noOfPages = len(reader.pages)
    with open('extractedText.txt', 'w') as file:
        for line in range(0, noOfPages):
            page = reader.pages[line]
            file.write(page.extract_text())
    with open('extractedText.txt', 'r') as file:
        text = file.read()
    if os.path.exists('extractedText.txt'):
        os.remove('extractedText.txt')
    return text


def showUploadedFile(file):
    f = pd.read_csv(file)
    return f


# def cleanMarks(text: str, subject_codes) -> dict:
#     """
#     This function will clean the marks from the pdf file.
#     """
#     for codes in subject_codes.keys():
#         # Improved regex pattern to handle grades with '+' character
#         pattern = re.findall(
#             fr'{codes}[A-Z]?\s+\w+[\/!#&$@ \*~]*\w*\s*\w*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s*[A-Z\+\w]*\s*[\d]*\s*[\d]*\s', text)

#         # DataFrame column names
#         d = {'subject': [], 'ISE': [], 'ESE': [], 'TOTAL': [], 'TW': [], 'PR': [], 'OR': [], 'TOT': [], 'Tot%': [], 'CRD': [], 'GRD': [], 'GP': [], 'CP': []}

#         for index, i in enumerate(pattern):
#             temp = i.split()

#             # Ensure we handle cases where there are missing fields by appending empty strings
#             if len(temp) < 13:
#                 while len(temp) != 13:
#                     temp.append('')

#             # Append the data to the corresponding lists in the dictionary
#             d['subject'].append(temp[0])
#             d['ISE'].append(temp[1])
#             d['ESE'].append(temp[2])
#             d['TOTAL'].append(temp[3])
#             d['TW'].append(temp[4])
#             d['PR'].append(temp[5])
#             d['OR'].append(temp[6])
#             d['TOT'].append(temp[7])
#             d['Tot%'].append(temp[8])
#             d['CRD'].append(temp[9])
#             d['GRD'].append(temp[10])
#             d['GP'].append(temp[11])
#             d['CP'].append(temp[12])

#         # Create a DataFrame from the dictionary
#         dataframe = pd.DataFrame(d)
#         subject_codes[codes] = dataframe

#     return subject_codes




def cleanMarks(text: str, subject_codes) -> dict:
    """
    This function will clean the marks from the pdf file.
    """
    for codes in subject_codes.keys():
        # Improved regex pattern to handle grades with '+' character and empty fields
        pattern = re.findall(
            fr'{codes}[A-Z]?\s+\w+(?:[\/!#&$@ \*~^]*\w*)*\s+[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\/!#&$@ \*~^]*\w*\s*[\+]*\w*\s*\+*\w*\s*\+*\w*\s*\w*\+*\s*\w*\s*\+*\w*\s*[A-Z\+\w]*\s*[\d]*\s*[\d]*\s*', text)

        # DataFrame column names
        d = {'subject': [], 'ISE': [], 'ESE': [], 'TOTAL': [], 'TW': [], 'PR': [], 'OR': [], 'TOT': [], 'Tot%': [], 'CRD': [], 'GRD': [], 'GP': [], 'CP': []}

        # for index, i in enumerate(pattern):
        #     temp = i.split()


        subject_count = {code: 0 for code in subject_codes}

        for index, i in enumerate(pattern):
            temp = i.split()
            subject_code = temp[0]
            if subject_code in subject_count:
                subject_count[subject_code] += 1
                if subject_count[subject_code] > 1:
                    # Append "_<count>" to handle multiple occurrences
                    subject_code = f"{subject_code}_{subject_count[subject_code]}"





            # Ensure we handle cases where there are missing fields by appending empty strings
            if len(temp) < 13:
                while len(temp) != 13:
                    temp.append('')

            # Append the data to the corresponding lists in the dictionary
            d['subject'].append(temp[0])
            d['ISE'].append(temp[1])
            d['ESE'].append(temp[2])
            d['TOTAL'].append(temp[3])
            d['TW'].append(temp[4])
            d['PR'].append(temp[5])
            d['OR'].append(temp[6])
            d['TOT'].append(temp[7])
            d['Tot%'].append(temp[8])
            d['CRD'].append(temp[9])
            d['GRD'].append(temp[10])
            d['GP'].append(temp[11])
            d['CP'].append(temp[12])

        # Create a DataFrame from the dictionary
        dataframe = pd.DataFrame(d)
        subject_codes[codes] = dataframe

    return subject_codes
