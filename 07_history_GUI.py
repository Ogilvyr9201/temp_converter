from tkinter import *
from functools import partial  # to prevent unwantned windows


class Converter:

    def __init__(self):
        # common format for all buttons
        # Arial size 14 bold with white text
        button_font = ("Arial", "14")
        button_fg = "#FFFFFF"

        # five item list
        # self.all_calculations = ['0 F° is -18 C°', '0 c° is 32f°',
        #                          '30 F° is -1 C°', '30 C° is 86 F°',
        #                          '40 F° is 4 C°']

        # six item list
        self.all_calculations = ['0 F° is -18 C°', '0 c° is 32f°',
                                 '30 F° is -1 C°', '30 C° is 86 F°',
                                 '40 F° is 4 C°', '100 C° is 212 F°']

        # Set up GUI Frame
        self.temp_frame = Frame(padx=10, pady=10)
        self.temp_frame.grid()

        self.button_frame = Frame(padx=30, pady=30)
        self.button_frame.grid(row=0)

        self.history_button = Button(self.button_frame,
                                     text="History / Export",
                                     font=button_font, width=12,
                                     bg="#CC6600",
                                     fg=button_fg,
                                     command=self.to_history)
        self.history_button.grid(row=1, column=0,
                                 padx=5, pady=5)

    def to_history(self):
        DisplayHistory(self)


class DisplayHistory:

    def __init__(self, partner):
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

        self.history_text_label = Label(self.history_frame,
                                        text=history_text, wraplength=300,
                                        justify="left",
                                        width=45, padx=10, pady=10, )
        self.history_text_label.grid(row=1, padx=10)

        self.user_history_label = Label(self.history_frame,
                                        text="Calculations go here",
                                        width=40,
                                        padx=10, pady=10,
                                        justify="left",
                                        bg=background)
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

        self.file_name_entry = Entry(self.history_frame,
                                     font=("Arial", "14"),
                                     bg="#FFFFFF", width=25)
        self.file_name_entry.grid(row=4, padx=10, pady=10)

        self.filename_error = Label(self.history_frame,
                                    text="Filename error goes here",
                                    font=("Arial", "12", "bold"),
                                    fg="#9C0000")
        self.filename_error.grid(row=5)

        self.button_frame = Frame(self.history_frame)
        self.button_frame.grid(row=6)

        self.dismiss_button = Button(self.button_frame,
                                     font=("Arial", "12", "bold"),
                                     text="Export", bg="#004C99",
                                     fg="#FFFFFF", width=12)
        self.dismiss_button.grid(row=0, column=0, padx=10, pady=10)

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


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Temperature Converter")
    Converter()
    root.mainloop()
