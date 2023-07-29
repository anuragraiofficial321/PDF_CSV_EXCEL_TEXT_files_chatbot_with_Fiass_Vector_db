from Secret_key import openaikey
import os 
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
import streamlit as st
from PyPDF2 import PdfReader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import getpass
from langchain.callbacks import get_openai_callback
import uuid

#os.environ['OPENAI_API_KEY'] = getpass.getpass(openaikey)

os.environ["OPENAI_API_KEY"]=openaikey

TEMP_DIR = "temp_pdfs"

def save_uploaded_pdf(uploaded_pdf):
    TEMP_DIR = "temp_pdfs"
    os.makedirs(TEMP_DIR, exist_ok=True)
    file_name = f"{str(uuid.uuid4())}.pdf"
    file_path = os.path.join(TEMP_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(uploaded_pdf.read())
    return file_path


def langchain_pdf_totext(pdffile):
    loader = PyPDFLoader(pdffile)
    pages = loader.load_and_split()
    full_text = "\n\n".join(page.page_content for page in pages)
    return full_text


def convert_pdf_to_text(pdf_file):
    pdf_reader =PdfReader(pdf_file)
    #txt_file = open("temp_pdf_text.txt", "w",encoding='utf-8')
    full_text=""
    for i in pdf_reader.pages:
        full_text+=i.extract_text()
        #txt_file.write(full_text)
    #print(len(full_text))
    #txt_file.close()
    return full_text


def question_ask(col2):
    db = FAISS.load_local("fiass_doc_idx",OpenAIEmbeddings())
    question_answer=col2.text_input("Ask a Question From Uploaded Files")

    if question_answer:
        st.header("Question Answering Results")
        docs=db.similarity_search(question_answer)
        llm=OpenAI()
        chain=load_qa_chain(llm,chain_type="stuff")
        with get_openai_callback() as cb:
            response=chain.run(input_documents=docs, question=chain)
        
        if response:
            st.write(response)


def main():
    st.set_page_config(page_title="Load PDF for semantic search")
    st.header("PDF Q&A Bot")
    st.markdown("Upload a PDF file and ask questions about its content using Natural Language Processing!")
    col1, col2 = st.columns(2)
    pdf=col1.file_uploader("Load PDF file",type="pdf")  
    if pdf is not None:
        try:
            text=convert_pdf_to_text(pdf)
            #pdf_file_path = save_uploaded_pdf(pdf)
            #text=langchain_pdf_totext(pdf)

            text_splitter = CharacterTextSplitter(        
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
             )
            chunks = text_splitter.split_text(text)
            
            db = FAISS.from_texts(chunks, OpenAIEmbeddings())
            db.save_local("fiass_doc_idx")
            st.success("PDF processing and indexing completed successfully!")
            question_ask(col2)
            #db = FAISS.from_documents(chunks, OpenAIEmbeddings())
            
            

        except Exception as e:
            st.error(f"An error occurred: {e}")

        #finally:
            #if pdf_file_path and os.path.exists(pdf_file_path):
                #os.remove(pdf_file_path)
        



if __name__=='__main__':
    main()


