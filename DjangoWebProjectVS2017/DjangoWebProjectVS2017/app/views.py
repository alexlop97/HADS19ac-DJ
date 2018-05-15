"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index_category(request, category):
    correct_question_list = []

    questions_of_category = Question.objects.filter(category=category)
    if not request.user.is_authenticated:
        for c_question in questions_of_category:
            choice_list = Choice.objects.filter(question = c_question)
            choice_count = 0
            for c_choice in choice_list:
                choice_count += 1
            if choice_count >= 2 and choice_count <= 4:
                correct_question_list.append(c_question)
    
    else:
        correct_question_list = questions_of_category

    latest_question_list = Question.objects.order_by('-pub_date')
    correct_question_category_list = []

    if not request.user.is_authenticated:
        for c_question in latest_question_list:
            choice_list = Choice.objects.filter(question = c_question)
            choice_count = 0
            for c_choice in choice_list:
                choice_count += 1
            if choice_count >= 2 and choice_count <= 4:
                correct_question_category_list.append(c_question)
    
    else:
        correct_question_category_list = latest_question_list

    category_list = []
    for c_q in correct_question_category_list:
        if c_q.category not in category_list:
            category_list.append(c_q.category)

    template = loader.get_template('polls/index.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': correct_question_list,
                'category_list' : category_list
              }
    return render(request, 'polls/index.html', context)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    correct_question_list = []

    if not request.user.is_authenticated:
        for c_question in latest_question_list:
            choice_list = Choice.objects.filter(question = c_question)
            choice_count = 0
            for c_choice in choice_list:
                choice_count += 1
            if choice_count >= 2 and choice_count <= 4:
                correct_question_list.append(c_question)
    
    else:
        correct_question_list = latest_question_list


    category_list = []
    for c_q in correct_question_list:
        if c_q.category not in category_list:
            category_list.append(c_q.category)

    template = loader.get_template('polls/index.html')
    context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': correct_question_list,
                'category_list' : category_list
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Question, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id, choice_id):
    question = get_object_or_404(Question, pk=question_id)

    choices = question.choice_set.order_by('id')
    counter = 1
    for choice in choices:
        if choice.id == int(choice_id):
            selected_pos = counter
        counter += 1

    if selected_pos == question.correct_choice:
        mes = 'Correcta!'
    else:
        mes = 'Incorrecta!'

    return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question, 'resultado' : mes})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id, selected_choice.id)))

def question_new(request):
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = QuestionForm()
        return render(request, 'polls/question_new.html', {'form': form})

def choice_add(request, question_id):
        question = Question.objects.get(id = question_id)

        choice_list = Choice.objects.filter(question = question)
        choice_count = 0
        for c_choice in choice_list:
                choice_count += 1
        if choice_count < 4:
            if request.method =='POST':
                form = ChoiceForm(request.POST)
                if form.is_valid():
                    choice = form.save(commit = False)
                    choice.question = question
                    choice.vote = 0
                    choice.save()         
                    #form.save()
            else: 
                form = ChoiceForm()
            #return render_to_response ('choice_new.html', {'form': form, 'poll_id': poll_id,}, context_instance = RequestContext(request),)
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.question_text,'form': form})

        else:
            form = ChoiceForm()
            form.fields['choice_text'].widget.attrs['readonly'] = True

            return render(request, 'polls/choice_new.html', {
            'title':'Pregunta:'+ question.question_text,
            'form' : form,
            'message': "ERROR: Número máximo de opciones alcanzado.",
        })

def chart(request, question_id):
    q=Question.objects.get(id = question_id)
    qs = Choice.objects.filter(question=q)
    dates = [obj.choice_text for obj in qs]
    counts = [obj.votes for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)