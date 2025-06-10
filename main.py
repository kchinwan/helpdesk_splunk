import sys
import subprocess

packages = [
    "numpy",
    "pandas",
    "streamlit"
     "google-generativeai"
    "dotenv"
]

for package in packages:
    print(f"Installing the latest version of {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
import streamlit as st
import uuid
from core.spl_generator import generate_spl_query
from core.spl_refiner import refine_spl_query
from utils.session import save_chat, load_chat

# --- Initialization ---
if "chats" not in st.session_state:
    st.session_state["chats"] = {}
if "active_chat_id" not in st.session_state:
    st.session_state["active_chat_id"] = None
if "refining" not in st.session_state:
    st.session_state["refining"] = False

st.set_page_config(page_title="Helpdesk AI Assistant", page_icon=":mag:", layout="wide")
st.sidebar.image("assets/icon.png", width=80)
st.sidebar.title("Helpdesk AI Assistant")
st.sidebar.caption("by LEAP + Gemini")

# ---  Theme Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
    background-color: #121212;
    color: #000000;
}

.stApp {
    background-color: #121212;
}

.stButton>button {
    background-color: #ffffff;
    color: #000000;
    border-radius: 6px;
    padding: 0.5em 1em;
    font-weight: 500;
    border: 1px solid #ccc;
}

.stTextInput>div>input, .stTextArea>div>textarea {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.stCode {
    background-color: #ffffff;
    color: #000000;
    border-radius: 4px;
}

.stSidebar {
    background-color: #1e1e1e;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)


# --- Start New Chat ---
if st.sidebar.button("➕ Start New Chat"):
    chat_id = str(uuid.uuid4())
    st.session_state["chats"][chat_id] = {
        "query": "",
        "history": [],
        "finalized": False,
        "extracted_entities": {},
        "current_spl": ""
    }
    st.session_state["active_chat_id"] = chat_id
    st.session_state["refining"] = False

# --- Show Chat List ---
for cid, chat in st.session_state["chats"].items():
    button_label = chat["query"][:50] if chat["query"] else "Untitled"
    if st.sidebar.button(button_label, key=cid):
        st.session_state["active_chat_id"] = cid
        st.session_state["refining"] = False

# --- Active Chat Logic ---
chat_id = st.session_state["active_chat_id"]
if chat_id:
    chat = st.session_state["chats"][chat_id]

    user_query = st.text_input("💬 Enter your query:", value=chat["query"], key="initial_query_input")
    if st.button("▶️ Generate SPL", key="generate_spl_button"):
        chat["query"] = user_query
        with st.spinner("Generating SPL..."):
            result = generate_spl_query(user_query, chat["history"])
        chat["current_spl"] = result["clean_output"]
        chat["extracted_entities"] = result.get("extracted_entities", {})
        chat["history"].append({"user": user_query, "spl": result["clean_output"]})
        st.session_state["refining"] = False

        save_chat(chat_id, chat)
        st.rerun()

    if chat["current_spl"]:
        st.code(chat["current_spl"], language="spl")

    if not chat["finalized"]:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔎 Refine Filters", key="refine_filters_button"):
                st.session_state["refining"] = True
                st.rerun()

        with col2:
            if st.button("✅ Finalize", key="finalize_button"):
                chat["finalized"] = True
                st.session_state["refining"] = False
                st.success("Query finalized. No more changes allowed.")
                save_chat(chat_id, chat)
                st.rerun()

    else:
        st.info("✅ This chat is finalized and cannot be refined further.")

    if st.session_state["refining"] and not chat["finalized"]:
        st.markdown("---")
        st.subheader("Refine your SPL query")
        refinement_prompt = st.text_input(
            "Tell me how to refine the current SPL (e.g., 'add time range last 24h', 'filter by sourcetype access_logs'):",
            key="refinement_prompt_input"
        )
        col_refine_btn, col_cancel_btn = st.columns(2)
        with col_refine_btn:
            if st.button("✨ Apply Refinement", key="apply_refinement_button"):
                if refinement_prompt:
                    with st.spinner("Refining SPL..."):
                        updated_spl = refine_spl_query(chat["current_spl"], chat["extracted_entities"], refinement_prompt)
                    chat["current_spl"] = updated_spl
                    chat["history"].append({"user": f"Refined with: '{refinement_prompt}'", "spl": updated_spl})
                    st.session_state["refining"] = False
                    save_chat(chat_id, chat)
                    st.rerun()
                else:
                    st.warning("Please provide refinement instructions.")
        with col_cancel_btn:
            if st.button("❌ Cancel Refinement", key="cancel_refinement_button"):
                st.session_state["refining"] = False
                st.rerun()
        st.markdown("---")

    with st.expander("📜 Chat History"):
        for msg in chat["history"]:
            st.markdown(f"**User:** {msg['user']}")
            st.code(msg["spl"], language="spl")

else:
    st.info("Start a new chat to begin.")

st.markdown("---")
st.caption("🔒 Your chat stays local. It only generates SPLs on demand.")
