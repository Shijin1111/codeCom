from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

from .models import Note
from .forms import NoteForm

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

@login_required
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
    
    res = chat_session.send_message(f"{message}Do this with less time complexity")
    print(res)
    return res.text



# Custom login view to handle login form rendering
# def login_view(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)

#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))  # Redirect to a protected page after login
#             else:
#                 form.add_error(None, "Invalid credentials")
#         else:
#             form.add_error(None, "Invalid credentials")

#     else:
#         form = AuthenticationForm()

#     return render(request, 'accounts/login.html', {'form': form})

# Custom logout view
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('login'))  # Redirect to login page after logout

def homepage_view(request):
    return render(request,'base.html')


@login_required
def blog(request):
    notes = Note.objects.all()
    return render(request, 'accounts/blog.html', {'notes': notes})

def note_detail(request, id):
    note = get_object_or_404(Note, id=id)
    return render(request, 'accounts/note_detail.html', {'note': note})

# def add_note(request):
#     if request.method == 'POST':
#         form = NoteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('blog')
#     else:
#         form = NoteForm()
#     return render(request, 'accounts/add_note.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import NoteForm, SubheadingFormSet

def add_note(request):
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        subheading_formset = SubheadingFormSet(request.POST)
        
        if note_form.is_valid() and subheading_formset.is_valid():
            note = note_form.save()
            subheadings = subheading_formset.save(commit=False)
            for subheading in subheadings:
                subheading.note = note
                subheading.save()
            return redirect('blog')
    else:
        note_form = NoteForm()
        subheading_formset = SubheadingFormSet()
    
    return render(request, 'accounts/add_note.html', {
        'note_form': note_form,
        'subheading_formset': subheading_formset
    })

from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/sign_up.html', {'form': form})


import subprocess
from django.shortcuts import render,get_object_or_404
from .forms import PythonCodeForm
from .models import CodeExecution
from django.utils.html import escape

def execute_python_code(code, input_data, timeout=5):
    try:
        process = subprocess.Popen(
            ['python', '-c', code],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            universal_newlines=True,
            errors='ignore'
        )
        output, error = process.communicate(input=input_data, timeout=timeout)

        if process.returncode == 0:
            return output
        else:
            return error
    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return str(e)

def save_code_execution(code, input_data, output):
    CodeExecution.objects.create(code=code, input_data=input_data, output=output)



def compile_and_execute(request, problem_id):
    output = None

    # Fetch the problem using the provided problem_id
    problem = get_object_or_404(Problem, id=problem_id)

    # Set default code
    code = "print('Hello, World!')"  # Default code example
    input_data = ""
    if request.method == "POST":
        # Get the code from the form submission
        code = request.POST.get("code", code)  # Retrieve code from POST, fallback to default
        input_data = request.POST.get("input_data", "")  # Optional input data if required

        # Execute the code
        try:
            output = execute_python_code(code, input_data)  # Call your execute function here
            save_code_execution(code, input_data, output)  # Log the execution result if needed
        except subprocess.TimeoutExpired:
            output = 'Execution timed out.'
        except Exception as e:
            output = str(e)

    # Pass the code along with output, input_data, and problem to the template
    return render(request, 'accounts/problems/compile.html', {
        'output': output,
        'code': escape(code),  # Pass code back to template to retain it
        'input_data': escape(input_data),
        'problem': problem
    })
    
from .models import Problem
@login_required
def problem_list(request):
    problems = Problem.objects.all()  # Retrieve all Problem objects
    return render(request, 'accounts/problems/problem_list.html', {'problems': problems})  # Pass them to the template