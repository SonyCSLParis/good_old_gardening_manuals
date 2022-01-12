from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.core import serializers
import json

from .models import *

class IndexView(generic.ListView):
    def get_queryset(self):
        return Manual.objects.order_by('-title')

class ManualView(generic.DetailView):
    model = Manual
    template_name = 'manuals/manual_text.html'

class ManualAnnotationsView(generic.DetailView):
    model = Manual
    template_name = 'manuals/manual_annotations.html'

class AnnotationsJson(generic.ListView):
    http_method_names = ['get']
        
    def get_queryset(self):
        manual = self.kwargs['manual']
        if 'section' in self.kwargs:
            section = self.kwargs['section']
            paragraph = self.kwargs['paragraph']
            sentence = self.kwargs['index']
            return Annotation.objects.filter(manual=manual, section=section,
                                             paragraph=paragraph, sentence=sentence)
        else:
            return Annotation.objects.filter(manual=manual)

    def get_type(self, e):
        if e.content_type.model == 'statement':
            return e.content_object.type
        elif e.content_type.model == 'ontology':
            return 'Ontology'
        else:
            return 'Unknown'

    def get_content(self, e):
        if e.content_type.model == 'statement':
            return {
                'subject': e.content_object.subject,
                'text': e.content_object.text
            }
        elif e.content_type.model == 'ontology':
            o = e.content_object
            content = {
                'names': [name.value for name in o.names.all()],
                'description': o.description,
                'children': []
            }
            for child in o.get_children():
                c = {
                    'names': [name.value for name in child.names.all()],
                    'description': child.description
                }
                content['children'].append(c)
            return content
        else:
            return {}
        
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        annotations = []
        for e in queryset:
            print(f"{e.content_type}")
            annotation = {
                'manual': e.manual,
                'section': e.section,
                'paragraph': e.paragraph,
                'sentence': e.sentence,
                'type': self.get_type(e),
                'content': self.get_content(e)
            }
            annotations.append(annotation)
        #data = serializers.serialize("json", queryset)
        return JsonResponse(json.dumps(annotations), status=200, safe=False)
