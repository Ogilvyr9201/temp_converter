from datetime import date
degree_sign = u'\N{DEGREE SIGN}'


# retrieves date and creates YYYY_MM_DD
def get_date():
    today = date.today()

    day = today.strftime("%d")
    month = today.strftime("%m")
    year = today.strftime("%Y")

    return "{}/{}/{}".format(day, month, year)


all_calculations = ['0 {}F is -18 {}C', '0 {}C is 32 {}F',
                    '30 {}F is -1 {}C', '30 {}C is 86 {}F',
                    '40 {}F is 4 {}C', '100 {}C is 212 {}F']

# file heading
file_heading = "**** Temperature Calculations ****"

file_date = "Generated: {}".format(get_date())

to_write = [file_heading, file_date, "Your Calculation History:"]

text_file = open("blah.txt", "w+")

for item in to_write:
    text_file.write(item)
    text_file.write("\n\n")

for item in all_calculations:
    text_file.write(item.format(degree_sign, degree_sign))
    text_file.write("\n")
