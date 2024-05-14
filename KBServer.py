import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone , Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
import pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.llms import OpenAI
from langchain_community.vectorstores import Pinecone
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage




llm = ChatOpenAI(model="gpt-3.5-turbo-0125", api_key=os.environ.get("OPEN_API_KEY"), temperature=0.3)



txt_loader=DirectoryLoader('./Documents',glob="**/*.txt")
docx_loader=DirectoryLoader('./Documents',glob="**/*.docx")
pptx_loader=DirectoryLoader('./Documents',glob='**/*.pptx')
xlsx_loader=DirectoryLoader('./Documents',glob='**/*.xlsx')

#take all loader
loaders=[txt_loader,docx_loader,xlsx_loader,pptx_loader]
#lets create document
documents = []
for loader in loaders:
    documents.extend(loader.load())


# Split the text from the documents

text_splitter=CharacterTextSplitter(chunk_size=1000,chunk_overlap=40)
documents = text_splitter.split_documents(documents)
print(len(documents))

#Embeddings and storing it in vector store

embeddings = OpenAIEmbeddings()

# Using pinecone for storing vectors

os.environ['PINECONE_API_KEY']="469893d2-888e-4294-8b0d-e72b36f33724"

#initialize the pinecone
index_name="langchain-demo"
vectorstore=PineconeVectorStore.from_documents(documents,embeddings,index_name=index_name)




# Now langchain part (Chaining with chat history )
retriever = vectorstore.as_retriever(search_type='similarity',search_kwargs={"k":10})
qa=ConversationalRetrievalChain.from_llm(llm,retriever)
chat_history=[]

def generate_response(prompt):
    user_input = prompt
    result=qa({
        "question":user_input,
        "chat_history":chat_history
    })
    chat_history.append((user_input,result['answer']))
    # return str(result["answer"])
    return result


