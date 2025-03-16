"""
Utility functions for the Russian Noun Cases Drill application.
"""

from typing import Dict, Tuple, Any

def get_translations(lang: str) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
    """
    Return translation dictionaries based on the language.

    Args:
        lang: The language code ('en' or 'ru')

    Returns:
        A tuple containing:
        - t: Dictionary of UI text translations
        - case_options_display: Dictionary of case names
        - number_options_display: Dictionary of number names
    """
    if lang == 'ru':
        t = {
            'welcome': 'Добро пожаловать в тренировку склонения русских существительных',
            'forward_drill': 'Тренировка: Склонение существительных',
            'backward_drill': 'Тренировка: определение падежа и числа',
            'select_cases': 'Выберите падежи:',
            'select_number': 'Выберите число:',
            'select_case_and_number': 'Выберите падеж и число:',
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
            'select_case_and_number': 'Select Case and Number:',
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
        case_options_display = {
            "nomn": "Nominative",
            "gent": "Genitive",
            "datv": "Dative",
            "accs": "Accusative",
            "ablt": "Instrumental",
            "loct": "Prepositional"
        }
        number_options_display = {
            "sing": "Singular",
            "plur": "Plural"
        }
    return t, case_options_display, number_options_display

def generate_question(morph, selected_cases, selected_numbers, noun=None, drill_data=None):
    """
    Generate a question for the forward drill.

    Args:
        morph: The pymorphy3 MorphAnalyzer instance
        selected_cases: List of selected grammatical cases
        selected_numbers: List of selected grammatical numbers
        noun: Optional specific noun to use (if None, a random one is selected)
        drill_data: Optional DrillData instance to use for getting a random noun

    Returns:
        A tuple containing (noun, case, number, inflected_form)
    """
    if noun is None and drill_data is not None:
        noun = drill_data.get_random_noun()
    elif noun is None:
        # Fallback to a random noun from a hardcoded list
        import random
        TOP_NOUNS = [
            "слово", "человек", "время", "дело", "жизнь",
            "день", "рука", "работа", "место", "право"
        ]
        noun = random.choice(TOP_NOUNS)

    # Randomly select a case and a number from the chosen options
    import random
    case = random.choice(selected_cases) if selected_cases else "gent"
    number = random.choice(selected_numbers) if selected_numbers else "sing"

    p = morph.parse(noun)[0]
    # Attempt to inflect the noun to the chosen case and number
    inflected_obj = p.inflect({case, number})
    inflected = inflected_obj.word if inflected_obj else "Error"

    return noun, case, number, inflected

def get_feedback(user_input, correct_answer, lang):
    """
    Generate feedback based on the user's answer.

    Args:
        user_input: The user's answer
        correct_answer: The correct answer
        lang: The language code ('en' or 'ru')

    Returns:
        Feedback message
    """
    if user_input.strip().lower() == correct_answer.strip().lower():
        return "Correct!" if lang == 'en' else "Правильно!"
    else:
        return (f"Incorrect. The correct answer is {correct_answer}."
                if lang == 'en' else
                f"Неверно. Правильный ответ: {correct_answer}.")
