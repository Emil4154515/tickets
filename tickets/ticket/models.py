import datetime
from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models import F, ExpressionWrapper, fields


class Ticket(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)

    # Analytical data
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)

    last_answer_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, related_name='ticket', on_delete=models.CASCADE)

    @classmethod
    def get_tickets(cls, ticket_type, count, user):
        if ticket_type == 'standard':
            tickets = cls.objects.filter(user=user).order_by('last_answer_date').all()[:count]
        elif ticket_type == 'new':
            tickets = cls.objects.filter(user=user).order_by('-created_at').all()[:count]
        else:
            rate = ExpressionWrapper(F('correct_answers') - F('incorrect_answers'), output_field=fields.IntegerField())
            tickets = cls.objects.filter(user=user).annotate(rate=rate).order_by('rate').all()[:count]

        return tickets

    def __str__(self):
        return self.question[:50]


class Quiz(models.Model):
    class Result(models.TextChoices):
        better = 'BETTER', 'Better'
        without_changes = 'NOCHAN', 'Without changes'
        worse = 'WORSE', 'Worse'

    total_questions = models.IntegerField()
    current_question = models.IntegerField(default=1)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    is_end = models.BooleanField(default=False)

    # Quiz timeline
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)

    # Analytical data
    result_by_last_quizzes = models.CharField(max_length=6, null=True, choices=Result.choices)
    result_by_last_quizzes_score = models.FloatField(null=True)
    result_text = models.CharField(max_length=255, null=True)

    questions = models.ManyToManyField(Ticket, related_name='quiz', through='Answer')
    user = models.ForeignKey(User, related_name='quiz', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_quiz(cls, quantity, quiz_type, user):
        ticket_count = Ticket.objects.filter(user=user).count()
        if quantity >= ticket_count:
            quantity = ticket_count
        quiz = cls.objects.create(total_questions=quantity, start_date=datetime.datetime.now(), user=user)
        tickets = Ticket.get_tickets(quiz_type, quantity, user)
        answers = []
        for index, ticket in enumerate(tickets):
            answers.append(
                Answer(
                    question_queue=index+1,
                    ticket=ticket,
                    quiz=quiz,
                    user=user,
                )
            )
        Answer.objects.bulk_create(answers)
        return quiz

    @classmethod
    def get_user_last_results(cls, user):
        quizzes = cls.objects.filter(user=user).order_by('-created_at')[:15]
        rate_list = []
        for quiz in quizzes:
            rate_list.append(quiz.correct_answers/quiz.total_questions)
        rate_total = sum(rate_list) / len(rate_list)
        print(rate_total)
        return rate_total

    def calc_results(self, user):
        last_quizzes_score = Quiz.get_user_last_results(user)
        self.result_by_last_quizzes_score = last_quizzes_score - (self.correct_answers / self.total_questions)

        # If the result is worse than 5%
        if self.result_by_last_quizzes_score > 0.05:
            self.result_by_last_quizzes = self.Result.worse
            self.result_text = f'The result is {self.result_by_last_quizzes_score*100}% worse than in the previous 15 quizzes'
        # If the result is better than 5%
        elif self.result_by_last_quizzes_score < -0.05:
            self.result_by_last_quizzes = self.Result.better
            self.result_text = f'The result is {self.result_by_last_quizzes_score*100}% better than in the previous 15 quizzes'
        # If there is no noticeable difference
        else:
            self.result_by_last_quizzes = self.Result.without_changes
            if self.result_by_last_quizzes_score > 0:
                self.result_text = f'The result is {self.result_by_last_quizzes_score*100}% better than in the previous 15 quizzes'
            else:
                self.result_text = f'The result is {self.result_by_last_quizzes_score*100}% better than in the previous 15 games'
        self.save()

    def questions_left(self):
        return self.total_questions - self.current_question

    def get_result_color(self):
        if round((self.correct_answers / self.total_questions), 1) > 0.65:
            return 'success'
        elif round((self.correct_answers / self.total_questions), 1) < 0.35:
            return 'danger'
        else:
            return 'warning'

    def get_done_percent(self):
        return (self.current_question / self.total_questions) * 100

    def get_correct_percent(self):
        return (self.correct_answers / self.total_questions) * 100

    def get_score(self):
        return round((self.correct_answers / self.total_questions) * 10, 1)

    def get_current_ticket(self):
        answer = self.user_answer.order_by('question_queue').all()[self.current_question-1]
        return answer

    def answered(self, correct: bool, user):
        answer = self.get_current_ticket()
        answer.set_stat(correct)

        if self.current_question == self.total_questions:
            self.is_end = True
            self.end_date = datetime.datetime.now()
        else:
            self.current_question = self.current_question + 1

        if correct:
            self.correct_answers = self.correct_answers + 1
        else:
            self.incorrect_answers = self.incorrect_answers + 1

        self.save()
        self.calc_results(user)

    def __str__(self):
        return f'{self.total_questions}/{self.correct_answers} | {self.created_at}'


class Answer(models.Model):
    question_queue = models.IntegerField()
    ticket = models.ForeignKey(Ticket, related_name='user_answer', on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='user_answer', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_answer', on_delete=models.CASCADE)
    correct = models.BooleanField(null=True)
    answer_date = models.DateTimeField(null=True)

    def set_stat(self, correct):
        ticket = self.ticket
        if correct:
            ticket.correct_answers += 1
        else:
            ticket.correct_answers -= 1
        ticket.last_answer_date = datetime.datetime.now()
        ticket.save()

        self.answer_date = datetime.datetime.now()
        self.correct = correct
        self.save()

    def __str__(self):
        return self.ticket.question[:50]
