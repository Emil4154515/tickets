from .models import Quiz


def get_quiz(pk):
    quiz = Quiz.objects.prefetch_related('user_answer').get(id=pk)
    return quiz


def create_quiz(quantity, quiz_type, user):
    quiz = Quiz.create_quiz(quantity, quiz_type, user)
    return quiz
