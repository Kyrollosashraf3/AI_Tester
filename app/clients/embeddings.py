from typing import List
from openai import OpenAI, APIError, AuthenticationError, RateLimitError
from app.config import settings
import os 
from dotenv import load_dotenv
from app.config.logger import get_logger

load_dotenv()

DEFAULT_EMBEDDING_MODEL = "text-embedding-ada-002"


class EmbeddingError(Exception):
    pass


def generate_embeddings(texts: List[str], model: str = None) -> List[List[float]]:
    if not texts:
        return []

    api_key_env = "OPENAI_API_KEY"
    api_key = os.environ.get(api_key_env)
    if not api_key:
            logger.error(f"Missing {api_key_env} environment variable")
            raise ValueError(f"Missing {api_key_env} environment variable")
    
    model = model or DEFAULT_EMBEDDING_MODEL
    
    try:
        client = OpenAI(api_key=api_key)
        non_empty_texts = [text for text in texts if text and text.strip()]
        
        if not non_empty_texts:
            return []
        
        response = client.embeddings.create(model=model, input=non_empty_texts)
        return [embedding.embedding for embedding in response.data]
    
    except AuthenticationError as e:
        raise EmbeddingError(f"OpenAI authentication failed: {str(e)}")
    except RateLimitError as e:
        raise EmbeddingError(f"OpenAI rate limit exceeded: {str(e)}")
    except APIError as e:
        raise EmbeddingError(f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise EmbeddingError(f"Error generating embeddings: {str(e)}")


def generate_embedding(text: str, model: str = None) -> List[float]:
    if not text or not text.strip():
        raise EmbeddingError("Cannot generate embedding for empty text")
    
    embeddings = generate_embeddings([text], model)
    return embeddings[0] if embeddings else []
