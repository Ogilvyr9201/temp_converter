from tkinter import *
from functools import partial  # to prevent unwanted windows
from datetime import date
import re

degree_sign = u'\N{DEGREE SIGN}'


class Converter:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold with white text
        button_font = ("Arial", "14")
        button_fg = "#FFFFFF"

        # five item list
        self.all_calculations = ['0 °F is -18 °C', '0 °C is 32 °F',
                                 '30 °F is -1 °C', '30 °C is 86 °F',
                                 '40 °F is 4 °C', '100 °C is 212 °F']
        # # six item list
        # self.all_calculations = ['0 F° is -18 C°', '0 c° is 32f°',
        #                          '30 F° is -1 C°', '30 C° is 86 F°',
        #                          '40 F° is 4 C°', '100 C° is 212 F°']

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.history_button = Button(self.button_frame,
                                     text="History / Export",
                                     font=button_font, width=12,
                                     bg="#004C99",
                                     fg=button_fg,
                                     command=self.to_history)
        self.history_button.grid(row=1, column=0,
                                 padx=5, pady=5)

    def to_history(self):
        DisplayHistory(self, self.all_calculations)


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
        partner.history_button.config(state=DISABLED)

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
        partner.history_button.config(state=NORMAL)
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
        for item in range(0, stop - 1):
            calc_string += var_calculations[len(var_calculations) - item - 1]
            calc_string += "\n"

        # add final item without an extra linebreak
        # ie: last item on list will be fith from the end!
        calc_string += var_calculations[-max_calcs]

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
