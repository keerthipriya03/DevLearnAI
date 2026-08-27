#step 5.2
# from modules.vector_store import collection

# print("Collection name:", collection.name)
# print("Stored chunks:", collection.count())

# modify the above steps to     (step 5.4)
from modules.vector_store import (
    collection,
    add_chunks,
    get_collection_count
)


test_chunks = [
    {
        "chunk_id": "page_1_chunk_0",
        "page": 1,
        "chunk_index": 0,
        "text": "Binary search repeatedly divides the search space.",
        "embedding": [0.1] * 384
    },
    {
        "chunk_id": "page_1_chunk_1",
        "page": 1,
        "chunk_index": 1,
        "text": "Binary search works efficiently on sorted data.",
        "embedding": [0.2] * 384
    }
]


add_chunks(
    test_chunks,
    "test_document.pdf"
)


print(
    "Stored chunks:",
    get_collection_count()
)
