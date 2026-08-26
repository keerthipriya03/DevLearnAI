#Stage 3.1.1

# from modules.document_processor import chunk_text             #for text
from modules.document_processor import create_document_chunks   # for pages


# text = """
# Binary search is an efficient searching algorithm
# that works on sorted data. It repeatedly divides
# the search space into two halves. The middle element
# is compared with the target value. If the target is
# smaller, the left half is searched. If the target is
# larger, the right half is searched. This process
# continues until the target is found or the search
# space becomes empty.
# """

# text="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# text = """
# ABCDEFGHIJ
# KLMNOPQRST
# UVWXYZ
# """


#Stage - 3.1.2
pages = [
    {
        "page": 1,
        "text": (
            "Binary search is an efficient searching algorithm "
            "that works on sorted data."
        )
    },
    {
        "page": 2,
        "text": (
            "Arrays are data structures that store elements "
            "in contiguous memory locations."
        )
    }
]

chunks = create_document_chunks(
    pages,
    chunk_size=30,               #These values will be changig accor to the text input taken.
    overlap=5                    #These values will be changig accor to the text input taken.
)                                #overlap should not >= chunk_size (else gets an valueerr)

print(
    f"Number of chunks: {len(chunks)}"
)

# for index, chunk in enumerate(
#     chunks,
#     start=1
# ):
#     print(
#         f"\n--- Chunk {index} ---"
#     )
#     print(chunk)
#Stage - 3.1.3
for chunk in chunks:

    print("\n--- Chunk ---")

    print(
        f"ID: {chunk['chunk_id']}"
    )

    print(
        f"Page: {chunk['page']}"
    )

    print(
        f"Chunk index: {chunk['chunk_index']}"
    )

    print(
        f"Text: {chunk['text']}"
    )