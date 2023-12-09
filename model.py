import os
from langchain.document_loaders import PyMuPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate

global_filtered_qa_pairs = []

os.environ["OPENAI_API_KEY"] ='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'

persist_directory = "./storage"
pdf_path = "C:\\Users\\MSI-PC\Desktop\\AI Quiz Generator\\PDFs\\Data science Lecture.pdf"

loader = PyMuPDFLoader(pdf_path)
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
texts = text_splitter.split_documents(documents)

vectorstore = Chroma.from_documents(documents=texts, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

llm = ChatOpenAI()

# qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

template = """Use the following pieces of context to Generate the most important 5 MCQ Questions and give 4 answers for them 
but the first answer must be correct while the others are not, 
before the questions write the format "Q1:" and before answers "A1:" and return them in array format.
{context}"""
rag_prompt_custom = PromptTemplate.from_template(template)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt_custom
    | llm
    | StrOutputParser()
)
# QA = rag_chain.invoke("")
# print(QA)
# qa_pairs = QA.strip().split('\n')
# filtered_qa_pairs = list(filter(None, qa_pairs))
# print(filtered_qa_pairs)
# Check if the global variable is empty, then run the chain and store the result
if not global_filtered_qa_pairs:
    QA = rag_chain.invoke("")
    qa_pairs = QA.strip().split('\n')
    global_filtered_qa_pairs = list(filter(None, qa_pairs))

# Access the result stored in the global variable
print(global_filtered_qa_pairs)  # Use global_filtered_qa_pairs wherever you need in your code