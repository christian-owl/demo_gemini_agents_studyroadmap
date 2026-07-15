from agents.teacher import TeacherAgent
from agents.quiz_generator import QuizGeneratorAgent
from agents.wiki_searcher import WikiSearcherAgent
from agents.normalizer import NormalizerAgent
import time


class Coordinator:
    history = []

    def __init__(self, client, model):
        self.teacher = TeacherAgent(client, model)
        self.quiz_generator = QuizGeneratorAgent(client, model)
        self.wiki_searcher = WikiSearcherAgent(client, model)
        self.normalizer = NormalizerAgent(client, model)

    def coordinate(self, domanda: str):
        titolo = self.normalizer.normalize_content(domanda)
        print("normalizer ok")
        time.sleep(10)
        spiegazione = self.teacher.teach(titolo, domanda)
        print("teacher ok")
        time.sleep(10)
        quiz = self.quiz_generator.generate_quiz(titolo)
        print("quiz generator ok")
        time.sleep(10)
        wiki = self.wiki_searcher.search(domanda, titolo)
        print("wiki searcher ok")

        risultato = {"titolo": titolo, "spiegazione": spiegazione, "quiz": quiz, "wiki": wiki}
        self.history.append(risultato)
        return risultato