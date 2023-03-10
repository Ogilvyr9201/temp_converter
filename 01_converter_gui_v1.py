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
                                       wraplength=250, width=40,
                                       justify="left")
        self.temp_instructions.grid(row=1)

        self.temp_entry = Entry(self.temp_frame,
                                font=("Arial", "14")
                                )
        self.temp_entry.grid(row=2, padx=10, pady=10)

        error = "<error> Please enter a number."

        self.temp_error = Label(self.temp_frame,
                                text="",
                                fg="#AA0000")

        self.temp_error.grid(row=3)

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.to_celsius_button = Button(self.button_frame,
                                        text="To Celsius",
                                        font=button_font, width=12,
                                        bg="#990099",
                                        fg=button_fg,
                                        command=self.to_celsius)
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

    def check_temp(self, min_value):
        has_error = "no"
        error = "Please enter a number that is more then {}".format(min_value)

        # check that user has entered a valid number...
        try:
            response = self.temp_entry.get()
            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # if number is invalid display error message
        if has_error == "yes":
            self.temp_error.config(text=error, fg="#9C0000")
        else:
            self.temp_error.config(text="You are OK", fg="blue")

            # if we have at least one valid calculation
            # enable history button
            self.history_export_button.config(state=NORMAL)
            return response

    # check temperature is more then -459 adn convert it
    def to_celsius(self):

        self.check_temp(-459)


# main routine

if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
