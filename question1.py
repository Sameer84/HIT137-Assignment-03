import tkinter as tk
#Define a custom Calculator class inheriting from tk.Tk
class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()  #Call the constructor of the parent class
        self.title("Calculator")  #Set the title of the calculator window
        self.geometry("300x380")  #Set the initial size of the window
        self.result_var = tk.StringVar()  #Variable to store calculation result
        
        self.create_widgets()  #Method to create GUI elements
    
    #Method to create GUI widgets
    def create_widgets(self):
        #Create an Entry widget for displaying and entering calculations
        self.entry = tk.Entry(self, textvariable=self.result_var, font=("Arial", 16), justify="right")
        self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        
        #Define buttons with their text, row, and column positions
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0)  #Add a "Clear" button
        ]
        
        button_width = 4
        button_height = 1
        button_padding = 8
        
        #Create buttons dynamically and place them in the grid layout
        for (text, row, column) in buttons:
            button = CalculatorButton(self, text=text, font=("Arial", 16), width=button_width, height=button_height, column=column)
            button.configure(command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column, padx=button_padding, pady=button_padding, sticky="nsew")
        
        #Configure grid layout to expand with window size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    #Method to handle button clicks
    def on_button_click(self, text):
        if text == "=":
            self.calculate()  #Call the calculate method when "=" button is clicked
        elif text == "C":
            self.clear()  #Call the clear method when "C" button is clicked
        else:
            current_text = self.result_var.get()
            self.result_var.set(current_text + text)
    
    #Method to evaluate and display calculation result
    def calculate(self):
        try:
            result = eval(self.result_var.get())
            self.result_var.set(str(result))
        except Exception as e:
            self.result_var.set("Error")
    
    #Method to clear the entry widget
    def clear(self):
        self.result_var.set("")  #Clear the entry widget when "C" button is clicked

#Define a custom CalculatorButton class inheriting from tk.Button
class CalculatorButton(tk.Button):
    def __init__(self, *args, column, **kwargs):
        super().__init__(*args, **kwargs)
        #Set different background colors based on the column index
        if column % 2 == 0:
            self.configure(bg="lightblue", fg="black")
        else:
            self.configure(bg="lightgreen", fg="black")

#Main entry point of the program
if __name__ == "__main__":
    app = Calculator()  #Create an instance of the Calculator class
    app.mainloop()  #Start the Tkinter event loop to display the GUI and handle events