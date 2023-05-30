# Build a platform, paste your endpoint, the application should download 50 questions, Save and number them,
# in a pdf. The application should fetch the following ; Title of Question, Total views, Read the link on 
#the pdf, and Picture of the Question.

import requests
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

url = input("Input your endpoint: ")
filename = input("Enter the filename for the PDF file: ")
print()

params = {
    "pagesize": 50
}

# Make the request
response = requests.get(url, params)
questions = response.json()

pdf_path = os.path.join(sys.path[0], "ques.pdf")

# Create a new PDF file
c = canvas.Canvas(pdf_path, pagesize=letter)

# Set initial y coordinate for drawing on the canvas
y = 700

# Set initial question number
question_number = 1

# Set maximum number of questions per page
max_questions_per_page = 5

# Iterate over questions in reverse order
for index, myquestion in enumerate(reversed(questions['items'])):
    # Check if a new page is needed
    if index != 0 and index % max_questions_per_page == 0:
        c.showPage()
        y = 700  # Reset y coordinate for new page

    question_title = myquestion['title']
    question_views = myquestion['view_count']
    question_answered = myquestion['is_answered']
    question_link = myquestion['link']
    question_image = myquestion.get('image', '')

    # Write question number and details onto the PDF
    c.drawString(50, y, f"Question #{question_number}")
    c.drawString(70, y - 20, f"Title: {question_title}")
    c.drawString(70, y - 40, f"Views: {question_views}")
    c.drawString(70, y - 60, f"is_answered: {question_answered}")
    c.drawString(70, y - 80, f"Link: {question_link}")
    c.drawString(70, y - 100, f"Image: {question_image}")
    c.drawString(50, y - 120, "")  # Leave some space between questions

    # Adjust the y coordinate for the next question
    y -= 140  # Increase the y coordinate to provide more space

    # Increment the question number
    question_number += 1

    # Print data on the terminal
    print(f"Question title: {question_title}")
    print(f"Question view count: {question_views}")
    print(f"Question answer status: {question_answered}")
    print(f"Question link: {question_link}")
    print(f"Question image: {question_image}")
    print()

    # Break the loop if the desired number of questions is reached
    if question_number > 50:
        break

# Save and close the PDF file
c.save()
print("PDF file created successfully.")
input("Press Enter to exit...")

