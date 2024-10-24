import tkinter as tk
import os

class BulbApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bulb ON/OFF Project")
        
        # Set the size of the window
        self.root.geometry("300x400")
        
        # Bulb is initially OFF
        self.bulb_status = False
        
        # Create the label to show bulb status
        self.label = tk.Label(self.root, text="Bulb is OFF", font=("Arial", 20), fg="red")
        self.label.pack(pady=20)
        
        # Create the button to toggle the bulb
        self.button = tk.Button(self.root, text="Turn ON", font=("Arial", 20), command=self.toggle_bulb)
        self.button.pack(pady=20)
        
        # Create a canvas to display the bulb image
        self.canvas = tk.Canvas(self.root, width=200, height=200)
        self.canvas.pack()
        
        # Load the OFF and ON images
        # Use absolute path to avoid file path issues
        try:
            self.bulb_off_image = tk.PhotoImage(file=os.path.abspath("test\off.PNG"))
            self.bulb_on_image = tk.PhotoImage(file=os.path.abspath("test\on.PNG"))
        except Exception as e:
            print(f"Error loading images: {e}")
            self.label.config(text="Error: Images not found")
            return
        
        # Display the initial OFF image
        self.canvas_image = self.canvas.create_image(100, 100, image=self.bulb_off_image)

    def toggle_bulb(self):
        # Toggle the bulb status
        self.bulb_status = not self.bulb_status
        
        if self.bulb_status:
            # Bulb is ON
            self.label.config(text="Bulb is ON", fg="green")
            self.button.config(text="Turn OFF")
            self.canvas.itemconfig(self.canvas_image, image=self.bulb_on_image)
        else:
            # Bulb is OFF
            self.label.config(text="Bulb is OFF", fg="red")
            self.button.config(text="Turn ON")
            self.canvas.itemconfig(self.canvas_image, image=self.bulb_off_image)

# Create the main window
root = tk.Tk()

# Create the BulbApp object
app = BulbApp(root)

# Start the GUI event loop
root.mainloop()
