# from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404 ,render
from django.views import generic

# Create your views here.
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

    # latest_question_list=Question.objects.order_by("-pub_date")[:5]
    # template=loader.get_template("polls/index.html")
    # context={
    #     "latest_question_list": latest_question_list,
    # }
    # return HttpResponse (template.render(context,request))

    # output=",".join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)



class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"




# def detail(request,question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     # try:
#     #     question=Question.objects.get(pk=question_id)
#     # except  Question.DoesNotExist: 
#     #     raise Http404("Question does not exist")
#     return render(request,"polls/detail.html",{"question":question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# def results(request,question_id):
#     question =get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/result.html",{"question":question})

    # response="You're looking at the results of question %s ."
    # return HttpResponse(response % question_id)

def vote(request ,question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError,Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message":"You didnt select a choice.", 
            }
        )
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question_id,)))