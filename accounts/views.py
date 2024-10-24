from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.http import JsonResponse
import os
import google.generativeai as genai


def complexity_bot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = find_complexity(message)
        print(f"Received message for complexity analysis: {message}")
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'accounts/codeeditor.html')

def find_complexity(message):
    # Example for using a different API key or method
    genai.configure(api_key="AIzaSyAjr1v-NGJb8qix3HXgQABxQViwMgdSCkI")

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 50,
        "max_output_tokens": 4096,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

    chat_session = model.start_chat(history=[])
    
    res = chat_session.send_message(f"find the time complexity of the following code: {message} return only the time complexity.nothing else")
    print(res)
    return res.text

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        print(f"Received message: {message}") 
        return JsonResponse({'message':message,'response':response})
    return render(request,'accounts/codeeditor.html')

def ask_openai(message):
    genai.configure(api_key="AIzaSyDUX756PqIuqKJpftGreqSHkzYL9pweNAk")

    # Create the model
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )

    chat_session = model.start_chat(
    history=[
    ]
    )
    
    res = chat_session.send_message(f"{message}reduce the time complexity of this code using any method.")
    print(res)
    return res.text



# Custom login view to handle login form rendering
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))  # Redirect to a protected page after login
            else:
                form.add_error(None, "Invalid credentials")
        else:
            form.add_error(None, "Invalid credentials")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Custom logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))  # Redirect to login page after logout

def homepage_view(request):
    return render(request,'base.html')

