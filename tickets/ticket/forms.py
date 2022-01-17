from django import forms
from .mixins import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['question', 'answer']
