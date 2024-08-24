from django.shortcuts import render
from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
import torch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

# Create your views here.
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_emotion(text):
    result = sentiment_analysis(text)
    print(result)
    return result[0]


def generate_text(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    attention_mask = torch.ones(inputs.shape, dtype=torch.long)

    outputs = model.generate(
        inputs, 
        attention_mask=attention_mask,
        max_length=100, 
        min_length=30,
        num_return_sequences=1,
        pad_token_id = tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        no_repeat_ngram_size=2
    )    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def give_feedback(emotion):
    if emotion['label'] == 'POSITIVE':
        return "Your writing has a positive tone! Keep it up!"
    elif emotion['label'] == 'NEGATIVE':
        return "It seems your writing reflects some negative emotions. Want to explore why?"
    else:
        return "Your writing is quite neutral. Maybe dive deeper into your feelings?"

@csrf_exempt
@require_POST
def handle_request(request):
    data = json.loads(request.body)
    user_input = data.get('user_input', '')
    emotion = analyze_emotion(user_input)
    feedback = give_feedback(emotion)
    continuation = generate_text(user_input)

    return JsonResponse({
        'feedback': feedback,
        'continuation': continuation
    })

def index(request):
    if request.method == 'POST':
        user_input = request.POST['user_input']
        emotion = analyze_emotion(user_input)
        feedback = give_feedback(emotion)
        continuation = generate_text(user_input)
        return render(request, 'writing/index.html', {
            'user_input': user_input,
            'feedback': feedback,
            'continuation': continuation,
        })
    return render(request, 'writing/index.html')

