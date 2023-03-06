from tkinter import *
from functools import partial  # to prevent unwanted windows
from datetime import date
import re


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
                                            state=DISABLED,
                                            command=lambda: self.to_history())
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
            from_to = "{} {}F is {} {}C"

        else:
            # do calculation
            answer = to_convert * 1.8 + 32
            from_to = "{} {}C is {} {}F"

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

    def to_history(self):
        DisplayHistory(self, self.all_calculations)


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


class DisplayHistory:

    def __init__(self, partner, calc_list):

        # set maximum number of calculations to 5
        # this can be changed if we want to show fewer /
        # more calculations
        max_calcs = 5
        self.var_max_calcs = IntVar()
        self.var_max_calcs.set(max_calcs)

        # set filename variable
        self.var_filename = StringVar()
        self.var_todays_date = StringVar()

        # set up calculation string
        self.var_calc_string = StringVar()

        # Function converts content of calculations list
        # into a string
        calc_string_text = self.get_calc_string(calc_list)
        self.var_calc_string.set(calc_string_text)

        # set up dialogue box and background colour
        background = "#ffe6cc"
        self.history_box = Toplevel()

        # disable history button
        partner.history_export_button.config(state=DISABLED)

        # if users press cross at top, closes history and
        # 'releases' history button
        self.history_box.protocol('WM_DELETE_WINDON',
                                  partial(self.close_history, partner))

        self.history_frame = Frame(self.history_box, width=300, height=200)
        self.history_frame.grid()

        self.history_heading = Label(self.history_frame,
                                     text="History / Export",
                                     font=("Arial", "23", "bold"))
        self.history_heading.grid(row=0)

        history_text = "Below are your recent calculations - showing3/3 " \
                       "calculations. all calculations are shown to the nearest " \
                       "degree."

        # customise text and background colour for calculation
        # area depending on whether all or only some calculations
        # are shown.
        num_calcs = len(calc_list)

        if num_calcs > max_calcs:
            calc_background = "#FFE6CC"  # peach
            showing_all = "Here are your recent calculations " \
                          "({}/{} calculations shown). please export your " \
                          "calculations to see your full calculation " \
                          "history".format(max_calcs, num_calcs)

        else:
            calc_background = "#B4FACB"  # pale green
            showing_all = "Below is your calculation history."

        # history text and label
        hist_text = "{}  \n\nAll calculations are shown to " \
                    "the nearest degree.".format(showing_all)
        self.history_text_label = Label(self.history_frame,
                                        text=hist_text, wraplength=300,
                                        justify="left",
                                        width=45, padx=10, pady=10, )
        self.history_text_label.grid(row=1)

        self.user_history_label = Label(self.history_frame,
                                        text=calc_string_text,
                                        width=40,
                                        padx=10, pady=10,
                                        justify="left",
                                        bg=calc_background)
        self.user_history_label.grid(row=2)

        export_text = "Either choose a custom file name (an push <Export>) " \
                      "or simply push <Export> to save your calculations in a" \
                      "text file. if the filename already exists it will be " \
                      "overwritten! "

        self.export_text_label = Label(self.history_frame,
                                       text=export_text, wraplength=300,
                                       justify="left",
                                       width=45, padx=10, pady=10, )
        self.export_text_label.grid(row=3, padx=10)

        self.filename_entry = Entry(self.history_frame,
                                    font=("Arial", "14"),
                                    bg="#FFFFFF", width=25)
        self.filename_entry.grid(row=4, padx=10, pady=10)

        self.filename_error = Label(self.history_frame,
                                    text="",
                                    font=("Arial", "12", "bold"),
                                    fg="#9C0000",
                                    wraplength=300)
        self.filename_error.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.export_button = Button(self.button_frame,
                                    font=("Arial", "12", "bold"),
                                    text="Export", bg="#004C99",
                                    fg="#FFFFFF", width=12,
                                    command=self.make_file)
        self.export_button.grid(row=0, column=0, padx=10, pady=10)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#696969",
                                     fg="#FFFFFF", width=12,
                                     command=partial(self.close_history,
                                                     partner))
        self.dismiss_button.grid(row=0, column=1, padx=10, pady=10)

    # closes history dialogue (used by button and x at top of dialogue)
    def close_history(self, partner):
        # Put history button back tp normal...
        partner.history_export_button.config(state=NORMAL)
        self.history_box.destroy()

    # change calculation list into a string so that it
    # Can be outputted as a label.
    def get_calc_string(self, var_calculations):
        # get maximum calculation to display
        # (was set in __init__ function)
        max_calcs = self.var_max_calcs.get()
        calc_string = ""

        # work out how many times we need to loop
        # to output either the last five calculations
        # or all the calculations
        if len(var_calculations) >= max_calcs:
            stop = max_calcs

        else:
            stop = len(var_calculations)

        # iterate to all but last item,
        # adding item line break to calculation string
        for item in range(0, stop):
            calc_string += var_calculations[len(var_calculations) - item - 1]
            calc_string += "\n"

        calc_string = calc_string.strip()
        return calc_string

    # makes a filename
    def make_file(self):
        # retrieve filename
        filename = self.filename_entry.get()
        filename_ok = ""

        if filename == "":
            # set filename_ok to "" so we can see
            # default name for testing purposes
            date_part = self.get_date()
            filename = "{}_temperature_calculations".format(date_part)

        else:
            # check that filename is valid
            filename_ok = self.check_filename(filename)

        if filename_ok == "":
            filename += ".txt"
            self.filename_error.config(text="File Exported",
                                       fg="#004C99")
            self.filename_entry.config(bg="#B4FACB")
            self.export_txt(filename)

        else:
            self.filename_error.config(text=filename_ok,
                                       fg="#9C0000")
            self.filename_entry.config(bg="#F8CECC")

    # gets today's date
    def get_date(self):
        today = date.today()

        day = today.strftime("%d")
        month = today.strftime("%m")
        year = today.strftime("%Y")

        todays_date = "{}_{}_{}".format(year, month, day)
        self.var_todays_date.set(todays_date)

        return "{}_{}_{}".format(year, month, day)

    # checks that filename only contains letters,
    # numbers and underscores. Returns either " if
    # OK or the problem if we have an error
    @staticmethod
    def check_filename(filename):
        problem = ""

        # regular expression to check file name is valid
        valid_char = "[A-Za-z0-9_]"

        # iterates through filename and checks each letter
        for letter in filename:
            if re.match(valid_char, letter):
                continue

            elif letter == " ":
                problem = "Sorry no spaces allowed"

            else:
                problem = ("Sorry, no {}'s allowed".format(letter))
            break

        if problem != "":
            problem = "{}. Use letters / numbers / underscores only.".format(problem)

        return problem

    # exports to txt
    def export_txt(self, filename):
        # file heading
        file_heading = "**** Temperature Calculations ****"

        # file date & calculation list
        file_date = "Generated: {}".format(self.get_date())
        get_calcs = self.var_calc_string.get()

        # list of items to write
        to_write = [file_heading, file_date, "Your Calculation History:",
                    get_calcs]

        # open file
        text_file = open(filename, "w+")

        for item in to_write:
            text_file.write(item)
            text_file.write("\n\n")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
