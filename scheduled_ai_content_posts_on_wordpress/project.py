import os
import unicodedata
from openai import OpenAI
from fpdf import FPDF
import csv
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import time

def main():
    i=1
    while i!=3:
        topic, sections = extract_topic(i)
        print(extract_topic(i))
        math_article=creates_article_with_open_ai(topic, sections)
        print(creates_article_with_open_ai(topic, sections))
        creates_pdf(i,topic,math_article)
        #psts_to_wordpress()
        i+=1

def extract_topic(i):
    # Replace 'your_file.csv' with the path to your actual CSV file
    with open('gmat_topics.csv', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
         # Skip the first i rows (0-indexed) to get to row i+1
        for _ in range(i):
            next(csvreader)

    # Read the third row
        row = next(csvreader)

    # Extract variables from the row
        #var1 = row[0]  # Assuming the variable is in the first column (0-indexed)
        topic = row[1]  # Assuming the variable is in the second column (0-indexed)
        sections = row[2]
    # Print or use the extracted variables
        return topic, sections

def creates_article_with_open_ai(topic, sections):
    math_article=""
    #category=var1
    # Load environment variables from .env file
    load_dotenv()

        # Get API key from environment variables
    client = OpenAI(
            # This is the default and can be omitted
        api_key = os.getenv('OPENAI_API_KEY'))

        # The prompt to generate a math article
    prompt = f"""
        Generate a math article for my WordPress site.
        Please write an article with the title {topic}. Sections must include: {sections}
        The article should begin immediately with content. The tone should be scientific and consice. Language should be formal and precise, avoid colloquialisms and overly descriptive language.
        Purpose: To give students all the nesessary formulae, concepts, rules to be able to score high on quantitative section of GMAT exam Examples: Include an example for each formula and concept
        Length: between 250 to 1000 words. Structure the article with clear headings for each section.
        At the end of an article there should be very short cliffnotes of this article labeled as Recap.
        Provide 10 relative keywords for that article for seo.
        """

        # Call the OpenAI API to generate a response
    stream = client.chat.completions.create(
        model="gpt-4", # or another appropriate model
        messages=[{"role": "user", "content": prompt}],
        stream=True,
            )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            math_article += chunk.choices[0].delta.content
    #math_article="hello"
         # The generated text will be in response.choices[0].text
    return math_article

def creates_pdf(i,topic,math_article):

# Create instance of FPDF class
    pdf = FPDF()
    pdf.add_page()

# Set the title
    pdf.set_title(topic)

# Add content
    pdf.set_font("Arial", size=11)
    # Normalize the math_article to remove any characters that cannot be encoded
    normalized_article = unicodedata.normalize('NFKD', math_article).encode('ascii', 'ignore').decode('utf-8')
    pdf.multi_cell(0, 10, normalized_article)

# Save the pdf with name
    article_name = f"{i}. {topic}.pdf"
    pdf.output(article_name)

def psts_to_wordpress(category,topic,math_article):

    wp_username = os.getenv('WORDPRESS_USERNAME')
    wp_password = os.getenv('WORDPRESS_PASSWORD')

         # Posting on WordPress site details
    client = Client('https://gmatmathprep.online/xmlrpc.php', wp_username, wp_password)
    post = WordPressPost()
    post.title = topic
    post.content = math_article
    post.terms_names = {
    'category': [category]
}
    post.id = client.call(posts.NewPost(post))

         # whoops, I forgot to publish it!
    post.post_status = 'publish'
    client.call(posts.EditPost(post.id, post))

if __name__ == "__main__":
    main()
