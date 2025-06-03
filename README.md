Splunk AI Assistant
This project is a Streamlit-based AI assistant designed to help users generate and refine Splunk Processing Language (SPL) queries. It leverages a hybrid approach, combining AI-driven generation with user-controlled manual refinements, providing a flexible and powerful tool for interacting with Splunk data.

Features
Natural Language to SPL: Convert natural language queries into executable SPL commands using a large language model (LLM).

Multiple Chats: Manage multiple conversation threads, each with its own context and history, similar to popular chat applications.

Hybrid SPL Refinement:

Manual Filter Addition: Users can explicitly add specific field-value filters to the generated SPL.

Smart Refine (LLM-powered): Users can provide natural language instructions to the LLM to intelligently modify or extend the existing SPL.

Query Finalization: Lock the SPL for a given chat, preventing further modifications once the user is satisfied.

Chat History: Maintain a clear history of user queries and generated/refined SPLs for each chat session.

Local Chat Data: All chat data remains local to the session, ensuring privacy.

Project Structure
splunk_ai_assistant/
│
├── main.py                     # Main Streamlit application entry point.
│                               # Handles UI, chat state, and orchestrates calls to core modules.
├── requirements.txt            # Lists Python dependencies required for the project.
│
├── core/                       # Contains the core logic for SPL generation and manipulation.
│   ├── spl_generator.py        # Responsible for calling the LLM (Gemini) to generate initial SPL queries from natural language.
│   ├── spl_composer.py         # Utility for composing clean SPL queries from structured components (index, filters, keywords).
│   ├── prompt_engine.py        # (Anticipated) Module for constructing and managing prompts for the LLM.
│   ├── memory.py               # (Optional) Module for managing in-memory chat history or context.
│   ├── spl_refiner.py          # Contains logic for refining existing SPL queries, supporting both manual filter additions and LLM-driven smart refinements.
│
├── config/                     # Configuration files for the assistant.
│   ├── schema_fields.py        # Defines expected Splunk schema fields, e.g., COLUMN_LIST, FIELD_MAPPINGS.
│   └── examples.py             # Stores few-shot examples to guide the LLM's SPL generation.
│
├── assets/                     # Static assets like images.
│   └── icon.png                # Application icon.

Getting Started (High-Level)
Clone the repository:

git clone <repository_url>
cd splunk_ai_assistant

Install dependencies:

pip install -r requirements.txt

Set up your LLM (Gemini) API: Ensure your environment is configured to access the Gemini API for spl_generator.py and the LLM-driven parts of spl_refiner.py.

Run the Streamlit application:

streamlit run main.py

This will launch the Splunk AI Assistant in your web browser.

