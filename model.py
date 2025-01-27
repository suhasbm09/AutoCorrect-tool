from symspellpy import SymSpell
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class SpellCheckerModule:
    def __init__(self):
        # Initialize SymSpell for spell correction
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2)
        self.sym_spell.load_dictionary("./frequency_dictionary_en.txt", term_index=0, count_index=1)

        # Initialize Hugging Face T5 model for grammar correction
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

    def correct_spell(self, text):
        """
        Correct spelling errors using SymSpell.
        """
        suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
        return suggestions[0].term if suggestions else text

    def preprocess_text(self, text):
        """
        Preprocess text for grammar correction.
        """
        sentences = text.split('. ')
        sentences = [sentence.capitalize().strip() for sentence in sentences if sentence]
        return '. '.join(sentences) + '.'

    def correct_grammar(self, text):
        """
        Correct grammatical errors using T5-small.
        """
        preprocessed_text = self.preprocess_text(text)
        inputs = self.tokenizer("gec: " + preprocessed_text, return_tensors="pt", truncation=True)
        outputs = self.model.generate(
            inputs["input_ids"],
            max_length=512,
            num_beams=5,
            early_stopping=True
        )
        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if corrected_text.startswith("gec: "):
            corrected_text = corrected_text[len("gec: "):].strip()
            
        return corrected_text
