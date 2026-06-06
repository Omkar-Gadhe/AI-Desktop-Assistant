# services/nlp_service.py
import spacy
from spacy.matcher import PhraseMatcher

class NLPService:
    def __init__(self):
        # Heavy resources start uninitialized as None
        self._nlp = None
        self._matcher = None

    def initialize(self, app_registry: list):
        """Explicit initialization method. 
        Perfect for a future GUI loading screen or startup worker.
        """
        if self._nlp is not None:
            return  # Already loaded, safeguard against double loading

        # Load the heavy linguistic model into memory
        self._nlp = spacy.load("en_core_web_sm")
        
        # Configure and warm up the phrase matcher
        self._matcher = PhraseMatcher(self._nlp.vocab, attr="LOWER")
        app_patterns = [self._nlp.make_doc(app) for app in app_registry]
        self._matcher.add("TARGET_APPS", app_patterns)

    @property
    def nlp(self):
        if self._nlp is None:
            raise RuntimeError("NLPService used before initialize() was called.")
        return self._nlp

    @property
    def matcher(self):
        if self._matcher is None:
            raise RuntimeError("NLPService used before initialize() was called.")
        return self._matcher

# Instantiate a single global instance of the service container
nlp_service = NLPService()