from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']  # Only the question text

# Inline formset to allow multiple choices to be submitted with a question
ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, fields=['choice_text'], extra=3, can_delete=False
)
