import fitz         #to open the PDF and read its pages.


#step2.1 added
def extract_pdf_text(pdf_bytes):
    #step2.4 added
    try:
        document = fitz.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        pages = []

        for page_number, page in enumerate(
            document,
            start=1
        ):
            text = page.get_text("text").strip()
            if text:
                #step2.2 added
                pages.append(
                    {
                        "page": page_number,
                        "text": text
                    }
                )

        #step2.3 added
        result = {
            #step2.4 added
            "success": True,
            "total_pages": len(document),
            "text_pages": len(pages),
            "pages": pages
        }

        document.close()
        #return pages it is changed to following after step2.3
        return result

    #step2.5 added
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Stage 3.1 - Step 1: Basic text chunking
def chunk_text(
    text,
    chunk_size=800,
    overlap=100
):
    #stage 3.2 - Step 2: Check if the text is empty or contains only whitespace
    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )
    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )
    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )
    
    if not text.strip():
        return []
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(
                chunk.strip()
            )
        start += (
            chunk_size - overlap
        )
    return chunks

#Stage 3.3
# Stage 3.3 - Create document chunks with metadata
def create_document_chunks(
    pages,
    chunk_size=800,
    overlap=100
):

    chunks = []

    for page_data in pages:

        page_number = page_data["page"]

        page_text = page_data["text"]

        page_chunks = chunk_text(
            page_text,
            chunk_size,
            overlap
        )

        for chunk_index, chunk in enumerate(
            page_chunks,
            start=1
        ):

            chunks.append(
                {
                    "chunk_id": (
                        f"page_{page_number}_"
                        f"chunk_{chunk_index}"
                    ),

                    "page": page_number,

                    "chunk_index": chunk_index,

                    "text": chunk
                }
            )

    return chunks
