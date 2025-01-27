from flask import Flask, request, render_template
from model import SpellCheckerModule


app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST', 'GET'])
def spell():
    if request.method == 'POST':
        text = request.form['text']
        if not text.strip():
            return render_template('index.html', error="No text provided", corrected_text=None, corrected_grammar=None)

        corrected_text = spell_checker_module.correct_spell(text)  # No SymSpell here
        corrected_grammar = spell_checker_module.correct_grammar(corrected_text)

        return render_template(
            'index.html',
            corrected_text=corrected_text,
            corrected_grammar=corrected_grammar
        )
    return render_template('index.html', corrected_text=None, corrected_grammar=None)


@app.route('/grammar', methods=['POST', 'GET'])
def grammar():
    if request.method == 'POST':
        file = request.files['file']
        if not file or file.filename == '':
            return render_template('index.html', error="No file uploaded", corrected_file_text=None, corrected_file_grammar=None, mistakes_count=None)
        readable_file = file.read().decode('utf-8', errors='ignore')
        corrected_file_text = spell_checker_module.correct_spell(readable_file)
        corrected_file_grammar, mistakes_count = spell_checker_module.correct_grammar(corrected_file_text)
        return render_template(
            'index.html',
            corrected_file_text=corrected_file_text,
            corrected_file_grammar=corrected_file_grammar,
            mistakes_count=mistakes_count
        )
    return render_template('index.html', corrected_file_text=None, corrected_file_grammar=None, mistakes_count=None)

if __name__ == "__main__":
    app.run()
