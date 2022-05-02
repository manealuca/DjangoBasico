from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choise
from django.views import generic
from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.all().filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    return render(request,"polls/index.html",{
        "latest_question_list":latest_question_list
    })

#def detail(request, question_id):
 #   question = get_object_or_404(Question,pk=question_id)
  #  return render(request,"polls/detail.html",{"question":question})


#def result(request, question_id):
 #   question = get_object_or_404(Question,pk=question_id)
  #  return render(request,"polls/result.html",{
   #     "question":question
   # })

class IndexView(generic.ListView):
    templte_name = "polls/index.html"
    context_object_name ='latest_question_list'

    def get_queryset(self):
        """return the last five published questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]



class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_query(self):
        """Excludes any questions that arent published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(DetailView):
    template_name = "polls/result.html"



def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choise = question.choise_set.get(pk=request.POST["choise"])
    except(KeyError,Choise.DoesNotExist):
        return render(request,"polls/detail.html",{
            "question":question,
            "error_message": "No elegiste una respuesta"
        })
    else:
        selected_choise.votes +=1
        selected_choise.save()
        return HttpResponseRedirect(reverse("polls:result",args=(question_id,)))
        


