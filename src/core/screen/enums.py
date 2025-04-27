from enum import Enum

class ScreenState(Enum):
    """
    Enum for display results.
    """
    STARTUP  = 1,
    GAME_START = 2,
    GAME_RUNNING = 3,
    GAME_PASS = 6,
    GAME_OVER = 4,
    QUIT = -1,
    RESET = -2
    