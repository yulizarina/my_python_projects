import os
import unicodedata
import pytest
from dotenv import load_dotenv
from unittest.mock import patch, call
from project import extract_topic, creates_article_with_open_ai, creates_pdf, psts_to_wordpress

def main():
    test_extract_topic()
    test_creates_article_with_open_ai()
    test_creates_pdf()
    test_psts_to_wordpress()

def test_extract_topic():
    # Define the expected values for each test case
    test_cases = [
        ['Value Order Factors', 'Types of Numbers', '(natural, whole, integer, rational, irrational)'],
        ['Value Order Factors', 'Absolute Value', '(definition as a distance on a number line, graph)'],
        ['Value Order Factors', 'Factors, Multiples, divisibility', '(consecutive integer, divisor, factor, common factor, divisible, multiple )'],
        ['Value Order Factors', 'Quotient, remainder', '(Quotient, remainder, polynomial remainder theorem, factor theorem)'],
        ['Value Order Factors', 'Even and odd integers', '(Even, consecutive even integers, odd, consecutive odd integers)'],
        ['Value Order Factors', 'Prime and composite numbers', '(Prime numbers, composite numbers, mutually prime, gcf, lcm)'],
        ['Value Order Factors', 'Exponents', '(Power properties formulae, including zero exponent, fractional exponent, negative exponent)'],
        ['Value Order Factors', 'Decimals and place value', '(tens, units, tenth, hundrieth, thousandth. How to write a variable with unknown tens, hundreths and thousands and write the equations with them)'],
        ['Value Order Factors', 'Scientific notation', '(formula for scientific notation, examples of coversion from scientific notation and vice verca)'],
        ['Value Order Factors', 'Properties of operations', '(PEDMAS, converting from word expressions to math expression)'],
        ['Algebra Equalities Inequalities', 'Linear Equations', 'how to solve linear equation step-by-step and example'],
        ['Algebra Equalities Inequalities', 'Factoring and Quadratic Equations', '(solve quadtratic equations by factoring, by using quadratic formula, Vietas Theorem)'],
        ['Algebra Equalities Inequalities', 'Inequalities', '(how to solve linear inequality, quadratic inequality, multiplying inequality by a negative number, graphical solution)'],
        ['Algebra Equalities Inequalities', 'Functions', '(linear, quadratic, polynomial, exponential, hyperbola function y=1/x)'],
        ['Algebra Equalities Inequalities', '(Formulas and Measurement Conversion', 'converting km to miles, m2 to cm2, m3 to cm3)'],
        ['Rates Ratios Percent', 'Ratio and proportion', 'Ways to solve word problems with ratios'],
        ['Rates Ratios Percent', 'Fractions and decimals', 'converting fractions to decimal and vice versa'],
        ['Rates Ratios Percent', 'Percent', 'Finding a value by creating percentage ratio'],
        ['Rates Ratios Percent', 'Percent of change', 'Percent of change formula'],
        ['Rates Ratios Percent', 'Discounts and sales tax', 'Formula for calculating amount after Discounts and after sales tax and when its combination of both'],
        ['Rates Ratios Percent', 'Compound interest', 'Compound interest formula for exponential growth or decay'],
        ['Rates Ratios Percent', 'Converting decimals and fractions to percent', 'Converting decimals to percent and Converting fractions to percent'],
        ['Rates Ratios Percent', '(Work, rate, and mixture problems)', '(rate formula, Work formula, combined work time formula, mixture formula, examples of solutions)'],
        ['Probability and Statistics', 'Statistics', '(Mean, median, standard deviation, first quartile, third quartile, range)'],
        ['Probability and Statistics', 'Sets', '(union and intersection of 2 sets, joint and disjoin events, vienn diagram, general addition rule for 2 sets, for 3 sets)'],
        ['Probability and Statistics', 'Counting methods', '(Multiplication principle, addition principle, subtraction principle, factorial, permutation, combination with and without repetitions, examples with coins, dice, playing cards)'],
        ['Probability and Statistics', 'Probability', '(Calculating probability, mutually exclusive events, independend events, dependend events, complex probability problems)'],
        ['Probability and Statistics', 'Estimation', '(Round up and round down,complex arithmetic calculations, upper and lower bounds)'],
        ['Probability and Statistics', 'Sequences', '(arithmetic and geometric sequence and neither, explicit recursive formulae, sum of a series)'],
        ['Geometry', 'Lines and angles', '(Vertical angles, supplementary, complementary, angles formed by parallel lines and a transversal, sum of angles in a triangle and polygon)'],
        ['Geometry', 'Polygons', '(types of polygons, regular polygon properties, property of a hexagon)'],
        ['Geometry', 'Triangles', '(Special right triangles, egyptian triangles, pythagorean theorem, isosceles, equilateral triangles, area of a triangle formula)'],
        ['Geometry', 'Quadrilaterals', '(Types of quadrilateral, area formulae)'],
        ['Geometry', 'Circles', '(Circumference formula, area of a circle, of a sector, of a segment, length of an arc, central angle, inscribed angle)'],
        ['Geometry', 'Solids', '(Edge, face, vertex, Volume of a spere, rectangular solid, cone, cylinder, surface area)'],
        ['Geometry', 'Coordinate geometry', '(origin, axis, quadrants, distance between 2 points, Linear function slope-intercept form, types of a slope: positive, negative, zero, undefined, slope formula, x-intercept, y-intercept, quadratic function and its standard form, vertex form, intercept form)']
    ]


    # Iterate over each test case
    for i, test_case in enumerate(test_cases, start=1):
        # Extract the values
        category, topic, sections = extract_topic(i)

        # Check if the extracted values match the expected values
        assert category == test_case[0]
        assert topic == test_case[1]
        assert sections == test_case[2]

def test_creates_article_with_open_ai():
    load_dotenv()
   # Set the expected API key
    expected_api_key = os.getenv('OPENAI_API_KEY')

    with patch('project.OpenAI') as mock_openai:
        # Call the function
        creates_article_with_open_ai('topic', 'sections')

        # Check if the OpenAI client was created with the correct API key
        assert mock_openai.call_args[1]['api_key'] == expected_api_key

def test_creates_pdf():

    i = 1
    topic = 'Math Topic'
    math_article = 'Math Article Content'

    # Call the function to create the PDF
    creates_pdf(i, topic, math_article)

    # Normalize the article name to remove any characters that cannot be encoded
    normalized_topic = unicodedata.normalize('NFKD', topic).encode('ascii', 'ignore').decode('utf-8')

    # Define the expected file name
    expected_file_name = f"{i}. {normalized_topic}.pdf"

    # Check if the file was created
    assert os.path.exists(expected_file_name)

    # Clean up: Delete the created file
    os.remove(expected_file_name)

def test_psts_to_wordpress():
    load_dotenv()
        # Set the expected username and password
    expected_username = os.getenv('WORDPRESS_USERNAME')
    expected_password = os.getenv('WORDPRESS_PASSWORD')
    expected_title = 'Types of Numbers'
    expected_category = 'Value Order Factors'

    with patch('project.Client') as mock_client:
        # Call the function
        psts_to_wordpress(expected_category, expected_title, 'math_article')

        # Check if the Client was created with the correct arguments
        mock_client.assert_called_once_with('https://gmatmathprep.online/xmlrpc.php', expected_username, expected_password)

        # Check if the post was published with the correct title and category
        expected_post_data = {
            'post_title': expected_title,
            'post_content': 'math_article',
            'post_status': 'publish',
            'terms_names': {'category': [expected_category]}
        }
        mock_client.return_value.call.assert_called()

if __name__ == "__main__":
    main()
