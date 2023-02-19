from tkinter import *

class Converter:


    def __init__(self):

        # common format for all buttons
        # Arial size 14 bold with white text
        button_font = ("Arial", "14")
        button_fg = "#FFFFFF"

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.temp_heading = Label(self.temp_frame,
                                  text="Temperature Converter",
                                  font=("Arial", "16", "bold")
                                  )
        self.temp_heading.grid(row=0)

        instructions = "Please enter a temperature below and " \
                       "then press ome of the buttons to convert " \
                       "it from centigrade to Fahrenheit."
        self.temp_instructions = Label(self.temp_frame,
                                       text=instructions,
                                       wrap=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error_label = "<error> Please enter a number."

        self.temp_error = Label(self.temp_frame,
                               text=error_label,
                               fg="#AA0000")

        self.temp_error.grid(row=3)

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.to_celsius_button = Button(self.button_frame,
                                         text="To Celsius",
                                         font=button_font, width=12,
                                         bg="#990099",
                                         fg=button_fg)
        self.to_celsius_button.grid(row=0, column=0)

        self.to_fahrenheit_button = Button(self.button_frame,
                                        text="To Fahrenheit",
                                        font=button_font, width=12,
                                        bg="#009900",
                                        fg=button_fg,
                                        )
        self.to_fahrenheit_button.grid(row=0, column=1,
                                       padx=5, pady=5)

        self.help_info_button = Button(self.button_frame,
                                           text="Help / info",
                                           font=button_font, width=12,
                                           bg="#CC6600",
                                           fg=button_fg)
        self.help_info_button.grid(row=1, column=0,
                                       padx=5, pady=5)

        self.history_export_button = Button(self.button_frame,
                                       text="History / Export",
                                       font=button_font, width=12,
                                       bg="#004C99",
                                       fg=button_fg,
                                       state=DISABLED)
        self.history_export_button.grid(row=1, column=1,
                                   padx=5, pady=5)





# main routine

if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()

