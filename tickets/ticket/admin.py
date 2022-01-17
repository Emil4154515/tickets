from django.contrib import admin
from .models import Ticket
from .models import Quiz
from .models import Answer


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['question', 'correct_answers', 'incorrect_answers', 'last_answer_date']
    search_fields = ['question', 'answer']
    date_hierarchy = 'created_at'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['total_questions', 'correct_answers', 'is_end', 'start_date']
    date_hierarchy = 'created_at'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'quiz', 'correct', 'answer_date']
    date_hierarchy = 'answer_date'
