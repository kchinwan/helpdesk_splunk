#core/memory.py

from typing import List, Dict


class ChatMemory:
    """
    Stores the user query and SPL generation history during a session.
    Supports context-aware follow-ups and reuse.
    """

    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def add_message(self, user_input: str, spl_output: str):
        """
        Adds a new interaction to the memory.

        Args:
            user_input (str): The user's original message.
            spl_output (str): The generated SPL.
        """
        self.history.append({
            "user": user_input,
            "spl": spl_output
        })

    def get_last_message(self) -> Dict[str, str]:
        """
        Returns the most recent user-SPL pair.

        Returns:
            Dict[str, str]: Last message dict.
        """
        return self.history[-1] if self.history else {}

    def get_full_history(self) -> List[Dict[str, str]]:
        """
        Returns the complete session history.

        Returns:
            List[Dict[str, str]]: All interactions.
        """
        return self.history

    def clear(self):
        """
        Clears the chat memory (for a new session).
        """
        self.history.clear()
