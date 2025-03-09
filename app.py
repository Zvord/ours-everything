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
            'intro_text': 'Практикуйтесь в склонении существительных на русском языке!',
            'insert_drill': 'Вставьте слово в пропуск',
            'insert_instruction': 'Вставьте недостающее слово в предложение ниже:',
            'insert_hint': '(Подсказка: начальная форма недостающего слова —'
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
            'intro_text': 'Practice Russian noun declensions interactively!',
            'insert_drill': 'Insert Word Drill: Fill in the gap',
            'insert_instruction': 'Fill in the missing word in the sentence below:',
            'insert_hint': '(Hint: The normal form of the missing word is'
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
        case_options=get_translations(lang)[1],
        number_options=get_translations(lang)[2],
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

# ---------------------------
# New Insert Word Drill Route
# ---------------------------
# Data for insert word drill: sentences grouped by case.
INSERT_SENTENCES = {
    "предложный": [
       {"sentence": "Этот студент учится в университете.", "word_index": 5},
       {"sentence": "Мой брат работает на заводе.", "word_index": 5},
       {"sentence": "Мы покупаем продукты в магазине.", "word_index": 5},
       {"sentence": "Наша семья любит гулять в парке.", "word_index": 6},
       {"sentence": "Цветы стоят на подоконнике.", "word_index": 4},
       {"sentence": "Где ваши книги? Они на полке.", "word_index": 6},
       {"sentence": "Преподаватель говорит об экзамене.", "word_index": 4},
       {"sentence": "Мой брат мечтает об автомобиле.", "word_index": 5},
       {"sentence": "В газете я прочитал статью о России.", "word_index": 2},
       {"sentence": "Книги стоят в шкафу.", "word_index": 4}
    ],
    "винительный": [
       {"sentence": "Я читаю книгу.", "word_index": 3},
       {"sentence": "Мой брат часто слушает музыку.", "word_index": 5},
       {"sentence": "Студент пишет упражнение.", "word_index": 3},
       {"sentence": "Мой друг хорошо знает химию.", "word_index": 5},
       {"sentence": "Каждый день мы учим слова.", "word_index": 5},
       {"sentence": "Студенты изучают грамматику.", "word_index": 3},
       {"sentence": "Борис переводит статью.", "word_index": 3},
       {"sentence": "Преподаватель проверяет тетрадь.", "word_index": 3},
       {"sentence": "Утром я делаю зарядку.", "word_index": 4}
    ],
    "дательный": [
       {"sentence": "Я всегда помогаю маме.", "word_index": 4},
       {"sentence": "Николай часто звонит другу.", "word_index": 4},
       {"sentence": "Студент отвечает преподавателю.", "word_index": 3},
       {"sentence": "Журналист задавал вопросы спортсмену.", "word_index": 4},
       {"sentence": "Бабушка часто читает книги внучке.", "word_index": 5},
       {"sentence": "Отец подарил велосипед сыну.", "word_index": 4},
       {"sentence": "Я послал открытку подруге.", "word_index": 4},
       {"sentence": "Учитель объясняет тему ученику.", "word_index": 4},
       {"sentence": "Николай послал телеграмму бабушке.", "word_index": 4},
       {"sentence": "Они предложили новый проект директору.", "word_index": 5}
    ],
    "творительный": [
       {"sentence": "Наша семья любит гулять с собакой.", "word_index": 6},
       {"sentence": "Брат пошёл в кино с сестрой.", "word_index": 6},
       {"sentence": "Кошка прячется за коробкой.", "word_index": 4},
       {"sentence": "Они любят кофе с сахаром.", "word_index": 5},
       {"sentence": "Его брат работает учителем.", "word_index": 4},
       {"sentence": "Дима пошёл в театр с другом.", "word_index": 6},
       {"sentence": "Мама дала мне чай с молоком.", "word_index": 6},
       {"sentence": "В кино я познакомился с девушкой.", "word_index": 6},
       {"sentence": "Она увлекается спортом.", "word_index": 3},
       {"sentence": "Она ходит на тренировку с подругой.", "word_index": 6},
       {"sentence": "Мой дядя работает продавцом.", "word_index": 4}
    ],
    "родительный": [
       {"sentence": "На собрании выступил директор школы.", "word_index": 5},
       {"sentence": "Я живу далеко от школы.", "word_index": 5},
       {"sentence": "Это компьютер моего брата.", "word_index": 4},
       {"sentence": "В нашем городе нет библиотеки.", "word_index": 5},
       {"sentence": "Завтра у нас не будет урока.", "word_index": 6},
       {"sentence": "Сейчас был урок литературы.", "word_index": 4},
       {"sentence": "У Сергея есть собака.", "word_index": 2},
       {"sentence": "У этих людей нет работы.", "word_index": 5}
    ]
}

@app.route('/insert_drill', methods=['GET', 'POST'])
def insert_drill():
    feedback = None
    lang = session.get('lang', 'en')
    t, _, _ = get_translations(lang)

    # On GET or if "next" button is pressed, generate a new question.
    if request.method == 'GET' or request.form.get("action") == "next":
        chosen_case = random.choice(list(INSERT_SENTENCES.keys()))
        sentence_data = random.choice(INSERT_SENTENCES[chosen_case])
        full_sentence = sentence_data["sentence"]
        word_index = sentence_data["word_index"]
        words = full_sentence.split()
        if word_index - 1 < len(words):
            missing_word = words[word_index - 1]
        else:
            missing_word = ""
        # Remove punctuation from missing word.
        stripped_word = missing_word.strip(".,!?")
        if stripped_word:
            normal_form = morph.parse(stripped_word)[0].normal_form
        else:
            normal_form = ""
        # Replace the target word with a blank.
        words[word_index - 1] = "_____"
        blank_sentence = " ".join(words)
        # Store the correct answer.
        correct_word = stripped_word
    # If the user submitted an answer, use the hidden fields to check.
    elif request.method == 'POST' and request.form.get("action") == "submit":
        user_answer = request.form.get("answer")
        correct_word = request.form.get("correct_word")
        blank_sentence = request.form.get("blank_sentence")
        normal_form = request.form.get("normal_form")
        if user_answer.strip().lower() == correct_word.strip().lower():
            feedback = "Correct!" if lang == 'en' else "Правильно!"
        else:
            feedback = ("Incorrect.\n Your answer: " + user_answer + "\nThe correct answer is " + correct_word + "."
                        if lang == 'en'
                        else "Неверно.\n Ваш ответ: " + user_answer + "\n Правильный ответ: " + correct_word + ".")

    return render_template("insert_drill.html",
                           blank_sentence=blank_sentence,
                           normal_form=normal_form,
                           feedback=feedback,
                           correct_word=correct_word,
                           t=t,
                           lang=lang)

@app.route('/')
def home():
    lang = session.get('lang', 'en')
    t, _, _ = get_translations(lang)
    return render_template('home.html', t=t, lang=lang)

if __name__ == '__main__':
    app.run(debug=True)
