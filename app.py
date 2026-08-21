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

from modules.code_analyzer import( analyze_code , extract_functions, get_function_source )
from modules.llm import generate_code_review


# Load environment variables
# load_dotenv()                               #no need after llm integration into the model
# api_key = os.getenv("GEMINI_API_KEY")       #no need after llm integration into the model
# client = genai.Client(api_key=api_key)      #no need after llm integration into the model


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
        "🎯 Quiz"
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

                review = generate_code_review(
                    selected_code,
                    selected_analysis,
                    explanation_level
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