# from django.http import HttpResponse
# from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        from datetime import datetime

        return {"my_date": datetime.now()}
