from agents.teacher import TeacherAgent
from agents.quiz_generator import QuizGeneratorAgent
from agents.wiki_searcher import WikiSearcherAgent
from agents.normalizer import NormalizerAgent
from tools.validator import Validator
import time


class Coordinator:

    def __init__(self, client, model):
        self.teacher = TeacherAgent(client, model)
        self.quiz_generator = QuizGeneratorAgent(client, model)
        self.wiki_searcher = WikiSearcherAgent(client, model)
        self.normalizer = NormalizerAgent(client, model)
        self.history = []

    def coordinate(self, domanda: str):
        titolo = self.normalizer.normalize_content(domanda)
        print("normalizer ok")
        time.sleep(10)
        
        spiegazione = self.teacher.teach(titolo, domanda)
        print("teach ready")
        time.sleep(10)

        wiki = self.wiki_searcher.search(domanda, titolo)
        print("wiki ready")
        time.sleep(10)

        print("Starting validation...")
        validator = Validator(spiegazione)
        validator.validate_length()
        validator.validate_structure()
        validation_result = validator.validate_ollama(wiki)
        print("validation result:", validation_result)
        
        self.teacher.submit(titolo, spiegazione)
        self.wiki_searcher.submit(titolo, wiki)

        time.sleep(10)
        quiz = self.quiz_generator.generate_quiz(titolo)

        print("quiz generator ok")
        time.sleep(10)
        
        risultato = {"titolo": titolo, "spiegazione": spiegazione, "quiz": quiz, "wiki": wiki}
        self.history.append(risultato)
        return risultato