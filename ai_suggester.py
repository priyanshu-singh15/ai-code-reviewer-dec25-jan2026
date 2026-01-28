from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    temperature=0.3,
)

model = ChatHuggingFace(llm=llm)


def get_ai_suggestions(code_string):
    """
    WHAT IT DOES: Asks AI improvement ideas.
    """
    prompt = f"""
    Review this Python code and suggest improvements: 
    {code_string}. 
    Provide 2-3 brief suggestions for: 
    1. Code readability
    2. Performance
    3. Best practices
    """

    try:
        response = model.invoke(
            [HumanMessage(content=prompt)]
        )

        ai_message = response.content
        print(ai_message)

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
            "- Add docstrings and type hints for public functions where useful."
        )

        return [
            {
                "type": "AISuggestion",
                "message": fallback_message,
                "severity": "Info",
            }
        ]
