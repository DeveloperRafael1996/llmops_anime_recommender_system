from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting To Build Anime Recommendation Pipeline...")
        loader = AnimeDataLoader("data/anime_with_synopsis.csv", "data/processed_anime.csv")
        proceseed_csv = loader.load_and_process()
        logger.info(f"Data Loaded and Processed: {proceseed_csv}")

        vector_builder = VectorStoreBuilder(proceseed_csv)
        vector_builder.build_and_save_vectorstore()
        logger.info("Vector Store Built and Saved Successfully")
        logger.info("Anime Recommendation Pipeline Built Successfully")
        
    except Exception as e:
        logger.error(f"Error in Anime Recommendation Pipeline: {e}")
        raise CustomException("Failed to run Anime Recommendation Pipeline", e)
    

if __name__ == "__main__":
    main()
