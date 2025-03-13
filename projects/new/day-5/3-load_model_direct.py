from transformers import AutoTokenizer, AutoModelForAudioClassification
import torch

model_name = "facebook/barte-large-mnli"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)

hypothesis = "A man is playing the guitar."
statements = [
    "A person is playing a musical instrument.",  # Entailment
    "A woman is dancing.",  # Contradiction
    "The weather is nice today.",  # Neutral
]

# Girdiyi ayarla
for statement in statements:
    inputs = tokenizer(
        statement,
        hypothesis,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )

    # Çıktı al
    with torch.no_grad():
        logits = model(**inputs).logits

        # Tahmin sınıfını al
        predicted_class_id = logits.argmax().item()

        # Sınıfın etiketini al
        label_mapping = ['çelişki','nötr','gereklilik']

        predicted_label = label_mapping[predicted_class_id]
