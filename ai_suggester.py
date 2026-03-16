from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()


def _build_qwen_model() -> ChatHuggingFace:
    """
    Returns a ChatHuggingFace model backed by a Qwen Instruct model on Hugging Face.
    Uses the Inference API via HuggingFaceEndpoint.
    """
    repo_id = os.getenv("QWEN_REPO_ID", "Qwen/Qwen2.5-7B-Instruct")

    llm = HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.3,
    )
    return ChatHuggingFace(llm=llm)


model = _build_qwen_model()


def get_ai_suggestions(code_string: str):
    """
    Ask the Qwen model for concrete suggestions, with an emphasis on
    code clarity, performance, best practices, and potential logical bugs.
    """
    prompt = f"""
You are a senior Python reviewer. Carefully read the code below and respond with
actionable, concise suggestions.

Code:
```python
{code_string}
```

Respond with 3–6 bullet points covering:
- Readability and structure
- Performance or unnecessary work
- Python best practices
- Possible logical issues or edge cases that might break
"""

    try:
        response = model.invoke([HumanMessage(content=prompt)])

        ai_message = response.content

        return [
            {
                "type": "AISuggestion",
                "message": ai_message,
                "severity": "Info",
            }
        ]
    except Exception as e:
        # If the remote model is misconfigured or unavailable,
        # fall back to a simple, local set of suggestions so
        # the UI continues to work without exposing low-level errors.
        print(f"[ai_suggester] backend error: {e}")

        fallback_message = (
            "- Consider breaking large functions into smaller, focused helpers.\n"
            "- Make variable and function names more descriptive and consistent.\n"
            "- Add docstrings and type hints for public functions where useful.\n"
            "- Add tests (or asserts) around edge cases such as empty inputs or None values."
        )

        return [
            {
                "type": "AISuggestion",
                "message": fallback_message,
                "severity": "Info",
            }
        ]
