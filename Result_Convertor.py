import re
import time

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from itdepartment import (cleanMarks, cleanText, displayPDF, getSubjectCodes,
                          getSubjectNames, getTabledownloadLink, pdfToText,
                          studentDetails)
from utils import PdfProcessor


@st.cache_resource
def concat_subjects(d: dict):
    #function to concat subject wise marks
    return pd.concat([i for i in d.values()], axis=1)


@st.cache_resource
def cleanTextRe(text: str) -> str:
    text = re.sub(r'^[a-zA-Z]{2}', '', text)
    return text

@st.cache_resource
def extractPrnNo(text: str):
    # function to extract prn no from text
    pattern = re.findall(
        r'7\d{7}[a-zA-Z]*', text
    )
    d = {'PRN-NO': []}
    for i in pattern:
        temp = i.split()
        d['PRN-NO'].append(temp[0])

    return pd.DataFrame(d)

@st.cache_resource
def replaceNan(df: pd.DataFrame) -> pd.DataFrame:
    # function to replace nan values
    df = df.replace('nnn', np.nan)
    df = df.replace('nan', np.nan)
    df = df.replace('nnnn', np.nan)
    df = df.replace('nnnn', np.nan)
    df = df.replace('nan', np.nan)
    df = df.replace('nnnnn', np.nan)
    df = df.replace('nnnnn', np.nan)
    df = df.replace('nnnnnnn', np.nan)
    df = df.replace('nnnnnnn', np.nan)
    df = df.replace('nnn', np.nan)
    df = df.replace('nan', np.nan)
    df = df.replace('nnnn', np.nan)
    return df

def App():

   

    st.markdown("""
    ## :outbox_tray: Result Analyser :outbox_tray:

    ---

    **Disclaimer:** Please ensure that you enter unique subject codes for accurate analysis. Duplicate subject codes may lead to incorrect results and data inconsistency. Each subject code should be distinct and identifiable to maintain the integrity of the analysis.

    ---

    """, unsafe_allow_html=True)


                        

    col1, col2 = st.columns(2)

    with col1:
        department = st.selectbox(
            'Select Department',
            ('COMPUTER', 'IT', 'AIDS', 'MECHANICAL', 'E&TC',
                'CIVIL', 'ELECTRICAL', 'INSTRUMENTATION')
        )
        st.success(f'Selected department is {department}')

    with col2:
        year = st.selectbox(
            'SELECT YEAR',
            ('BE','TE','SE','FE')
        )
        st.success(f'Selected year is {year}')
    if department:
        
        pdf_file = st.file_uploader(label="Upload Pdf File", type="pdf")
        if pdf_file:
            # display document
            with st.expander(label="Show Uploaded File"):
                displayPDF(pdf_file)

            try:
                text = pdfToText(pdf_file)
            except FileNotFoundError:
                st.error('File not found try again!')
                return
            # store text to find subject names
            textForSubjectNames = text
            
            # subjectNamesList = []
            # # other departments than IT
            # if department !='IT':
            #     st.info('Enter subject Names')
            #     subjectNamesList = st.text_area(label="Enter subject Names(Each subject on separate line)")
            #     subjectNamesListBtn = st.button(label='Add Subjects')
            #     if subjectNamesListBtn and subjectNamesList:
            #         st.success('Selected subjects are')

            #         # convert string to list
            #         subjectNamesList = subjectNamesList.split('\n')
            #         st.write(subjectNamesList)

            #         # store the subjectNames in session state
            #         if 'subjectNamesList' not in st.session_state:
            #             st.session_state['subjectnamesList'] = subjectNamesList

            #     else:
            #         st.error('Subject Name must be added to work.')


            text = cleanText(text)
            try:

                seat_no_name = studentDetails(text)
                student_prn_no = extractPrnNo(text)

                student_data = pd.concat(
                    [seat_no_name, student_prn_no], axis=1)
            except Exception as e:
                st.error(
                    f"Error in extracting data from pdf. Please check the pdf file and try again. {e}")
                return

            # show progress bar
            # Create an empty container for the progress bar
            progressBar = st.progress(0, text='Processing File')
            for percentageComplete in range(100):
                time.sleep(0.05)
                progressBar.progress(percentageComplete + 1, text='Processing File')
            
            # hide progress bar after finish
            progressBar.empty()

            # with st.expander('Show Students Details'):
            #     # remove columns with all nan values
            #     student_data = student_data.dropna(axis=1, how='all')
            #     storeStudentData = student_data.copy()
                
            #     AgGrid(student_data)
            #     st.spinner('Processing...')
            #     time.sleep(4)
            #     st.text("")

            #     downloadButtonAllCol1,downloadButtonAllCol2 = st.columns(2)
            #     with downloadButtonAllCol1:
            #         st.download_button(
            #             'Download CSV File',
            #             data=storeStudentData.to_csv().encode('utf-8'),
            #             file_name=f"{str(pdf_file.name).split('.')[0]}.csv",
            #             mime='text/csv'
            #         )
            #     with downloadButtonAllCol2:
                
            #         st.markdown(getTabledownloadLink(
            #             df=storeStudentData,fileName=f"{str(pdf_file.name).split('.')[0]}.xlsx",), unsafe_allow_html=True)

            # with st.expander('Show Students Marks by Subject Code'):

            #     # text = cleanTextRe(text)
            #     subject_codes = st.text_input(
            #         'Enter subject code to see subject marks(One at at time)')
            #     subject_codes_submit = st.button(
            #         'Submit', key='one_subject_codes_submit')
            #     if subject_codes_submit:
            #         try:
            #             subject_codes = subject_codes.split()
            #             subject_codes = {i: None for i in subject_codes}
            #             st.markdown('#### Selected subjects')
            #             st.write(subject_codes)
            #             st.spinner('Processing...')
            #             pattern = r'[A-Z]{3}'
            #             text = cleanTextRe(text)
            #             text = re.sub(pattern, '', text)
            #             try:
            #                 marks = cleanMarks(text, subject_codes)
            #             except Exception as e:
            #                 st.error(
            #                     f'Error in processing pdf. Please check the pdf file and try again {e}')
            #                 return
                        
            #             try:
            #                 student_marks = concat_subjects(marks)
            #                 student_marks = pd.concat(
            #                     [student_data, student_marks], axis=1)
            #             except Exception as e:
            #                 st.error(
            #                     f'Error in extracting marks. Please check the pdf file and try again.@concat_subjects {e}')
            #                 return


            #             st.success('Done!....')
            #             # remove columns with all nan values
            #             # student_marks = replaceNan(student_marks)
            #             student_marks = student_marks.replace(
            #                 'nnnnnnn', np.nan)
            #             student_marks = student_marks.replace(
            #                 'nnnnnnn', np.nan)
            #             student_marks = student_marks.replace('nnn', np.nan)
            #             student_marks = student_marks.replace('nan', np.nan)
            #             student_marks = student_marks.replace('nnnn', np.nan)

            #             student_marks = student_marks.replace('nnn', np.nan)
            #             student_marks = student_marks.dropna(axis=1, how='all')
            #             studentMarksStore = student_marks.copy()

            #             AgGrid(student_marks)
                        
            #             st.spinner('Processing...')
            #             time.sleep(4)
            #             st.text("")

            #             downloadButtonCol1,downloadButtonCol2 = st.columns(2)
            #             with downloadButtonCol1:
            #                 st.download_button(
            #                     'Download CSV File',
            #                     data=studentMarksStore.to_csv().encode('utf-8'),
            #                     file_name=f"{str(pdf_file.name).split('.')[0]}.csv",
            #                     mime='text/csv'
            #                 )
            #             with downloadButtonCol2:
            #                 st.markdown(getTabledownloadLink(
            #                     df=studentMarksStore,fileName=f"{str(pdf_file.name).split('.')[0]}.xlsx",), unsafe_allow_html=True)
                            
                                        
            #         except Exception as e:
            #             st.error(f'Please enter valid subject code or cannot convert this marks {e}')
                        
            #             return

            with st.expander('Download Student marks in Excel/Csv File'):
                st.warning(
                    'Enter subject codes those are common for all student(Exclude honors courses)')
                subject_codes = st.text_input(
                    'Enter subject codes separated by space Example:  210241 210242')
                subject_codes_submit = st.button(
                    'Submit', key='all_subject_codes_submit')

                if subject_codes_submit:
                    try:
                        subject_codes = subject_codes.split()
                        subject_codes = {i: None for i in subject_codes}
                        st.markdown('### Selected subjects are :')
                        student_data = replaceNan(student_data)
                        st.write(subject_codes)
                        st.spinner('Processing...')
                        stored_text = text
                        text = cleanTextRe(text)
                        # pattern = r'[A-Z]\w*[A-Z]'
                        pattern = r'[A-Z]{3}'
                        text = re.sub(pattern, '', text)
                        # uncomment to log the data
                    
                        try:
                            marks = cleanMarks(text, subject_codes)
                        except Exception as e:
                            st.error(
                                f'Error in extracting marks. Please check the pdf file and try again.@cleanMarks {e}')
                            return
                        
                        try:

                            student_marks = concat_subjects(marks)
                            student_marks = pd.concat(
                                [student_data, student_marks], axis=1)
                        except Exception as e:
                            st.error(
                                f'Error in extracting marks. Please check the pdf file and try again.@concat_subjects {e}')
                            return
                        
                        student_marks = replaceNan(student_marks)

                        try:
                            # find sgpa
                            print('trying to extract spga')
                            pattern = re.findall(r'SGPA1?\W*\d*\W*\d*', stored_text)
                            # SGPA1: 8.3
                            d = {'sgpa':[],'score':[]}
                            for i in pattern:
                                try:
                                    temp = i.split()
                                    if len(temp) == 1:
                                        temp.append('00')
                                except Exception as e:
                                    temp = ['SGPA1','00']
                                d['sgpa'].append(temp[0])
                                d['score'].append(temp[1])
                            sgpa = pd.DataFrame(d)
                            student_marks = pd.concat([student_marks,sgpa],axis=1)
                        except:
                            print('error in extracting spga')
                            st.error('Error in extracting sgpa')
                            pass

                        

                        student_marks = student_marks.dropna(axis=1, how='all')

                        # st.markdown(getTabledownloadLink(
                        #     student_marks), unsafe_allow_html=True)

                        downloadButtonAllCol1,downloadButtonAllCol2 = st.columns(2)
                        with downloadButtonAllCol1:
                            st.download_button(
        'Download CSV File',
        data=student_marks.to_csv().encode('utf-8'),
        file_name=f"{str(pdf_file.name).split('.')[0]}.csv",
        mime='text/csv',
        key=f"download_csv_{pdf_file.name}"
                            )
                        with downloadButtonAllCol2:
                        
                             st.markdown(getTabledownloadLink(
        df=student_marks, fileName=f"{str(pdf_file.name).split('.')[0]}.xlsx"), unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error(
                            f'Please enter valid subject codes OR Cannot convert following subject codes to excel file {e}')
                        return

            with st.expander('Advance subject wise marks'):
                st.warning('Use this feature only if above feature is not working')
                st.warning('Keep default values if you are not sure')

                result_type = st.selectbox(
                    'Select result type', ['SEMESTER', 'YEAR'])
                st.write('You selected:', result_type)
                
                # IF SEMESTER RESULT then 10 SUBJECTS ELSE 20
                if result_type == 'SEMESTER':
                    options = st.multiselect(
                        'select subject codes',
                        getSubjectCodes(text,10)
                    )
                else:
                    options = st.multiselect(
                        'select subject codes',
                        getSubjectCodes(text,20)
                    )

                
                st.write('Selected subject codes:', options)

                if options:

                    subject_names = st.multiselect(
                        'select subject names',
                        list(set(getSubjectNames(textForSubjectNames)))
                    )
                    st.write('Selected subject names:', subject_names)

                subject_codes = st.text_input(
                    'Enter subject code')
                
                subject_name = st.text_input(
                    "Enter subject name"
                )
                pattern = st.selectbox(
                            options=['[A-Z]{3}','[A-Z]\w*[A-Z]'],
                            label='Try changing pattern if not working(Select one) optional',

                    )
                subject_codes_submit = st.button(
                    'Submit', key='one_subject_codes_submit_advance')
                if subject_codes_submit:
                    try:
                        subject_codes = subject_codes.split()
                        subject_codes = {i: None for i in subject_codes}
                        st.markdown('#### Selected subjects')
                        st.write(subject_codes)
                        st.spinner('Processing...')
                        


                        text = cleanTextRe(text)
                        text = text.replace(subject_name,'')
                        text = re.sub(pattern, '', text)
                        try:
                            marks = cleanMarks(text, subject_codes)
                        except:
                            st.error(
                                'Error in processing pdf. Please check the pdf file and try again')
                            return
                        
                        try:
                            student_marks = concat_subjects(marks)
                            student_marks = pd.concat(
                                [student_data, student_marks], axis=1)
                        except:
                            st.error(
                                'Error in extracting marks. Please check the pdf file and try again.@concat_subjects')
                            return


                        st.success('Done!....')
                        # remove columns with all nan values
                        student_marks = replaceNan(student_marks)
                        student_marks = student_marks.dropna(axis=1, how='all')
                        studentMarksStore = student_marks.copy()

                        AgGrid(student_marks)
                        
                        st.spinner('Processing...')
                        time.sleep(4)
                        st.text("")


                        downloadButtonAdvanceCol1,downloadButtonAdvanceCol2 = st.columns(2)
                        with downloadButtonAdvanceCol1:
                            st.download_button(
                                'Download CSV File',
                                data=studentMarksStore.to_csv().encode('utf-8'),
                                file_name=f"{str(pdf_file.name).split('.')[0]}.csv",
                                mime='text/csv'
                            )
                        with downloadButtonAdvanceCol2:
                        
                            st.markdown(getTabledownloadLink(
                                df=studentMarksStore,fileName=f"{str(pdf_file.name).split('.')[0]}.xlsx",), unsafe_allow_html=True)
                    except:
                        st.error('Please enter valid subject code or cannot convert this marks')
                        
                        return



    else:
        st.write('selected department is ', department)


if __name__ == "__main__":

    # set page title and icon
    try:
        st.set_page_config(
            page_title='Result Analysis',
            page_icon='📃',
        )
        with st.sidebar:
        #     st.header('Our Contributors')
        #     contributors = [
        #     "SATYA PRAKASH RAJ",
        #     "SHUBHIKA SHREE"
        # ]
        #     for contributor in contributors:
        #         st.write(contributor)

   
        

            import streamlit as st

            st.markdown(
                """
                <style>
                    /* Add CSS styles here */
                    .avatar-container {
                        display: inline-block;
                        margin-right: 20px; /* Adjust the margin to your desired spacing */
                    }
                </style>        
                """,
                unsafe_allow_html=True
            )


    except Exception as e:
        pass

    App()
