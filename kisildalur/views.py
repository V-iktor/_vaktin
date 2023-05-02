from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from _verdvaktin.models import Cpu

from kisildalur.models import Choice, Product, Question

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

import requests

class IndexView(generic.ListView):
    API_URL = "https://kisildalur.is/api/categories/9?includes=sub_public_categories,sub_public_categories.media,public_products&fields=id,propgroups,name,sub_public_categories(id,name,media(medium_url)),public_products(id,special_order,properties,name,price,external_stock,in_stock,in_reserve,in_coming"

    r = requests.get(API_URL)
    products_response = r.json()
    products = products_response["public_products"]
    for product in products:
        obj, created = Product.objects.update_or_create(
            id=product["id"],
            defaults={
                "price": product["price"],
                "name": product["name"],
                "isInStock": product["in_stock"] > 0,
                "group": Cpu.get_group_from_regex(product["name"]),
            },
        )
    
    template_name = "kisildalur/cpu.html"
    context_object_name = "cpus"

    def get_queryset(self):
        return Product.objects.all().order_by("group")



# class IndexView(generic.ListView):
#     template_name = "kisildalur/index.html"
#     context_object_name = "latest_question_list"

#     def get_queryset(self):
#         """
#         Return the last five published questions (not including those set to be
#         published in the future).
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
#             :5
#         ]


class DetailView(generic.DetailView):
    model = Question
    template_name = "kisildalur/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "kisildalur/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "kisildalur/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("kisildalur:results", args=(question.id,)))
