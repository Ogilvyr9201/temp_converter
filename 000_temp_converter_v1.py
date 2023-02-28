from tkinter import *
from functools import partial  # to prevent unwantned windows


class Converter:

    def __init__(self):

        # initialise variables (such as the feedback variable)
        self.var_feedback = StringVar()
        self.var_feedback.set("")

        self.var_has_error = StringVar()
        self.var_has_error.set("no")

        self.all_calculations = []

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

        # error = "<error> Please enter a number."

        self.output_label = Label(self.temp_frame,
                                  text="",
                                  fg="#AA0000")

        self.output_label.grid(row=3)

        self.button_frame = Frame(self.temp_frame)
        self.button_frame.grid(row=4)

        self.to_celsius_button = Button(self.button_frame,
                                        text="To Celsius",
                                        font=button_font, width=12,
                                        bg="#990099",
                                        fg=button_fg,
                                        command=lambda: self.temp_convert(-459))
        self.to_celsius_button.grid(row=0, column=0,
                                    padx=5, pady=5)

        self.to_fahrenheit_button = Button(self.button_frame,
                                           text="To Fahrenheit",
                                           font=button_font, width=12,
                                           bg="#009900",
                                           fg=button_fg,
                                           command=lambda: self.temp_convert(-273))
        self.to_fahrenheit_button.grid(row=0, column=1,
                                       padx=5, pady=5)

        self.help_info_button = Button(self.button_frame,
                                       text="Help / info",
                                       font=button_font, width=12,
                                       bg="#CC6600",
                                       fg=button_fg,
                                       command=self.to_help)
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

        response = self.temp_entry.get()

        # check that user has entered a valid number...
        try:
            response = float(response)

            if response < min_value:
                has_error = "yes"

        except ValueError:
            has_error = "yes"

        # Sets var_has_error so that entry box and
        # Labels can be correctly formatted by formatting function
        if has_error == "yes":
            self.var_has_error.set("yes")
            self.var_feedback.set(error)
            return "invalid"

        # If we have no errors
        else:
            # Set to 'no' case of previous errors
            self.var_has_error.set("no")

            # return number to be
            # converted and enabled history button
            self.history_export_button.config(state=NORMAL)
            return response

    @staticmethod
    def round_ans(val):
        val_rounded = (2 * val + 1) // 2
        return "{:.0f}".format(val_rounded)

    # check temperature is valid and convert it
    def temp_convert(self, min_val):
        deg_sign = u'\N{DEGREE SIGN}'
        to_convert = self.check_temp(min_val)
        set_feedback = "yes"
        answer = ""
        from_to = ""

        if to_convert == "invalid":
            set_feedback = "no"

        elif min_val == -459:
            # do calculation
            answer = (to_convert - 32) * 5 / 9
            from_to = "{} F{} is {} C{}"

        else:
            # do calculation
            answer = to_convert * 1.8 + 32
            from_to = "{} C{} is {} F{}"

        if set_feedback == "yes":
            to_convert = self.round_ans(to_convert)
            answer = self.round_ans(answer)

            # create user output and add to calculation history
            feedback = from_to.format(to_convert, deg_sign,
                                      answer, deg_sign)
            self.var_feedback.set(feedback)

            self.all_calculations.append(feedback)

        self.output_answer()

    # show an output
    def output_answer(self):
        output = self.var_feedback.get()
        has_errors = self.var_has_error.get()

        if has_errors == "yes":
            # red text, pint entry box
            self.output_label.config(fg="#9C0000")
            self.temp_entry.config(bg="#F8CECC")

        else:
            self.output_label.config(fg="#004C00")
            self.temp_entry.config(bg="#FFFFFF")

        self.output_label.config(text=output)

    def to_help(self):
        DisplayHelp(self)


class DisplayHelp:

    def __init__(self, partner):
        # set up dialogue box and backround colour
        background = "#ffe6cc"
        self.help_box = Toplevel()

        # disable help button
        partner.help_info_button.config(state=DISABLED)

        # if users press cross at top, closes help and
        # 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDON',
                               partial(self.close_help, partner))

        self.help_frame = Frame(self.help_box, width=300, height=200,
                                bg=background)
        self.help_frame.grid()

        self.help_heading = Label(self.help_frame,
                                  text="Help / Info", bg=background,
                                  font=("Arial", "23", "bold"))
        self.help_heading.grid(row=0)

        help_text = "To use this program, simply enter the temperature " \
                    "you wish to convert and then choose to convert " \
                    "either degrees Celsius (centigrade) or " \
                    "Fahrenheit. \n\n" \
                    " Note that -273 degrees C " \
                    "(-459 F) is absolute zero (the coldest possible " \
                    "temperature). If you try to convert a " \
                    "temperature that is less than -273 degrees C, " \
                    "you will get an error message. \n\n " \
                    "to see your calculation history and export it to a " \
                    "text file, please click the 'History / Export' button. "

        self.help_text_label = Label(self.help_frame, bg=background,
                                     text=help_text, wraplength=350,
                                     justify="left")
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#CC6600",
                                     fg="#FFFFFF",
                                     command=partial(self.close_help,
                                                     partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

    # closes help dialogue (used by button and x at top of dialogue)
    def close_help(self, partner):
        # Put help button back tp normal...
        partner.help_info_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine

if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
