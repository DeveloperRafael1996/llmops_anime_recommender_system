import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv

st.set_page_config(page_title="Anime Recommendation System", page_icon=":books:")
load_dotenv()

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


