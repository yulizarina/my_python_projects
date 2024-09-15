import sys
from pdf2image import convert_from_path

# Check if the user provided a file as an argument
if len(sys.argv) < 2:
    print("Please provide the PDF file as an argument.")
    sys.exit()

# Get the PDF file from the command-line arguments
pdf_file = sys.argv[1]

# Convert PDF to images
images = convert_from_path(pdf_file)

# Save each image
for i, image in enumerate(images):
    image.save(f'page_{i+1}.png', 'PNG')
