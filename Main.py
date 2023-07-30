import streamlit as st
import os
from Secret_key import openai_api_key
import csv_utils
import pdf_utils
#from csv_utils import get_answer_csv
#from pdf_utils import get_answer_pdf
#os.environ["OPENAI_API_KEY"]=openai_api_key

def main():
    st.set_page_config(page_title="Load PDF/CSV/TEXT for semantic search")
    st.header("PDF/CSV/TEXT Q&A Bot")
    #st.markdown("Upload a PDF file/CSV file/Text file and ask questions about its content using Natural Language Processing!")
    #col1, col2 = st.columns(2)
    pdf_or_csv_or_txt=st.file_uploader("Load: PDF file/CSV file/Text file:",type=["pdf",'csv','txt'])  #,accept_multiple_files=True #for uploaded_file in uploaded_files: bytes_data = uploaded_file.read()
    if pdf_or_csv_or_txt is not None:
        try:
            file_extension = os.path.splitext(pdf_or_csv_or_txt.name)[1].lower()
            #st.write(file_extension)
            if file_extension == ".csv":
                #st.write("csv in")
                query=st.text_input("Ask a Question From Uploaded Files")
                button=st.button("Submit")
                if button:
                    #print("function start")
                    st.write(csv_utils.get_answer_csv(pdf_or_csv_or_txt,query))
                
            elif file_extension == ".txt":
                query=st.text_input("Ask a Question From Uploaded Files")
                button=st.button("Submit")
                if button:
                    #print("out pdf")
                    file_contents = pdf_or_csv_or_txt.read()
                    text_content = file_contents.decode("utf-8")
                    #st.write(text_content)
                    st.write(pdf_utils.FiassVectordb(text_content,query))
                
            elif file_extension == ".pdf":
                full_text=pdf_utils.pdftotext(pdf_or_csv_or_txt)
                query=st.text_input("Ask a Question From Uploaded Files")
                button=st.button("Submit")
                if button:
                    #print("out pdf")
                    st.write(pdf_utils.FiassVectordb(full_text,query))
                    #print("in pdf")
                #pdftotext(pdf_or_csv_or_txt)
                #pdf_file_path = save_uploaded_pdf(pdf)
                #text=langchain_pdf_totext(pdf)

            
            
            

        except:
            st.write("Unsupported file type. Please upload a CSV, TXT, or PDF file.")

        #finally:
            #if pdf_file_path and os.path.exists(pdf_file_path):
                #os.remove(pdf_file_path)
        



if __name__=='__main__':
    main()


