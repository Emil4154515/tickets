# Generated by Django 4.0.1 on 2022-01-16 20:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_queue', models.IntegerField()),
                ('correct', models.BooleanField(null=True)),
                ('answer_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.CharField(max_length=500)),
                ('correct_answers', models.IntegerField(default=0)),
                ('incorrect_answers', models.IntegerField(default=0)),
                ('last_answer_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_questions', models.IntegerField()),
                ('current_question', models.IntegerField(default=0)),
                ('correct_answers', models.IntegerField(default=0)),
                ('incorrect_answers', models.IntegerField(default=0)),
                ('is_end', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('result_by_last_quizzes', models.CharField(choices=[('BETTER', 'Better'), ('NOCHAN', 'Without changes'), ('WORSE', 'Worse')], max_length=6, null=True)),
                ('result_by_last_quizzes_score', models.FloatField(null=True)),
                ('result_text', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('questions', models.ManyToManyField(related_name='quiz', through='ticket.Answer', to='ticket.Ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='ticket.quiz'),
        ),
        migrations.AddField(
            model_name='answer',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='ticket.ticket'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to=settings.AUTH_USER_MODEL),
        ),
    ]
