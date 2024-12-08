import tkinter as tk

# Function to cycle through the states of the bulb
def cycle_bulb_state():
    # Define the sequence of states
    states = ["Off", "Low", "Mid", "High", "Highest"]
    bulb_colors = {
        "Off": "gray",
        "Low": "#FFFDD0",
        "Mid": "yellow",
        "High": "orange",
        "Highest": "red"
    }
    corner_colors = {
        "Off": "white",
        "Low": "#f0e68c",
        "Mid": "#ffeb3b",
        "High": "#ff9800",
        "Highest": "#ff5722"
    }

    # Get the current state
    current_state = state_label["text"]

    # Find the next state
    current_index = states.index(current_state)
    next_index = (current_index + 1) % len(states)  # Cycle back to "Off" after "Highest"

    # Update the bulb color and state label
    new_state = states[next_index]
    bulb_canvas.itemconfig(bulb_body, fill=bulb_colors[new_state])
    state_label.config(text=new_state)

    # Update the canvas background color (corner color)
    bulb_canvas.config(bg=corner_colors[new_state])

# Create the main window
root = tk.Tk()
root.title("Bulb Intensity Control")
root.geometry("500x600")  # Set a larger window size

# Create a canvas for the bulb
bulb_canvas = tk.Canvas(root, width=400, height=400, bg="white")
bulb_canvas.pack(pady=20)

# Draw the bulb shape
bulb_body = bulb_canvas.create_oval(100, 50, 300, 300, fill="gray")  # Enlarged bulb body
bulb_base = bulb_canvas.create_rectangle(170, 300, 230, 350, fill="black")  # Enlarged bulb base

# Label to show the current state
state_label = tk.Label(root, text="Off", font=("Helvetica", 20))
state_label.pack(pady=10)

# Button to control the bulb
control_button = tk.Button(
    root,
    text="Control Bulb",
    font=("Helvetica", 18),
    command=cycle_bulb_state
)
control_button.pack(pady=20)

# Run the application
root.mainloop()
