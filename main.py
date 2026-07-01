# Imports & Variables
import pandas
import datetime as dt
import random
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

# 1. Update the birthdays.csv
# This is OPTIONAL; Simpler Alternate: update file manually
birthdays = pandas.DataFrame({
    "name": ["Mom", "Dad"],
    "email": ["aanyatester@gmail.com", "aanyatester@yahoo.com"],
    "year": [1970, 1971],
    "month": [11, 7],
    "day":[12, 2],
})
new_birthdays = birthdays.to_csv("birthdays.csv", mode="w", index=False)

# 2. Check if today matches a birthday in the birthdays.csv
now = dt.datetime.now() # Alternate Code:
month = now.month           # today = (dt.datetime.now().month, dt.datetime.now().day)
day = now.day

birthdays_data = pandas.read_csv("birthdays.csv")
# Alternate code: use a dictionary comprehension to create a birthday_dict
# Syntax- birthdays_dict = {(data_row["month"], data_row["day"]) : data_row for (index, data_row) in data.iterrows()}
birthday_exists = ((birthdays_data["month"] == month) & (birthdays_data["day"] == day)).any()

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# Alternate Code- if today in birthdays_dict:
if birthday_exists:
    person = birthdays_data[(birthdays_data["month"] == month) & (birthdays_data["day"] == day)]["name"].item()
    person_email = birthdays_data[(birthdays_data["month"] == month) & (birthdays_data["day"] == day)]["email"].item()
    letter_choice = random.randint(1, 3)
    
    with open(f"letter_templates/letter_{letter_choice}.txt") as letter_file:
        letter = letter_file.read()
        letter = letter.replace("[NAME]", person)

    # 4. Send the letter generated in step 3 to that person's email address.
    with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PWD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs=person_email,msg=f"Subject: Happy Birthday!!!\n\n{letter}")
