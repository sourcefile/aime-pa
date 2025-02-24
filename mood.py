from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self, thresholdvalue: float):
        print("Preparing Sentiment Analysis module...")
        self.classifier = pipeline("text-classification",
                                    model='bhadresh-savani/distilbert-base-uncased-emotion',
                                    top_k=None,
                                    device='cpu')
        self.thresholdvalue = thresholdvalue
        print("Sentiment Analysis module initialized.")

    def sentiment(self, input):
        scores = self.classifier(input)[0]
        mood = scores[0]
        if mood['score'] <= self.thresholdvalue: return 'neutral'
        else: return mood['label']