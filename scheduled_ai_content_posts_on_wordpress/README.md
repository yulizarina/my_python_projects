#SCHEDULED AI CONTENT CREATOR IN WORDPRESS
    #### Video Demo:  https://youtu.be/fpiNbmPD2Ns
    #### Description:

This Python project automates the process of generating math articles for a WordPress site, based on topics from a CSV file. It uses the OpenAI API to create the content and then publishes it on the WordPress site. Scheduling allows space out posting 24 hours apart, which could be customized.

TODO
import os
import unicodedata
from openai import OpenAI
from fpdf import FPDF
import csv
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.taxonomies import GetTerms
import time

Setup
Install the required libraries using pip:

openai
fpdf
python-dotenv
wordpress-xmlrpc

Set up environment variables:

Create a .env file in the project directory with the following content:

makefile

OPENAI_API_KEY=your_openai_api_key
WORDPRESS_USERNAME=your_wordpress_username
WORDPRESS_PASSWORD=your_wordpress_password
Replace your_openai_api_key, your_wordpress_username, and your_wordpress_password with your actual API key, WordPress username, and password.

Ensure the gmat_topics.csv file contains the topics you want to generate articles for, in the format:

category,topic,sections

MAIN FUNCTION:

main() function initiates a loop that iterates 36 times (from i=1 to i!=37). During each iteration, it performs the following tasks:

It calls the extract_topic(i) function to extract the category, topic, and sections for the current iteration i.
It prints the extracted topic information using print(extract_topic(i)).
It calls the creates_article_with_open_ai(topic, sections) function to generate a math article based on the extracted topic and sections.
It prints the generated math article using print(creates_article_with_open_ai(topic, sections)).
It calls the creates_pdf(i,topic,math_article) function to create a PDF file for the generated article.
It calls the psts_to_wordpress(category,topic,math_article) function to post the generated article to a WordPress website.
It increments the i variable by 1 for the next iteration.
it includes a time delay of 15 seconds using time.sleep(15) between each iteration. This delay ensures that the program waits for {the amount of time you want it to wait} seconds before processing the next line, as commented in the code.

EXTRACT_TOPIC() FUNCTION:

The extract_topic(i) function reads a CSV file named 'gmat_topics.csv' and extracts information from the ith row of the file. Here's a step-by-step description of what the code does:

Opens the 'gmat_topics.csv' file in read mode ('r') using the open() function with a context manager (with open(...) as csvfile:). The newline='' argument is used to handle newlines in the file correctly.
Creates a CSV reader object (csvreader) using the csv.reader() function, which allows iterating over the CSV file's rows.
Skips the first i rows of the CSV file using a for loop and the next(csvreader) function. This moves the reader to the (i+1)th row, as the rows are zero-indexed.
Reads the (i+1)th row of the CSV file using row = next(csvreader).
Extracts three variables (category, topic, and sections) from the row based on their positions in the row. It assumes that category is in the first column (0-indexed), topic is in the second column, and sections is in the third column.
Returns the extracted variables category, topic, and sections.
Overall, this function is designed to read a specific row (specified by i) from a CSV file and extract the values in that row to be used in other parts of the program

CREATE_ARTICLES_WITH_OPENAI FUNCTION:

The creates_article_with_open_ai(topic, sections) function generates a math article using the OpenAI API based on the provided topic and sections. Here's a breakdown of what the function does:

Initializes an empty string math_article to store the generated article.
Loads environment variables from a .env file using load_dotenv(). This assumes that the .env file contains the OPENAI_API_KEY needed to authenticate with the OpenAI API.
Instantiates an OpenAI client (client) using the OpenAI class and the API key loaded from the environment variables.
Constructs a prompt string (prompt) for the OpenAI API. The prompt requests the generation of a math article for a WordPress site with specific requirements for title, sections, tone, length, structure, and keywords.
Calls the OpenAI API's completions.create method to generate the article based on the prompt. The stream=True parameter indicates that the API response should be streamed.
Iterates over the response chunks from the API (stream) and appends the generated content to the math_article string.
Returns the generated math_article

CREATES_PDF FUNCTION:

The creates_pdf(i, topic, math_article) function creates a PDF file containing the generated math article. Here's a breakdown of what the function does:

Creates an instance of the FPDF class to work with PDF files.
Adds a new page to the PDF.
Sets the title of the PDF to the provided topic.
Sets the font of the PDF to Arial with a font size of 11.
Normalizes the math_article text to remove any characters that cannot be encoded. This is done to ensure compatibility with the FPDF library.
Adds the normalized math_article to the PDF, using pdf.multi_cell(0, 10, normalized_article) to add multi-line text with a cell height of 10.
Constructs the name of the PDF file based on the index i and the topic.
Outputs the PDF file with the constructed name (article_name).
Overall, this function takes the generated math article and saves it as a PDF file, using the provided topic as the title of the PDF

PSTS_TO_WORDPRESS FUNCTION:

The psts_to_wordpress(category, topic, math_article) function is responsible for posting the generated math article to a WordPress site. Here's a breakdown of what the function does:

Retrieves the WordPress username and password from environment variables using os.getenv('WORDPRESS_USERNAME') and os.getenv('WORDPRESS_PASSWORD').
Creates a client object for interacting with the WordPress site using the Client class from wordpress_xmlrpc.
Creates a new WordPress post object (WordPressPost()).
Sets the title of the post to the provided topic and the content of the post to the generated math_article.
Assigns the post to a category specified by the category variable.
Creates a new post on the WordPress site using client.call(posts.NewPost(post)) and stores the post ID in the post.id attribute.
Sets the post status to "publish" to ensure that the post is published on the site.
Updates the post on the WordPress site with the new status using client.call(posts.EditPost(post.id, post)).
Overall, this function takes the generated math article and posts it to a WordPress site under the specified category.

USAGE:
python project.py
