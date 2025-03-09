from flask import Flask, render_template, request, session, redirect, url_for
import pymorphy3
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production
morph = pymorphy3.MorphAnalyzer()

# List of 10 most used Russian nouns
TOP_NOUNS = [
    "слово", "человек", "время", "дело", "жизнь",
    "день", "рука", "работа", "место", "право"
]

# English base dictionaries for case and number names.
CASE_OPTIONS = {
    "nomn": "Nominative",
    "gent": "Genitive",
    "datv": "Dative",
    "accs": "Accusative",
    "ablt": "Instrumental",
    "loct": "Prepositional"
}
NUMBER_OPTIONS = {
    "sing": "Singular",
    "plur": "Plural"
}

# A route to set the language.
@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['en', 'ru']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('home'))

def get_translations(lang):
    """Return translation dictionaries based on the language."""
    if lang == 'ru':
        t = {
            'welcome': 'Добро пожаловать в тренировку склонения русских существительных',
            'forward_drill': 'Тренировка: Склонение существительных',
            'backward_drill': 'Тренировка: определение падежа и числа',
            'select_cases': 'Выберите падежи:',
            'select_number': 'Выберите число:',
            'convert': 'Склоните существительное',
            'into': 'в',
            'form': 'форму',
            'your_answer': 'Ваш ответ',
            'submit': 'Отправить',
            'next': 'Следующий',
            'back_home': 'Назад на главную',
            'intro_text': 'Практикуйтесь в склонении существительных на русском языке!'
        }
        case_options_display = {
            "nomn": "Именительный",
            "gent": "Родительный",
            "datv": "Дательный",
            "accs": "Винительный",
            "ablt": "Творительный",
            "loct": "Предложный"
        }
        number_options_display = {
            "sing": "Единственное число",
            "plur": "Множественное число"
        }
    else:
        t = {
            'welcome': 'Welcome to the Russian Noun Cases Drill',
            'forward_drill': 'Forward Drill',
            'backward_drill': 'Backward Drill',
            'select_cases': 'Select Cases:',
            'select_number': 'Select Number:',
            'convert': 'Convert the noun',
            'into': 'into its',
            'form': 'form',
            'your_answer': 'Your Answer',
            'submit': 'Submit',
            'next': 'Next',
            'back_home': 'Back to Home',
            'intro_text': 'Practice Russian noun declensions interactively!'
        }
        case_options_display = CASE_OPTIONS
        number_options_display = NUMBER_OPTIONS
    return t, case_options_display, number_options_display

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

    # Retrieve chosen language from session (default to English)
    lang = session.get('lang', 'en')
    t, case_options_display, number_options_display = get_translations(lang)

    # Get training options from the form (if present)
    selected_cases = request.form.getlist("cases")
    selected_numbers = request.form.getlist("numbers")

    # Set defaults if nothing selected.
    if not selected_cases:
        selected_cases = ["gent"]  # default to Genitive
    if not selected_numbers:
        selected_numbers = ["sing"]  # default to Singular

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
                feedback = "Correct!" if lang == 'en' else "Правильно!"
            else:
                feedback = (f"Incorrect. The correct answer is {correct_answer}."
                            if lang == 'en' else
                            f"Неверно. Правильный ответ: {correct_answer}.")
            # Generate a new question after checking.
            question, current_case, current_number, correct_answer = generate_question(selected_cases, selected_numbers)
        elif action == "next":
            # Generate a new question without validating an answer.
            question, current_case, current_number, correct_answer = generate_question(selected_cases, selected_numbers)
    else:
        # On initial GET, use defaults.
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
        case_options=case_options_display,
        number_options=number_options_display,
        t=t,
        lang=lang
    )

# ---------------------------
# New Backward Drill Route
# ---------------------------
@app.route('/backward_drill', methods=['GET', 'POST'])
def backward_drill():
    feedback = None
    lang = session.get('lang', 'en')
    t, case_options_display, number_options_display = get_translations(lang)
    # Use all available case and number keys.
    possible_cases = list(CASE_OPTIONS.keys())
    possible_numbers = list(NUMBER_OPTIONS.keys())

    # Generate a backward drill question:
    noun = random.choice(TOP_NOUNS)
    correct_case = random.choice(possible_cases)
    correct_number = random.choice(possible_numbers)
    p = morph.parse(noun)[0]
    inflected_obj = p.inflect({correct_case, correct_number})
    inflected_word = inflected_obj.word if inflected_obj else "Error"

    if request.method == 'POST':
        action = request.form.get("action")
        if action == "submit":
            user_case = request.form.get("selected_case")
            user_number = request.form.get("selected_number")
            # Retrieve the correct answers from hidden fields.
            hidden_case = request.form.get("current_case")
            hidden_number = request.form.get("current_number")
            if user_case == hidden_case and user_number == hidden_number:
                feedback = "Correct!" if lang == 'en' else "Правильно!"
            else:
                feedback = (f"Incorrect. The correct answer is {hidden_case} and {hidden_number}."
                            if lang == 'en'
                            else f"Неверно. Правильный ответ: {hidden_case} и {hidden_number}.")
            # Generate a new question after submission.
            noun = random.choice(TOP_NOUNS)
            correct_case = random.choice(possible_cases)
            correct_number = random.choice(possible_numbers)
            p = morph.parse(noun)[0]
            inflected_obj = p.inflect({correct_case, correct_number})
            inflected_word = inflected_obj.word if inflected_obj else "Error"

    return render_template("backward_drill.html",
                           inflected_word=inflected_word,
                           feedback=feedback,
                           current_case=correct_case,
                           current_number=correct_number,
                           possible_cases=case_options_display,
                           possible_numbers=number_options_display,
                           t=t,
                           lang=lang)

@app.route('/')
def home():
    lang = session.get('lang', 'en')
    t, _, _ = get_translations(lang)
    return render_template('home.html', t=t, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
