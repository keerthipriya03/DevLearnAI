# # py->gem api->ai res (the below code is to check if the gemini api is working properly)
# import os

# from dotenv import load_dotenv
# from google import genai


# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY was not found in the .env file.")


# client = genai.Client(api_key=api_key)


# response = client.models.generate_content(
#     model="gemini-3.6-flash",
#     contents="Explain inheritance in Java in simple terms."
# )


# print(response.text)


##converting program with streamlit
import streamlit as st

# import os                                  #no need after llm integration into the model
# from dotenv import load_dotenv             #no need after llm integration into the model
# from google import genai                   #no need after llm integration into the model

#step2.2.1 added
# from modules.document_processor import (
#     extract_pdf_text
# )

#above changed step 3.2.1
from modules.document_processor import (
    extract_pdf_text,
    create_document_chunks
)



from modules.code_analyzer import( analyze_code , extract_functions, get_function_source )
from modules.llm import generate_code_review




# Load environment variables
# load_dotenv()                               #no need after llm integration into the model
# api_key = os.getenv("GEMINI_API_KEY")       #no need after llm integration into the model
# client = genai.Client(api_key=api_key)      #no need after llm integration into the model

#step3.7 added
if "documents" not in st.session_state:
    st.session_state.documents = []


# Page Configuration
st.set_page_config(
    page_title="DevLearn AI",
    page_icon="🤖",
    layout="wide"
)


# Application Title
st.title("🤖 DevLearn AI")
st.write(
    "AI-Powered Study & Coding Assistant"
)


# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a feature:",
    [
        "📚 Knowledge Assistant",
        "💻 Code Assistant",
        "🎯 Quiz",
        "📚 Knowledge Manager"
    ]
)


# KNOWLEDGE ASSISTANT
if page == "📚 Knowledge Assistant":
    st.header("📚 Personal Knowledge Assistant")
    st.info(
        "Document-based Q&A will be implemented in the RAG stage."
    )


# CODE ASSISTANT
elif page == "💻 Code Assistant":
    st.header("💻 AI Code Assistant")
    st.write(
        "Analyze, understand and improve your Python code."
    )

    # Session State
    if "analyzed_code" not in st.session_state:
        st.session_state.analyzed_code = ""
    if "source_name" not in st.session_state:
        st.session_state.source_name = ""
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    if "review_result" not in st.session_state:
        st.session_state.review_result = None

    # Explanation level
    explanation_level = st.selectbox(
        "Choose explanation level:",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    simple_mode = st.checkbox(
        "🧒 Explain Like I'm Completely New"
    )


    # Code input
    st.markdown("### 📥 Choose Code Input")

    input_method = st.radio(
        "How would you like to provide your code?",
        [
            "✏️ Paste Code",
            "📁 Upload Python File"
        ],
        horizontal=True
    )

    code = ""
    source_name = "No source"

    if input_method == "✏️ Paste Code":
        source_name = "Pasted Code"
        code = st.text_area(
            "Paste your Python code here:",
            height=300,
            placeholder="""Example:
                        def find_max(arr):
                            maximum = arr[0]

                            for value in arr:
                                if value > maximum:
                                    maximum = value

                            return maximum
                        """
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a Python (.py) file",
            type=["py"]
        )
        if uploaded_file is not None:
            source_name = uploaded_file.name
            code = uploaded_file.read().decode(
                "utf-8"
            )
            st.success(
                f"Uploaded: {uploaded_file.name}"
            )
            with st.expander(
                "👀 Preview Code"
            ):
                st.code(
                    code,
                    language="python"
                )

    # --------------------------------------------------
    # Analyze Button
    # --------------------------------------------------

    if st.button(
        "🔍 Analyze Code",
        type="primary"
    ):

        if not code.strip():

            st.warning(
                "Please provide Python code before analysis."
            )

        else:

            st.caption(
                f"Analyzing: {source_name}"
            )

            analysis = analyze_code(code)

            if not analysis["valid"]:

                st.error(
                    "❌ Invalid Python code"
                )

                st.write(
                    analysis["error"]
                )

            else:

                # Save analyzed code
                st.session_state.analyzed_code = code

                st.session_state.source_name = source_name

                st.session_state.analysis_complete = True

                st.session_state.analysis_result = analysis
                st.session_state.review_result = None


    # --------------------------------------------------
    # Display Analysis Results
    # --------------------------------------------------

    if st.session_state.analysis_complete:

        code = st.session_state.analyzed_code

        analysis = st.session_state.analysis_result

        source_name = st.session_state.source_name

        # --------------------------------------------------
        # Valid Python
        # --------------------------------------------------

        st.success(
            "✅ Python syntax is valid"
        )

        st.caption(
            f"Source: {source_name}"
        )

        # --------------------------------------------------
        # Code Structure
        # --------------------------------------------------

        st.subheader(
            "📊 Code Structure"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Functions",
                analysis["functions"]
            )

            st.metric(
                "Loops",
                analysis["loops"]
            )

            st.metric(
                "Conditions",
                analysis["conditions"]
            )

        with col2:

            st.metric(
                "Classes",
                analysis["classes"]
            )

            st.metric(
                "Imports",
                analysis["imports"]
            )

            st.metric(
                "Function Calls",
                analysis["function_calls"]
            )

        with col3:

            st.metric(
                "Return Statements",
                analysis["returns"]
            )


        # --------------------------------------------------
        # Analysis Scope
        # --------------------------------------------------

        st.divider()

        st.subheader(
            "🎯 Analysis Scope"
        )

        function_data = extract_functions(code)

        function_names = [
            function["name"]
            for function in function_data["functions"]
        ]

        if function_names:

            analysis_scope = st.selectbox(
                "Choose what you want to analyze:",

                [
                    "📦 Entire File"
                ]
                +
                [
                    f"🔹 {name}()"
                    for name in function_names
                ]
            )

        else:

            analysis_scope = "📦 Entire File"

            st.info(
                "No functions detected. "
                "The entire file will be analyzed."
            )


        # --------------------------------------------------
        # Determine Selected Code
        # --------------------------------------------------

        selected_code = code

        selected_name = "Entire File"

        if analysis_scope != "📦 Entire File":

            selected_name = (
                analysis_scope
                .replace("🔹 ", "")
                .replace("()", "")
            )

            selected_code = get_function_source(
                code,
                selected_name
            )

        st.info(
            f"Selected: **{selected_name}**"
        )


        # --------------------------------------------------
        # Preview Selected Code
        # --------------------------------------------------

        with st.expander(
            "🔎 Preview Selected Code"
        ):

            st.code(
                selected_code,
                language="python"
            )


        # --------------------------------------------------
        # AST Analysis For Selected Code
        # --------------------------------------------------

        selected_analysis = analyze_code(
            selected_code
        )


        # # --------------------------------------------------
        # # Gemini Analysis
        # # --------------------------------------------------

        # with st.spinner(
        #     "🤖 AI is analyzing your code..."
        # ):

        #     review = generate_code_review(
        #         selected_code,
        #         selected_analysis,
        #         explanation_level
        #     )

        # --------------------------------------------------
        # Analyze Selected Code Button
        # --------------------------------------------------

        if st.button(
            "🤖 Analyze Selected Code",
            type="primary"
        ):

            with st.spinner(
                "🤖 AI is analyzing your code..."
            ):

                if simple_mode:
                    actual_level = (
                        "Very beginner-friendly. "
                        "Assume the learner has little "
                        "programming experience. "
                        "Avoid unnecessary technical jargon."
                    )

                else:

                    actual_level = explanation_level


                review = generate_code_review(
                    selected_code,
                    selected_analysis,
                    actual_level
                )

                st.session_state.review_result = review


        # --------------------------------------------------
        # AI Review Result
        # --------------------------------------------------

        review = st.session_state.review_result

        if review is not None:
            if "error" in review:

                st.error(
                    review["error"]
                )

                st.code(
                    review["raw_response"]
                )

            else:

                st.subheader(
                    "🤖 AI Code Review"
                )

                # --------------------------------------------------
                # Summary
                # --------------------------------------------------

                st.markdown(
                    "### 📋 Summary"
                )

                st.write(
                    review["summary"]
                )


                # --------------------------------------------------
                # Potential Issues
                # --------------------------------------------------

                st.markdown(
                    "### 🐛 Potential Issues"
                )

                if review["issues"]:

                    for issue in review["issues"]:

                        severity = issue["severity"]

                        if severity == "High":

                            st.error(
                                f"🔴 {issue['title']}\n\n"
                                f"{issue['description']}"
                            )

                        elif severity == "Medium":

                            st.warning(
                                f"🟠 {issue['title']}\n\n"
                                f"{issue['description']}"
                            )

                        else:

                            st.info(
                                f"🟢 {issue['title']}\n\n"
                                f"{issue['description']}"
                            )

                else:

                    st.success(
                        "No major issues were detected."
                    )


                # --------------------------------------------------
                # Improvements
                # --------------------------------------------------

                st.markdown(
                    "### 🔧 Improvements"
                )

                if review["improvements"]:

                    for improvement in review["improvements"]:

                        st.write(
                            f"**{improvement['title']}**"
                        )

                        st.write(
                            improvement["description"]
                        )

                else:

                    st.info(
                        "No major improvements suggested."
                    )


                # --------------------------------------------------
                # Complexity
                # --------------------------------------------------

                st.markdown(
                    "### ⏱ Complexity Analysis"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Time Complexity",
                        review["time_complexity"]["value"]
                    )

                    st.write(
                        review["time_complexity"]["explanation"]
                    )

                with col2:

                    st.metric(
                        "Space Complexity",
                        review["space_complexity"]["value"]
                    )

                    st.write(
                        review["space_complexity"]["explanation"]
                    )


                # --------------------------------------------------
                # Programming Concepts
                # --------------------------------------------------

                st.markdown(
                    "### 🎓 Programming Concepts"
                )

                for concept in review["concepts"]:

                    st.markdown(
                        f"- {concept}"
                    )


                # --------------------------------------------------
                # Learning Explanation
                # --------------------------------------------------

                st.markdown(
                    "### 📖 Learning Explanation"
                )

                st.write(
                    review["learning_explanation"]
                )


                # ---------------------------------------------
                # Step-by-Step Explanation
                # ---------------------------------------------

                st.markdown(
                    "### 🧭 Step-by-Step Explanation"
                )

                if review.get("step_by_step"):

                    for item in review["step_by_step"]:

                        step_number = item["step"]
                        title = item["title"]
                        explanation = item["explanation"]

                        with st.expander(
                            f"Step {step_number}: {title}"
                        ):

                            st.write(
                                explanation
                            )

                else:

                    st.info(
                        "Step-by-step explanation is not available."
                    )



                # --------------------------------------------------
                # Improved Code
                # --------------------------------------------------

                st.markdown(
                    "### 💻 Suggested Improved Code"
                )

                st.code(
                    review["improved_code"],
                    language="python"
                )

# QUIZ
elif page == "🎯 Quiz":
    st.header("🎯 AI Quiz")
    st.info(
        "Quiz generation will be implemented later."
    )

#KNOWLEDGE MANAGER
elif page == "📚 Knowledge Manager":
    # step1.1 added
    st.header("📚 Personal Knowledge Manager")
    st.write(
        "Upload your learning materials and build "
        "your personal AI knowledge base."
    )
    # step1.2 added
    st.markdown("### 📥 Upload Learning Material")
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"]
    )

    # step1.4 added
    document_name = st.text_input(
        "Document name",
        placeholder="Example: Python DSA Notes"
    )

    # step1.3 added
    if uploaded_file is not None:
        st.success(
            f"Uploaded: {uploaded_file.name}"
        )
        file_size = (
            len(uploaded_file.getvalue()) / 1024                 # gets the contents of the uploaded file as bytes
        )
        st.caption(
            f"File size: {file_size:.2f} KB"
        )
        #step1.5 added
        if not document_name.strip():
            st.warning(
                "Please provide a name for the document."
            )
        else:
            st.success(
                f"Ready to add: {document_name}"
            )

    #step1.6 added
    if st.button(
        "➕ Add to Knowledge Base",
        type="primary"
    ):
        if uploaded_file is None:
            st.warning(
                "Please upload a PDF first."
            )
        elif not document_name.strip():
            st.warning(
                "Please provide a document name."
            )
        # else:
        #     #step1.7 added
        #     document = {
        #         "name": document_name.strip(),
        #         "filename": uploaded_file.name,
        #         "size": len(uploaded_file.getvalue()),
        #         "status": "Uploaded"
        #     }

        #     st.session_state.documents.append(
        #         document
        #     )

        #     st.success(
        #         f"'{document_name}' added successfully!"
        #     )

        #step1.8 added
        else:
            existing_names = [
                document["name"]
                for document in st.session_state.documents
            ]
            if document_name.strip() in existing_names:
                st.warning(
                    "A document with this name already exists."
                )

            # else:
            #     document = {
            #         "name": document_name.strip(),
            #         "filename": uploaded_file.name,
            #         "size": len(uploaded_file.getvalue()),
            #         "status": "Uploaded"
            #     }
            #     st.session_state.documents.append(
            #         document
            #     )
            #     st.success(
            #         f"'{document_name}' added successfully!"
            #     )

            #step2.2.2 added changes the above else part.
            else:
                pdf_bytes = uploaded_file.getvalue()
                with st.spinner(
                    "📖 Reading PDF..."
                ):
                    result = extract_pdf_text(
                        pdf_bytes
                    )
                if not result["success"]:
                    st.error(
                        "❌ Unable to process the PDF."
                    )
                    st.write(
                        result["error"]
                    )
                else:
                    st.success(
                        "✅ PDF processed successfully!"
                    )
                    st.write(
                        f"Total pages: "
                        f"{result['total_pages']}"
                    )
                    st.write(
                        f"Pages containing text: "
                        f"{result['text_pages']}"
                    )
                    #step 3.2.2
                    chunks = create_document_chunks(
                        result["pages"]
                    )

                    st.write(
                        f"Generated chunks: "
                        f"{len(chunks)}"
                    )

                    document = {
                        "name": document_name.strip(),
                        "filename": uploaded_file.name,
                        "size": len(pdf_bytes),
                        "status": "Uploaded",
                        "total_pages": result["total_pages"],
                        "text_pages": result["text_pages"],
                        "pages": result["pages"],
                        #step 3.2.3
                        "chunks": chunks
                    }

                    st.session_state.documents.append(
                        document
                    )

                    st.success(
                        f"'{document_name}' added successfully!"
                    )
 
            
    #step1.9 added
    st.divider()
    st.markdown("### 📚 Your Documents")
    if not st.session_state.documents:
        st.info(
            "No documents added yet."
        )
    # else:
    #     for document in st.session_state.documents:
    #         with st.container(border=True):
    #             st.markdown(
    #                 f"### 📄 {document['name']}"
    #             )
    #             st.caption(
    #                 document["filename"]
    #             )
    #             st.write(
    #                 f"Status: {document['status']}"
    #             )
    #             st.write(
    #                 f"{document['size'] / 1024:.1f} KB"
    #             )
    else:
        for document in st.session_state.documents:
            with st.container(border=True):
                col1, col2, col3 = st.columns(
                    [4, 2, 1]
                )
                with col1:
                    st.markdown(
                        f"### 📄 {document['name']}"
                    )
                    st.caption(
                        document["filename"]
                    )
                #step 2.2.3 changed the below code to comment out col2 and use col3 for size
                # with col2:
                #     st.write(
                #         f"Status: {document['status']}"
                #     )
                with col2:
                    st.write(
                        f"Status: {document['status']}"
                    )
                    st.caption(
                        f"Pages: {document['total_pages']}"
                    )

                with col3:
                    st.write(
                        f"{document['size'] / 1024:.1f} KB"
                    )

            #step2.2.4 added
            with st.expander(
                "🔍 View extracted text"
            ):

                for page in document["pages"]:

                    st.markdown(
                        f"**📄 Page {page['page']}**"
                    )

                    st.text(
                        page["text"]
                    )

            #step3.2.4 added
            with st.expander(
                "🧩 View generated chunks"
            ):

                for chunk in document["chunks"]:

                    st.markdown(
                        f"**📄 Page {chunk['page']} | "
                        f"Chunk {chunk['chunk_index']}**"
                    )

                    st.caption(
                        f"Chunk ID: {chunk['chunk_id']}"
                    )

                    st.text(
                        chunk["text"]
                    )


