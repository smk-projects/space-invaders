from types import SimpleNamespace
game_state = SimpleNamespace(
    player_life = 4, 
    player_score = 0, 
    current_level = 1
)

def reset_state():
    reset_player_life()
    reset_player_score()
    reset_level()
    
def reset_player_life():
    game_state.player_life = 4

def reset_player_score():
    game_state.player_score = 0
    
def reset_level():
    game_state.current_level = 1
    
def next_level():
    game_state.current_level += 1
    
    