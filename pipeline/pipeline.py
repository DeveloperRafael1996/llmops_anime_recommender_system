from src.vector_store import VectorStoreBuilder
from src.recommender import AnimeRecommender
from config.config import GROQ_API_KEY, MODEL_NAME
from utils.logger import get_logger 
from utils.custom_exception import CustomException

logger = get_logger(__name__)

class AnimeRecommendationPipeline:
    def __init__(self, persist_dir="chroma_db"):
        try:
            logger.info("Initializing Recommendation Pipeline")
            vector_builder = VectorStoreBuilder(csv_path="", persist_directory=persist_dir)
            retriever = vector_builder.load_vectorstore().as_retriever()
            
            logger.info("Vector Store loaded successfully")
            logger.info(retriever)


            self.recommender = AnimeRecommender(retriever,GROQ_API_KEY,MODEL_NAME)
            logger.info("Pipeline Initialized Successfully")
        except Exception as e:
            logger.error(f"Error initializing pipeline: {e}")
            raise CustomException("Failed to initialize AnimeRecommendationPipeline", e)

    def get_recommendations(self, query: str) -> str:
        try:
            logger.info(f"Getting recommendations for query: {query}")
            recommendations = self.recommender.get_recommendations(query)
            logger.info("Recommendations retrieved successfully")
            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            raise CustomException("Failed to get recommendations", e)    
        
    def get_recommendations_with_sources(self, query: str) -> str:
        try:
            logger.info(f"Getting recommendations with sources for query: {query}")
            response = self.recommender.get_recommendations_with_sources(query)
            
            logger.info(f"Sources retrieved: {len(response['sources'])} documents")
            logger.info(f"Source Documents: {response['sources']}")

            logger.info("Recommendations retrieved successfully")
            
            return response['recommendations']
        except Exception as e:
            logger.error(f"Error getting recommendations with sources: {e}")
            raise CustomException("Failed to get recommendations with sources", e)    