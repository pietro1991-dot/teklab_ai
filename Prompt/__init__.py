"""
Prompt package initialization
"""

from .prompts_config import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    WELCOME_MESSAGE,
    COMMANDS_HELP,
    TEST_QUESTIONS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    MAX_HISTORY_TURNS,
    MAX_TOKENS_ESTIMATE,
    TOP_K_CHUNKS,
    HYBRID_SEARCH_WEIGHTS,
    get_system_prompt,
    get_user_prompt,
    get_welcome_message,
    get_commands_help,
    get_test_questions
)

__all__ = [
    'SYSTEM_PROMPT',
    'USER_PROMPT_TEMPLATE',
    'WELCOME_MESSAGE',
    'COMMANDS_HELP',
    'TEST_QUESTIONS',
    'DEFAULT_TEMPERATURE',
    'DEFAULT_MAX_TOKENS',
    'MAX_HISTORY_TURNS',
    'MAX_TOKENS_ESTIMATE',
    'TOP_K_CHUNKS',
    'HYBRID_SEARCH_WEIGHTS',
    'get_system_prompt',
    'get_user_prompt',
    'get_welcome_message',
    'get_commands_help',
    'get_test_questions'
]
