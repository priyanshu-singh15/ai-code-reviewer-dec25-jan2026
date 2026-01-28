# import streamlit as st

# from code_parser import parse_code
# from style_checker import show_style_corrected
# from error_detector import detect_errors
# from ai_suggester import get_ai_suggestions

# st.title("AI Code Reviewer")
# st.markdown("Paste your Python code below and click Analyze!")
# code = st.text_area("Code:")

# if st.button("Analyze"):
#     if not code:
#         st.warning("Please enter some code first!")
#     else:
#         st.info("Analyzing your code...")

#         parse_result = parse_code(code)
#         if not parse_result["success"]:
#             st.error("Your code has syntax errors!")
#             st.code(parse_result["error"]["message"])
#             st.stop()
        
#         st.success("Code parsed successfully!")

#         st.subheader("Error Detection Results")

#         error_result = detect_errors(code)

#         if error_result["success"]:
#             if error_result["error_count"] == 0:
#                 st.success("No error found! Your code looks good.")
#             else:
#                 st.warning(f"Found {error_result['error_count']} issue(s):")

#                 for error in error_result["errors"]:
#                     with st.expander(f" {error['type']}", expanded=True):
#                         st.write(f"**Message:** {error['message']}")
#                         st.info(f"**Suggestion:** {error['suggestion']}")
#         else:
#             st.error("Could not analyze code for errors")

#         st.subheader("Style-Corrected Version")

#         try:
#             style_result = show_style_corrected(code)

#             if style_result["success"]:
#                 st.code(style_result["corrected_code"], language="python")
#                 st.caption("This is how you code looks with proper formatting")
#             else:
#                 st.info("Style correction not available")
#         except Exception as e:
#             st.info("Style checking module not found")

#         st.subheader("Your Original Code")
#         st.code(code, language="python")

#         st.subheader("AI Suggestions")

#         suggest = get_ai_suggestions(code)
#         st.info(suggest[0]["message"])

        
import streamlit as st
import time
from code_parser import parse_code
from style_checker import show_style_corrected
from error_detector import detect_errors
from ai_suggester import get_ai_suggestions


def stream_data(text: str):
    """Yields text word by word for the typewriter effect."""
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Minimal, dark, code-first theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #05060a;
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Mono",
                     Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
        font-size: 15px;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .header-bar {
        display: flex;
        align-items: center;
        gap: 1rem;
        border-bottom: 1px solid #1f2933;
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }

    .header-title {
        font-size: 1.4rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #e5e7eb;
    }

    .header-subtitle {
        font-size: 0.9rem;
        color: #9ca3af;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        border-bottom: 1px solid #1f2933;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0;
        padding: 0.5rem 1rem;
        color: #9ca3af;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #3b82f6;
        color: #e5e7eb;
    }

    .stTextArea textarea {
        background-color: #05060a;
        border-radius: 4px;
        border: 1px solid #111827;
        padding: 1rem;
        font-family: "JetBrains Mono", "Fira Code", Menlo, Monaco, Consolas,
                     "Liberation Mono", "Courier New", monospace;
        font-size: 0.9rem;
        color: #e5e7eb;
    }

    .stButton > button {
        background-color: #111827;
        color: #e5e7eb;
        border-radius: 4px;
        border: 1px solid #374151;
        padding: 0.55rem 1.4rem;
        font-size: 0.9rem;
    }

    .stButton > button:hover {
        background-color: #1f2937;
        border-color: #4b5563;
    }

    .stAlert {
        border-radius: 4px;
        border: 1px solid #111827;
        background-color: #05060a;
        font-size: 0.95rem;
    }

    .streamlit-expanderHeader {
        background-color: #05060a;
        color: #e5e7eb;
        border-bottom: 1px solid #111827;
    }

    .streamlit-expanderContent {
        background-color: #05060a;
        border-left: 1px solid #111827;
        border-right: 1px solid #111827;
        border-bottom: 1px solid #111827;
    }

    code, pre {
        font-family: "JetBrains Mono", "Fira Code", Menlo, Monaco, Consolas,
                     "Liberation Mono", "Courier New", monospace !important;
        font-size: 0.9rem !important;
    }

    h3 {
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 1.75rem;
        margin-bottom: 0.75rem;
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_col, title_col = st.columns([1, 5])
with logo_col:
    # Use the provided logo file
    st.logo("logo.png")
with title_col:
    st.markdown(
        """
        <div class="header-bar">
            <div>
                <div class="header-title">AI Code Reviewer</div>
                <div class="header-subtitle">Static checks, formatting, and AI prompts for Python</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

tab1, tab2 = st.tabs(["Analysis", "AI Suggestions"])



with tab1:
    st.caption("Paste Python below and run static checks plus formatting.")

    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        analyze_clicked = st.button("Run analysis", type="primary", use_container_width=False)
    with btn_col2:
        refresh_clicked = st.button("Refresh", use_container_width=False)

    if refresh_clicked:
        # Clear widget + derived state, then rerun before widgets instantiate.
        st.session_state["source_code"] = ""
        st.session_state.pop("analyzed_code", None)
        st.session_state.pop("ai_suggestions", None)
        st.rerun()

    code = st.text_area(
        "Source code",
        height=260,
        placeholder="Paste or type Python here…",
        help="The code is never stored; it is only used for this analysis session.",
        key="source_code",
    )

    if analyze_clicked:
        if not code:
            st.warning("Provide some code to analyze.")
        else:
            st.session_state["analyzed_code"] = code

            parse_result = parse_code(code)
            if not parse_result["success"]:
                st.error("Syntax errors detected.")
                st.code(parse_result["error"]["message"], language="python")
                st.stop()

            st.success("Parsed successfully.")

            st.markdown("### Error detection")
            error_result = detect_errors(code)

            if error_result["success"]:
                if error_result["error_count"] == 0:
                    st.info("No static issues found.")
                else:
                    st.warning(f"{error_result['error_count']} potential issue(s) found.")
                    for error in error_result["errors"]:
                        with st.expander(error["type"], expanded=True):
                            st.markdown(f"**Message:** {error['message']}")
                            st.info(f"Suggestion: {error['suggestion']}")
            else:
                st.error("Error analysis failed.")

            st.markdown("### Formatted version")
            try:
                style_result = show_style_corrected(code)
                if style_result["success"]:
                    with st.expander("View formatted code", expanded=False):
                        st.code(style_result["corrected_code"], language="python")
                        st.caption("PEP8-style formatting of your input.")
                else:
                    st.info("Style correction not available.")
            except Exception:
                st.info("Style checking module not available.")

            st.markdown("### Original input")
            with st.expander("View original code", expanded=False):
                st.code(code, language="python")

            with st.spinner("Computing AI suggestions…"):
                suggestions = get_ai_suggestions(code)
                st.session_state["ai_suggestions"] = suggestions


with tab2:
    st.caption("Model-level suggestions based on the last analysis.")

    if "analyzed_code" in st.session_state and st.session_state["analyzed_code"]:
        if "ai_suggestions" in st.session_state:
            suggestions = st.session_state["ai_suggestions"]
            for suggestion in suggestions:
                if suggestion["type"] == "AISuggestion":
                    with st.chat_message("assistant"):
                        st.write_stream(stream_data(suggestion["message"]))
                elif suggestion["type"] == "Error":
                    st.error(suggestion["message"])
        else:
            st.info("Run analysis in the Analysis tab to generate suggestions.")
    else:
        st.info("Run analysis in the Analysis tab to generate suggestions.")

