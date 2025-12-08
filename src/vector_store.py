# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from dotenv import load_dotenv
load_dotenv()

class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_directory: str="chroma_db"):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_and_save_vectorstore(self):
        loader = CSVLoader(file_path=self.csv_path,metadata_columns=[])
        data = loader.load()

        print(f"Number of documents loaded in directory: {len(data)}")


        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
        )
        docs_split = splitter.split_documents(data)
        print(f"Number of text chunks created: {len(docs_split)} \n")


        Chroma.from_documents(documents=docs_split, embedding=self.embeddings, persist_directory=self.persist_directory)
        # db.persist()

    def load_vectorstore(self):
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        return db