#step 5.1
import chromadb
import hashlib          #step 5.3

client = chromadb.PersistentClient(
    path="./chroma_db"
)
collection = client.get_or_create_collection(
    name="devlearn_knowledge"
)

#step 5.3
def generate_document_id(document_name):
    return hashlib.md5(
        document_name.encode()
    ).hexdigest()

def add_chunks(
    chunks,
    document_name
):

    if not chunks:
        return

    document_id = generate_document_id(
        document_name
    )

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:

        chunk_id = (
            f"{document_id}_"
            f"{chunk['chunk_id']}"
        )

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        embeddings.append(
            chunk["embedding"]
        )

        metadatas.append(
            {
                "document": document_name,
                "document_id": document_id,
                "page": chunk["page"],
                "chunk_index": chunk["chunk_index"]
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

def get_collection_count():
    return collection.count()

def get_all_documents():
    return collection.get()
