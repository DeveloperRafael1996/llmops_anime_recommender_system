import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
from utils.logger import get_logger
import warnings

st.set_page_config(page_title="Anime Recommendation System", page_icon=":books:")
load_dotenv()

logger = get_logger(__name__)

# Capturar todos los warnings y enviarlos al logger
def warning_to_logger(message, category, filename, lineno, file=None, line=None):
    """Captura warnings (incluyendo deprecaciones de LangChain) y los registra"""
    logger.critical(f"{category.__name__}: {message} (in {filename}:{lineno})")

warnings.showwarning = warning_to_logger

logger.info("🎌 Starting Anime Recommendation System")

@st.cache_resource
def initialize_pipeline():
    pipeline = AnimeRecommendationPipeline()
    return pipeline

pipeline = initialize_pipeline()
st.title("Anime Recommendation System")
user_query = st.text_input("Enter your anime prefernces eg. : light hearted anime with school settings | i want similar anime to naruto")

if user_query:
    with st.spinner("Fetching recommendations..."):
        try:
            # recommendations = pipeline.get_recommendations(user_query)
            recommendations = pipeline.get_recommendations_with_sources(user_query)
            st.markdown("### Recommended Anime:")
            st.write(recommendations)
        except Exception as e:
            st.error(f"An error occurred: {e}")


