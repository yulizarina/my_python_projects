import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import csv

# Read dates from the CSV file
class_dates = []
months=[]
with open('class_dates2.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        class_dates.append(row[0])
        if int(row[0][5:7]) not in months:
            months.append(int(row[0][5:7]))

print(class_dates)

# Convert string dates to datetime objects
class_dates = [datetime.strptime(date, "%Y-%m-%d") for date in class_dates]

# Function to draw the calendar
def draw_calendar(c, year, month, class_dates):
    if month == 1:
        month_name = "January"
    elif month == 2:
        month_name = "February"
    elif month == 3:
        month_name = "March"
    elif month == 4:
        month_name = "April"
    elif month == 5:
        month_name = "May"
    elif month == 6:
        month_name = "June"
    elif month == 7:
        month_name = "July"
    elif month == 8:
        month_name = "August"
    elif month == 9:
        month_name = "September"
    elif month == 10:
        month_name = "October"
    elif month == 11:
        month_name = "November"
    elif month == 12:
        month_name = "December"

    c.setFont("Helvetica-Bold", 14)
    c.setStrokeColorRGB(68/255, 63/255, 72/255)
    c.drawString(3 * inch, 10.5 * inch, f"Class attendance for {month_name} {year}")
    c.setFont("Helvetica", 12)


    # Draw the days of the week
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        c.drawString((0.5+0.5 * i) * inch, 9.5 * inch, day)

    # Find the first day of the month
    first_day = datetime(year, month, 1)
    start_day = first_day.weekday()  # Monday = 0, Sunday = 6
    if start_day == 6:
        start_day = -1  # To adjust the starting position for Sunday

    # Draw the dates in the calendar
    y = 9.0 * inch
    x = (start_day + 1) * 0.5 * inch  # Start position for the first day

    current_date = first_day
    while current_date.month == month:
        if current_date in class_dates:
            c.setStrokeColorRGB(121/255, 35/255, 207/255)  # Purple for the circle outline
            c.setFillColorRGB(121/255, 35/255, 207/255)
            c.circle(x +0.1 * inch, y, 0.2 * inch) # Draw a circle around the date
            c.setFillColorRGB(121/255, 35/255, 207/255)  # Reset to black for the date text
        else:
            c.setFillColorRGB(68/255, 63/255, 72/255)  # Black for normal dates
        c.drawString(x, y, str(current_date.day))
        current_date += timedelta(days=1)
        x += 0.5 * inch
        if current_date.weekday() == 6:
            y -= 0.5 * inch
            x = 0.5 * inch

    c.setFillColorRGB(0, 0, 0)  # Reset color to black

# Create a PDF file
pdf_file = "class_calendar_highlighted.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)

print(months)
for each_month in months:
# Draw the calendars for January and February
    draw_calendar(c, 2024, each_month, class_dates)
    c.showPage()

# Save the PDF
c.save()

pdf_file
