from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
HAS_GEMINI = bool(GEMINI_API_KEY)

st.set_page_config(
    page_title="Research Console",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Minimal, dark, code-centric theme to match the reviewer app
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
        max-width: 1000px;
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

    .stTextInput > div > div > input {
        background-color: #05060a;
        border-radius: 4px;
        border: 1px solid #111827;
        padding: 0.7rem 0.85rem;
        font-size: 0.95rem;
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

    .result-container {
        background-color: #05060a;
        border-radius: 4px;
        border: 1px solid #111827;
        padding: 1.25rem;
        margin-top: 1.5rem;
    }

    h3 {
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_col, title_col = st.columns([1, 5])
with logo_col:
    st.logo("logo.png")
with title_col:
    st.markdown(
        """
        <div class="header-bar">
            <div>
                <div class="header-title">Research Console</div>
                <div class="header-subtitle">Quick summaries and context for your work</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

prompt = st.text_input(
    "Prompt",
    placeholder="Ask a focused research question or describe the topic.",
)

if not HAS_GEMINI:
    st.info(
        "Cloud research is disabled because no Gemini API key is configured. "
        "Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment or Streamlit secrets to enable it."
    )
else:
    if st.button("Summarize", type="primary"):
        if prompt.strip():
            with st.spinner("Generating summary…"):
                model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GEMINI_API_KEY)
                result = model.invoke(prompt)
                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                st.markdown("### Summary")
                st.write(result.content)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("Enter a prompt to summarize.")
