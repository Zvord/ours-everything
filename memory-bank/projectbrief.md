# Application Summary: Russian Noun Cases Drill

**Overview:**
A web-based drill application built with Flask for practicing Russian noun declensions. It uses pymorphy3 for morphological analysis and supports bilingual UI (English and Russian). The application features three types of exercises:

1. **Forward Drill:**
   - **Purpose:** Present a noun in the nominative form; the user must provide the correct inflected form (e.g., Genitive Singular).
   - **Behavior:** When the user clicks "Submit," the answer is validated and feedback is provided, but the question remains unchanged so the user can review their input. Clicking "Next" generates a new question.

2. **Backward Drill:**
   - **Purpose:** Display an inflected form of a noun; the user must select the correct grammatical case and number from drop-down menus.
   - **Behavior:** On "Submit," the application validates the drop-down selections while preserving the current question and user’s selections. "Next" generates a new question.

3. **Insert Drill:**
   - **Purpose:** Present a sentence (grouped by case) with a missing word. A hint is provided by showing the normal form (lemma) of the missing word.
   - **Behavior:** When the user submits an answer, the application validates it without generating a new question, allowing the user to review their input. "Next" generates a new exercise.
