import random
import tkinter as tk
from tkinter import messagebox

# If running in a headless environment (e.g., server), use pyvirtualdisplay to simulate a display
try:
    from pyvirtualdisplay import Display
    # Start a virtual display
    display = Display(visible=0, size=(800, 600))
    display.start()
except ImportError:
    display = None  # If pyvirtualdisplay is not available, continue without it

# Game logic functions
def get_computer_choice():
    options = ['rock', 'paper', 'scissors']
    return random.choice(options)

def determine_winner(player1, player2, player1_name, player2_name="Computer"):
    if player1 == player2:
        return "It's a tie!"
    elif (player1 == 'rock' and player2 == 'scissors') or \
         (player1 == 'scissors' and player2 == 'paper') or \
         (player1 == 'paper' and player2 == 'rock'):
        return f"{player1_name} wins!"
    else:
        return f"{player2_name} wins!"

# GUI functions
def select_mode(mode):
    
    global game_mode
    game_mode = mode
    start_game()

def start_game():
    # Hide mode selection and show the main game interface
    mode_frame.pack_forget()
    main_frame.pack(pady=10)

def play_game(player_choice):
    if not player_name.get():
        messagebox.showwarning("Input Required", "Please enter your name!")
        return
    
    if game_mode == "computer":
        # Computer mode logic
        disable_choice_buttons()
        player_choice_label.config(text=f"{player_name.get()} chose: {player_choice}")
        result_label.config(text="Loading...", font=("Arial", 16, "italic"))
        computer_choice = get_computer_choice()
        root.after(1000, display_result, player_choice, computer_choice, player_name.get(), "Computer")
    
    elif game_mode == "multiplayer":
        # Multiplayer mode logic: Prompt for Player 2's choice
        if not player2_choice.get():
            player_choice_label.config(text=f"{player_name.get()} chose: {player_choice}")
            player2_choice.set(player_choice)
            player_choice_label.config(text=f"{player_name.get()} chose: {player_choice}")
            choice_instructions.config(text="Player 2, make your choice.")
        else:
            player1_choice = player2_choice.get()
            player2_choice.set("")  # Reset player 2's choice for replay
            disable_choice_buttons()
            root.after(1000, display_result, player1_choice, player_choice, player_name.get(), "Player 2")

def display_result(player1_choice, player2_choice, player1_name, player2_name):
    result = determine_winner(player1_choice, player2_choice, player1_name, player2_name)
    computer_choice_label.config(text=f"{player2_name} chose: {player2_choice}")
    result_label.config(text=f"Result: {result}", font=("Arial", 16, "bold"))

def replay_game():
    result_label.config(text="Result:")
    player_choice_label.config(text=f"{player_name.get()} chose:")
    computer_choice_label.config(text=f"Computer chose:" if game_mode == "computer" else "Player 2 chose:")
    player2_choice.set("")
    enable_choice_buttons()

def disable_choice_buttons():
    rock_button.config(state="disabled")
    paper_button.config(state="disabled")
    scissors_button.config(state="disabled")

def enable_choice_buttons():
    rock_button.config(state="normal")
    paper_button.config(state="normal")
    scissors_button.config(state="normal")

# Setting up the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors Game")

# Game mode selection
game_mode = "computer"  # Default mode
player2_choice = tk.StringVar()  # Holds Player 2's choice in multiplayer mode

mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)

tk.Label(mode_frame, text="Choose Game Mode", font=("Arial", 14)).pack()
tk.Button(mode_frame, text="Play vs Computer", font=("Arial", 12), width=15, command=lambda: select_mode("computer")).pack(pady=5)
tk.Button(mode_frame, text="Play Multiplayer", font=("Arial", 12), width=15, command=lambda: select_mode("multiplayer")).pack(pady=5)

# Main game interface
main_frame = tk.Frame(root)

# Player name entry
name_frame = tk.Frame(main_frame)
name_frame.pack(pady=10)

tk.Label(name_frame, text="Enter your name:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
player_name = tk.Entry(name_frame, font=("Arial", 12), width=15)
player_name.grid(row=0, column=1, padx=5)

# Labels to display choices and result
choice_instructions = tk.Label(main_frame, text="Make your choice:", font=("Arial", 14))
choice_instructions.pack(pady=5)

player_choice_label = tk.Label(main_frame, text="You chose:", font=("Arial", 14))
player_choice_label.pack(pady=5)

computer_choice_label = tk.Label(main_frame, text="Computer chose:", font=("Arial", 14))
computer_choice_label.pack(pady=5)

result_label = tk.Label(main_frame, text="Result:", font=("Arial", 16, "bold"))
result_label.pack(pady=10)

# Buttons for rock, paper, scissors
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=10)

rock_button = tk.Button(button_frame, text="Rock", font=("Arial", 12), width=10, command=lambda: play_game("rock"))
rock_button.grid(row=0, column=0, padx=5)

paper_button = tk.Button(button_frame, text="Paper", font=("Arial", 12), width=10, command=lambda: play_game("paper"))
paper_button.grid(row=0, column=1, padx=5)

scissors_button = tk.Button(button_frame, text="Scissors", font=("Arial", 12), width=10, command=lambda: play_game("scissors"))
scissors_button.grid(row=0, column=2, padx=5)

# Replay button
replay_button = tk.Button(main_frame, text="Replay", font=("Arial", 12), command=replay_game)
replay_button.pack(pady=10)

# Exit button
exit_button = tk.Button(main_frame, text="Exit", font=("Arial", 12), command=root.quit)
exit_button.pack(pady=10)

# Run the application
root.mainloop()

# Stop the virtual display if it was used
if display:
    display.stop()
