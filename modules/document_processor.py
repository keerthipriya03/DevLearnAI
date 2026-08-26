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