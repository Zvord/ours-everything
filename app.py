from flask import Flask, render_template, request
import pymorphy3
import random

app = Flask(__name__)
morph = pymorphy3.MorphAnalyzer()

# List of 10 most used Russian nouns (you can adjust this list as needed)
TOP_NOUNS = [
    "слово", "человек", "время", "дело", "жизнь",
    "день", "рука", "работа", "место", "право"
]

# Mapping of case grammemes to their human-readable names.
CASE_OPTIONS = {
    "nomn": "Nominative",
    "gent": "Genitive",
    "datv": "Dative",
    "accs": "Accusative",
    "ablt": "Instrumental",
    "loct": "Prepositional"
}

# Mapping of number grammemes to names.
NUMBER_OPTIONS = {
    "sing": "Singular",
    "plur": "Plural"
}

def generate_question(selected_cases, selected_numbers):
    noun = random.choice(TOP_NOUNS)
    # Randomly select a case and a number from the chosen options.
    case = random.choice(selected_cases) if selected_cases else "gent"
    number = random.choice(selected_numbers) if selected_numbers else "sing"
    p = morph.parse(noun)[0]
    # Attempt to inflect the noun to the chosen case and number.
    inflected_obj = p.inflect({case, number})
    inflected = inflected_obj.word if inflected_obj else "Error"
    return noun, case, number, inflected

@app.route('/forward_drill', methods=['GET', 'POST'])
def forward_drill():
    feedback = None

    # Get training options from the form (if present)
    selected_cases = request.form.getlist("cases")
    selected_numbers = request.form.getlist("numbers")

    # If the user hasn't selected any options, set defaults.
    if not selected_cases:
        selected_cases = ["gent"]  # default to Genitive
    if not selected_numbers:
        selected_numbers = ["sing"]  # default to Singular

    # On a POST request, determine the action.
    if request.method == 'POST':
        action = request.form.get("action")
        if action == "submit":
            # Validate the user's answer.
            user_input = request.form.get('answer')
            correct_answer = request.form.get('correct_answer')
            question = request.form.get('question')
            current_case = request.form.get('current_case')
            current_number = request.form.get('current_number')
            if user_input.strip().lower() == correct_answer.strip().lower():
                feedback = "Correct!"
            else:
                feedback = f"Incorrect. The correct answer is {correct_answer}."
            # After answer validation, generate a new question.
            question, current_case, current_number, correct_answer = generate_question(selected_cases, selected_numbers)
        elif action == "next":
            # Generate a new question without checking an answer.
            question, current_case, current_number, correct_answer = generate_question(selected_cases, selected_numbers)
    else:
        # On initial GET, use defaults and generate a new question.
        selected_cases = ["gent"]
        selected_numbers = ["sing"]
        question, current_case, current_number, correct_answer = generate_question(selected_cases, selected_numbers)

    return render_template(
        "forward_drill.html",
        question=question,
        correct_answer=correct_answer,
        feedback=feedback,
        selected_cases=selected_cases,
        selected_numbers=selected_numbers,
        current_case=current_case,
        current_number=current_number,
        case_options=CASE_OPTIONS,
        number_options=NUMBER_OPTIONS
    )

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
