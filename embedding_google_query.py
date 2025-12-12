from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = 'gemini-embedding-001')

result = embeddings.embed_query('Delhi is the capital of india.')
print(str(result))
