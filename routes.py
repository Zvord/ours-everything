"""
Route handlers for the Russian Noun Cases Drill application.
"""

import random
from flask import render_template, request, session, redirect, url_for

from models import DrillData
from utils import get_translations, generate_question, get_feedback

# Initialize drill data
drill_data = DrillData()

def init_routes(app, morph):
    """
    Initialize all route handlers for the application.

    Args:
        app: The Flask application instance
        morph: The pymorphy3 MorphAnalyzer instance
    """

    @app.route('/set_language/<lang>')
    def set_language(lang):
        """Set the language for the application."""
        if lang in ['en', 'ru']:
            session['lang'] = lang
        return redirect(request.referrer or url_for('home'))

    @app.route('/')
    def home():
        """Render the home page."""
        lang = session.get('lang', 'en')
        t, _, _ = get_translations(lang)
        return render_template('home.html', t=t, lang=lang)

    @app.route('/forward_drill', methods=['GET', 'POST'])
    def forward_drill():
        """Handle the forward drill route."""
        feedback = None

        # Retrieve chosen language from session (default to English)
        lang = session.get('lang', 'en')
        t, case_options_display, number_options_display = get_translations(lang)

        # Get training options from the form (if present)
        selected_cases = request.form.getlist("cases")
        selected_numbers = request.form.getlist("numbers")

        # Set defaults if nothing selected
        if not selected_cases:
            selected_cases = ["gent"]  # default to Genitive
        if not selected_numbers:
            selected_numbers = ["sing"]  # default to Singular

        if request.method == 'POST':
            action = request.form.get("action")
            if action == "submit":
                # Validate the user's answer and retain it
                submitted_answer = request.form.get('answer')
                correct_answer = request.form.get('correct_answer')
                question = request.form.get('question')
                current_case = request.form.get('current_case')
                current_number = request.form.get('current_number')
                feedback = get_feedback(submitted_answer, correct_answer, lang)
            elif action == "next":
                # Generate a new question without validating an answer
                question, current_case, current_number, correct_answer = generate_question(
                    morph, selected_cases, selected_numbers, drill_data=drill_data
                )
        else:
            # On initial GET, use defaults
            selected_cases = ["gent"]
            selected_numbers = ["sing"]
            question, current_case, current_number, correct_answer = generate_question(
                morph, selected_cases, selected_numbers, drill_data=drill_data
            )

        return render_template(
            "forward_drill.html",
            question=question,
            correct_answer=correct_answer,
            feedback=feedback,
            submitted_answer=submitted_answer if request.method == 'POST' and request.form.get("action") == "submit" else "",
            selected_cases=selected_cases,
            selected_numbers=selected_numbers,
            current_case=current_case,
            current_number=current_number,
            case_options=drill_data.get_case_options(lang),
            number_options=drill_data.get_number_options(lang),
            t=t,
            lang=lang
        )

    @app.route('/backward_drill', methods=['GET', 'POST'])
    def backward_drill():
        """Handle the backward drill route."""
        feedback = None
        submitted_answer = ""
        lang = session.get('lang', 'en')
        t, case_options_display, number_options_display = get_translations(lang)

        # Use all available case and number keys for generating question
        case_keys = list(drill_data.case_options.keys())
        number_keys = list(drill_data.number_options.keys())

        # Generate a backward drill question
        noun = drill_data.get_random_noun()
        correct_case = random.choice(case_keys)
        correct_number = random.choice(number_keys)
        p = morph.parse(noun)[0]
        inflected_obj = p.inflect({correct_case, correct_number})
        inflected_word = inflected_obj.word if inflected_obj else "Error"

        if request.method == 'POST':
            action = request.form.get("action")
            if action == "submit":
                user_case = str(request.form.get("selected_case"))
                user_number = str(request.form.get("selected_number"))
                # Retrieve the correct answers from hidden fields and convert to string
                hidden_case = str(request.form.get("current_case"))
                hidden_number = str(request.form.get("current_number"))

                case_options = drill_data.get_case_options(lang)
                number_options = drill_data.get_number_options(lang)
                if user_case == hidden_case and user_number == hidden_number:
                    feedback = "Correct!" if lang == 'en' else "Правильно!"
                else:
                    feedback = (f"Incorrect. The correct answer is {case_options.get(hidden_case, hidden_case)} / {number_options.get(hidden_number, hidden_number)}."
                                if lang == 'en'
                                else f"Неверно. Правильный ответ: {case_options.get(hidden_case, hidden_case)} / {number_options.get(hidden_number, hidden_number)}.")
                    submitted_answer = f"{case_options.get(user_case, user_case)} / {number_options.get(user_number, user_number)}"

        return render_template(
            "backward_drill.html",
            inflected_word=inflected_word,
            feedback=feedback,
            submitted_answer=submitted_answer if request.method == 'POST' and request.form.get("action") == "submit" else "",
            current_case=correct_case,
            current_number=correct_number,
            possible_cases=drill_data.get_case_options(lang),
            possible_numbers=drill_data.get_number_options(lang),
            t=t,
            lang=lang
        )

    @app.route('/insert_drill', methods=['GET', 'POST'])
    def insert_drill():
        """Handle the insert drill route."""
        feedback = None
        lang = session.get('lang', 'en')
        t, _, _ = get_translations(lang)
        submitted_answer = ""

        # On GET or if "next" button is pressed, generate a new question
        if request.method == 'GET' or request.form.get("action") == "next":
            chosen_case, sentence_data = drill_data.get_random_sentence()

            if not sentence_data:
                # Fallback if no sentences are available
                return render_template(
                    "insert_drill.html",
                    blank_sentence="No sentences available.",
                    normal_form="",
                    feedback=None,
                    correct_word="",
                    t=t,
                    lang=lang
                )

            full_sentence = sentence_data["sentence"]
            word_index = sentence_data["word_index"]
            words = full_sentence.split()

            if word_index - 1 < len(words):
                missing_word = words[word_index - 1]
            else:
                missing_word = ""

            # Remove punctuation from missing word
            stripped_word = missing_word.strip(".,!?")
            if stripped_word:
                normal_form = morph.parse(stripped_word)[0].normal_form
            else:
                normal_form = ""

            # Replace the target word with a blank
            words[word_index - 1] = "_____"
            blank_sentence = " ".join(words)

            # Store the correct answer
            correct_word = stripped_word

        # If the user submitted an answer, use the hidden fields to check
        elif request.method == 'POST' and request.form.get("action") == "submit":
            user_answer = request.form.get("answer")
            submitted_answer = user_answer
            correct_word = request.form.get("correct_word")
            blank_sentence = request.form.get("blank_sentence")
            normal_form = request.form.get("normal_form")

            feedback = get_feedback(user_answer, correct_word, lang)

        return render_template(
            "insert_drill.html",
            blank_sentence=blank_sentence,
            normal_form=normal_form,
            feedback=feedback,
            submitted_answer=submitted_answer if request.method == 'POST' and request.form.get("action") == "submit" else "",
            correct_word=correct_word,
            t=t,
            lang=lang
        )
