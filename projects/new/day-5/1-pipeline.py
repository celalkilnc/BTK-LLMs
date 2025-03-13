from transformers import pipeline

classifier = pipeline('sentiment-analysis')

texts = [
    "I have' been HF Course my whole life",
    "I hate this so much!"
]

results = classifier(texts)

for text, result in zip(texts,results):
    print(f"{text} : {result} . Score {result["score"]}")
