from django.shortcuts import render
from transformers import BartForConditionalGeneration, BartTokenizer, pipeline
import torch
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

model_name = "facebook/bart-large"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

sentiment_analysis = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_emotion(text):
    result = sentiment_analysis(text)
    print(result)
    return result[0]

def generate_text(prompt):
    story_prompt = f'Help write a creative story that continues from {prompt}'
    inputs = tokenizer.encode(story_prompt, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=100,
        min_length=30,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        no_repeat_ngram_size=2
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return f'{prompt}, {generated_text[len(story_prompt):]}'

def give_feedback(emotion):
    if emotion['label'] == 'POSITIVE':
        return "Your writing has a positive tone! Keep it up!"
    elif emotion['label'] == 'NEGATIVE':
        return "It seems your writing reflects some negative emotions. Want to explore why?"
    else:
        return "Your writing is quite neutral. Maybe dive deeper into your feelings?"

@csrf_exempt
@require_POST
def generate_poem_line(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_line = data.get('line', '')

        poetic_prompt = f"Complete the following poetic line with rhyming and rhythm: '{user_line}'."

        inputs = tokenizer.encode(poetic_prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=100,
            min_length=30,
            num_return_sequences=1,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
            no_repeat_ngram_size=2
        )

        ai_line = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return JsonResponse({'ai_line': ai_line[len(poetic_prompt)-1:]})

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
