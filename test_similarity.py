#step4.2
from sentence_transformers import util
from modules.embeddings import load_embedding_model

model = load_embedding_model()
texts = [
    "Binary search divides the search space.",
    "Binary search repeatedly reduces the search area.",
    "Photosynthesis converts sunlight into chemical energy."
]

embeddings = model.encode(
    texts,
    convert_to_tensor=True
)

similarity_1_2 = util.cos_sim(
    embeddings[0],
    embeddings[1]
)
similarity_1_3 = util.cos_sim(
    embeddings[0],
    embeddings[2]
)

print(
    "Similarity 1 vs 2:",
    similarity_1_2.item()
)
print(
    "Similarity 1 vs 3:",
    similarity_1_3.item()
)
