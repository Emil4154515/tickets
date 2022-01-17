from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import View
from django.views.generic.base import RedirectView
from django.urls import reverse

from .models import Ticket
from .models import Quiz


class TicketMixin(View):

    def dispatch(self, request, *args, **kwargs):
        tickets = Ticket.objects.filter(user=request.user).all().order_by('-created_at')

        page = request.GET.get('page', 1)
        tickets_count = tickets.count()
        paginator = Paginator(tickets, 12)
        try:
            tickets = paginator.page(page)
        except PageNotAnInteger:
            tickets = paginator.page(1)
        except EmptyPage:
            tickets = paginator.page(paginator.num_pages)

        self.tickets = tickets
        self.tickets_count = tickets_count

        return super().dispatch(request, *args, **kwargs)


class QuizMixin(View):

    def dispatch(self, request, *args, **kwargs):
        quizzes = Quiz.objects.filter(user=request.user).all().order_by('-created_at')

        page = request.GET.get('page', 1)
        quizzes_count = quizzes.count()
        paginator = Paginator(quizzes, 12)
        try:
            quizzes = paginator.page(page)
        except PageNotAnInteger:
            quizzes = paginator.page(1)
        except EmptyPage:
            quizzes = paginator.page(paginator.num_pages)

        self.quizzes = quizzes
        self.quizzes_count = quizzes_count

        return super().dispatch(request, *args, **kwargs)