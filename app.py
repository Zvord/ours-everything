from flask import Flask, render_template, request
import pymorphy3

app = Flask(__name__)
morph = pymorphy3.MorphAnalyzer()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/forward_drill', methods=['GET', 'POST'])
def forward_drill():
    if request.method == 'POST':
        user_input = request.form.get('answer')
        correct_answer = request.form.get('correct_answer')
        # Simple string comparison after stripping and lowering case.
        if user_input.strip().lower() == correct_answer.strip().lower():
            feedback = "Correct!"
        else:
            feedback = f"Incorrect. The correct answer is {correct_answer}."
        return render_template(
            'forward_drill.html',
            question=request.form.get('question'),
            correct_answer=correct_answer,
            feedback=feedback
        )
    else:
        # For demonstration, we use the noun "слово"
        noun = "слово"
        # Define target case as Genitive Singular: 'gen' for genitive, 'sing' for singular.
        target_case = {'gent', 'sing'}
        p = morph.parse(noun)[0]
        inflected = p.inflect(target_case).word if p.inflect(target_case) else "Error"
        correct_answer = inflected
        return render_template(
            'forward_drill.html',
            question=noun,
            correct_answer=correct_answer,
            feedback=None
        )

if __name__ == '__main__':
    # Run in debug mode so that changes update automatically.
    app.run(debug=True)
