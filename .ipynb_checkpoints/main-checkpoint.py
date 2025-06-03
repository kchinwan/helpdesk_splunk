import streamlit as st
import uuid
from core.spl_generator import generate_spl_query
from core.spl_refiner import refine_spl_query # This function will need to accept a refinement_prompt

# --- Initialization ---
if "chats" not in st.session_state:
    st.session_state["chats"] = {}
if "active_chat_id" not in st.session_state:
    st.session_state["active_chat_id"] = None
if "refining" not in st.session_state: # New state to manage refinement mode
    st.session_state["refining"] = False

st.set_page_config(page_title="Splunk AI Assistant", page_icon=":mag:", layout="wide")
st.sidebar.image("assets/icon.png", width=80)
st.sidebar.title("Splunk AI Assistant")
st.sidebar.caption("by LEAP + Gemini")

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
    st.session_state["refining"] = False # Reset refining state for new chat

# --- Show Chat List ---
for cid, chat in st.session_state["chats"].items():
    button_label = chat["query"][:50] if chat["query"] else "Untitled"
    if st.sidebar.button(button_label, key=cid):
        st.session_state["active_chat_id"] = cid
        st.session_state["refining"] = False # Reset refining state when switching chats

# --- Active Chat Logic ---
chat_id = st.session_state["active_chat_id"]
if chat_id:
    chat = st.session_state["chats"][chat_id]

    user_query = st.text_input("💬 Enter your query:", value=chat["query"], key="initial_query_input")
    if st.button("▶️ Generate SPL", key="generate_spl_button"):
        chat["query"] = user_query
        result = generate_spl_query(user_query, chat["history"])
        chat["current_spl"] = result["clean_output"]
        chat["extracted_entities"] = result.get("extracted_entities", {})
        chat["history"].append({"user": user_query, "spl": result["clean_output"]})
        st.session_state["refining"] = False # Ensure refinement mode is off after new generation
        st.experimental_rerun() # Rerun to update UI immediately

    if chat["current_spl"]:
        st.code(chat["current_spl"], language="spl")

    if not chat["finalized"]:
        col1, col2 = st.columns(2)
        with col1:
            # Clicking Refine Filters now toggles the refinement input visibility
            if st.button("🔎 Refine Filters", key="refine_filters_button"):
                st.session_state["refining"] = True
                st.experimental_rerun() # Rerun to show the refinement input

        with col2:
            if st.button("✅ Finalize", key="finalize_button"):
                chat["finalized"] = True
                st.session_state["refining"] = False # Exit refinement mode on finalize
                st.success("Query finalized. No more changes allowed.")
                st.experimental_rerun() # Rerun to update UI

    else:
        st.info("✅ This chat is finalized and cannot be refined further.")

    # --- Refinement Input Section ---
    # This section appears only if "refining" state is True and chat is not finalized
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
                    # IMPORTANT: The 'refine_spl_query' function in 'core/spl_refiner.py'
                    # will need to be updated to accept this 'refinement_prompt' argument.
                    # Example: refine_spl_query(current_spl, extracted_entities, refinement_prompt)
                    updated_spl = refine_spl_query(chat["current_spl"], chat["extracted_entities"], refinement_prompt)
                    chat["current_spl"] = updated_spl
                    chat["history"].append({"user": f"Refined with: '{refinement_prompt}'", "spl": updated_spl})
                    st.session_state["refining"] = False # Exit refinement mode
                    st.experimental_rerun() # Rerun to update UI and hide refinement input
                else:
                    st.warning("Please provide refinement instructions.")
        with col_cancel_btn:
            if st.button("❌ Cancel Refinement", key="cancel_refinement_button"):
                st.session_state["refining"] = False
                st.experimental_rerun() # Rerun to hide refinement input
        st.markdown("---")


    with st.expander("📜 Chat History"):
        for msg in chat["history"]:
            st.markdown(f"**User:** {msg['user']}")
            st.code(msg["spl"], language="spl")
else:
    st.info("Start a new chat to begin.")

st.markdown("---")
st.caption("🔒 Your chat stays local. Gemini only generates SPLs on demand.")
