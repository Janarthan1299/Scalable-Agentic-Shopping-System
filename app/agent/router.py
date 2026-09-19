"""Route intents to retrieval domains."""
from app.services.intent_classifier import IntentClassifier


class RequestRouter:
    def __init__(self, classifier: IntentClassifier | None = None) -> None:
        self.classifier = classifier or IntentClassifier()

    def route(self, query: str) -> tuple[str, str]:
        intent = self.classifier.classify(query)
        return intent.domain, intent.intent
