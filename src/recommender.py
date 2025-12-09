from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.prompt_template import get_anime_prompt
from utils.logger import get_logger

logger = get_logger(__name__)


class AnimeRecommender:
    def __init__(self, retriever, api_key: str, model_name: str):
        self.llm = ChatGroq(api_key=api_key, model_name=model_name, temperature=0)
        self.prompt = get_anime_prompt()
        self.retriever = retriever

        # Crear la cadena RAG usando LCEL (LangChain Expression Language)
        def format_docs(docs):
            format = "\n\n".join(doc.page_content for doc in docs)

            logger.warning(f"Formatted {len(docs)} documents for LLM input.")
            # logger.warning(f"Formatted Documents Content: {format}")
            return format

        # Chain before LLM to format documents
        ''' 
            self.chain_before_llm = (
                {
                    "context": self.retriever | format_docs,
                    "question": RunnablePassthrough()
                }
                | self.prompt
            )
        '''
        
        self.qa_chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_recommendations(self, query: str):
        # Calling the chain to get recommendations to prompt
        '''
            prompt_value = self.chain_before_llm.invoke(query)
            logger.info(f"Prompt sent to LLM: {prompt_value.to_string()}")
        ''' 
        
        """get recommendations based on user query"""
        result = self.qa_chain.invoke(query)
        return result
    
    def get_recommendations_with_sources(self, query: str):
        """get recommendations and the source documents used"""
        source_docs = self.retriever.invoke(query)
        recommendations = self.qa_chain.invoke(query)

        return {
            'recommendations': recommendations,
            'sources': source_docs
        }