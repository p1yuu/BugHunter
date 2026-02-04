import chromadb
from chromadb.utils import embedding_functions
import os

# Chroma client
client = chromadb.Client()

# Embedding fonksiyonu
embedding = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Koleksiyon oluştur
collection = client.create_collection(
    name="secai_knowledge",
    embedding_function=embedding
)

# Knowledge klasöründeki tüm .md dosyalarını ekle
knowledge_dir = "../knowledge"
for file_name in os.listdir(knowledge_dir):
    if file_name.endswith(".md"):
        path = os.path.join(knowledge_dir, file_name)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        collection.add(
            documents=[content],
            metadatas=[{"source": file_name}],
            ids=[file_name]
        )

print("Knowledge başarıyla ingested.")
