from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DeleteView
from django.views.generic.detail import View, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy

from .mixins import TicketMixin
from .mixins import QuizMixin
from .forms import TicketForm
from .models import Ticket
from .models import Quiz

from .service import get_quiz
from .service import create_quiz


# Ticket
class TicketsView(TicketMixin, ListView):

    def get(self, request, *args, **kwargs):
        context = {
            'tickets': self.tickets,
            'tickets_count': self.tickets,
        }
        return render(request, 'tickets.html', context)


class TicketView(DetailView):
    model = Ticket
    template_name = 'ticket.html'


class TicketCreateView(CreateView):
    template_name = 'ticket/add_ticket.html'
    form_class = TicketForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        if '_addanother' in self.request.POST:
            return redirect(f'{reverse("tickets")}#ticket_modal')
        else:
            return redirect('tickets')


class TicketUpdateView(UpdateView):
    model = Ticket
    template_name = 'edit_ticket.html'
    fields = ['question', 'answer']
    success_url = reverse_lazy('tickets')


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets')


# Quiz
class QuizzesView(QuizMixin, ListView):

    def get(self, request, *args, **kwargs):
        context = {
            'quizzes': self.quizzes,
            'quizzes_count': self.quizzes,
        }
        return render(request, 'quizzes.html', context)


class QuizView(DetailView):
    model = Quiz
    template_name = 'quiz-result.html'

    def get(self, request, *args, **kwargs):
        quiz = get_quiz(self.kwargs.get("pk", False))
        context = {
            'quiz': quiz
        }
        if quiz.is_end:
            return render(request, 'quiz-result.html', context)
        else:
            return render(request, 'quiz.html', context)


def new_quiz(request):
    quantity = request.POST.get('quantity', None)
    quiz_type = request.POST.get('quiz_type', None)
    quiz = create_quiz(int(quantity), quiz_type, request.user)
    return redirect('quiz', quiz.id)


def quiz_answer(request, pk):
    answer = request.POST.get('answer', None)
    quiz = get_quiz(pk)
    if answer == 'correct':
        quiz.answered(True, request.user)
    else:
        quiz.answered(False, request.user)

    return redirect('quiz', pk)
