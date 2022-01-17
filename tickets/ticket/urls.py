from django.urls import path
from . import views

urlpatterns = [
    # Ticket
    path('tickets/', views.TicketsView.as_view(), name='tickets'),
    path('ticket/<int:pk>/', views.TicketView.as_view(), name='tickets'),
    path('ticket/add/', views.TicketCreateView.as_view(), name='add_ticket'),
    path('ticket/<int:pk>/edit/', views.TicketUpdateView.as_view(), name='edit_ticket'),
    path('ticket/<int:pk>/delete/', views.TicketDeleteView.as_view(), name='delete_ticket'),
    # Quiz
    path('quizzes/', views.QuizzesView.as_view(), name='quizzes'),
    path('quiz/<int:pk>/', views.QuizView.as_view(), name='quiz'),
    path('quiz/new_quiz/', views.new_quiz, name='new_quiz'),
    path('quiz/<int:pk>/answer/', views.quiz_answer, name='quiz_answer'),
]
