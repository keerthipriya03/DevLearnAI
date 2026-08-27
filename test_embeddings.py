#step 4.3
from modules.embeddings import generate_embedding
text = (
    "Binary search repeatedly "
    "divides the search space."
)
embedding = generate_embedding(text)

print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
