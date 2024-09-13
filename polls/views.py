from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question
from .forms import QuestionForm, ChoiceFormSet


from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
            :5
        ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)



def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            # Don't save the question yet, add pub_date first
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()  # Set the current time for pub_date
            question.save()  # Now save the question with pub_date

            # save the choices, linking them to the question
            formset.instance = question
            formset.save()

            return redirect('polls:index')  # Redirect to index after saving

    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'polls/add_question.html', {
        'question_form': question_form,
        'formset': formset
    })