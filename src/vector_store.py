# from langchain.text_splitter import CharacterTextSplitter
# from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
import warnings
from utils.logger import get_logger

from dotenv import load_dotenv
load_dotenv()

logger = get_logger(__name__)

# Capturar warnings y enviarlos al logger
def warning_to_logger(message, category, filename, lineno, file=None, line=None):
    """Captura warnings y los registra en el logger"""
    logger.critical(f"{category.__name__} in {filename}:{lineno} - {message}")

# Configurar warnings para que usen el logger
warnings.showwarning = warning_to_logger

class VectorStoreBuilder:
    def __init__(self, csv_path: str, persist_directory: str="chroma_db"):
        self.csv_path = csv_path
        self.persist_directory = persist_directory
        logger.info(f"Initializing VectorStoreBuilder with csv_path={csv_path}")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        logger.info("HuggingFace embeddings loaded successfully")

    def build_and_save_vectorstore(self):
        logger.info(f"Loading CSV data from {self.csv_path}")
        loader = CSVLoader(file_path=self.csv_path, metadata_columns=[])
        data = loader.load()

        logger.info(f"Number of documents loaded: {len(data)}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=0,
        )
        docs_split = splitter.split_documents(data)
        logger.info(f"Number of text chunks created: {len(docs_split)}")

        logger.info("Building vector store with Chroma...")
        Chroma.from_documents(documents=docs_split, embedding=self.embeddings, persist_directory=self.persist_directory)
        logger.info(f"Vector store saved to {self.persist_directory}")

    def load_vectorstore(self):
        logger.info(f"Loading vector store from {self.persist_directory}")
        db = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
        logger.info("Vector store loaded successfully")
        return db