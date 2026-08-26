#step2.1.1 added

from modules.document_processor import (
    extract_pdf_text
)

with open(
    "Interview Questions for Freshers (online).pdf",
    "rb"
) as file:
    pdf_bytes = file.read()

result = extract_pdf_text(
    pdf_bytes
)

# print("Number of extracted pages:", len(result))
# # step2.1.2 added
# print(
#     "Total pages:",
#     result["total_pages"]
# )
# print(
#     "Pages containing text:",
#     result["text_pages"]
# )

# # for page in result:
# for page in result["pages"]:
#     print(
#         f"\n--- Page {page['page']} ---"
#     )
#     print(
#         page["text"][:500]
#     )

#step2.1.2 changed
if not result["success"]:

    print(
        "PDF processing failed:"
    )

    print(
        result["error"]
    )

else:

    print(
        "PDF processing successful!"
    )

    print(
        "Total pages:",
        result["total_pages"]
    )

    print(
        "Pages containing text:",
        result["text_pages"]
    )

    for page in result["pages"]:

        print(
            f"\n--- Page {page['page']} ---"
        )

        print(
            page["text"][:500]
        )