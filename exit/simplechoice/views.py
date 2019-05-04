from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse_lazy

from random import randint
from django.utils.crypto import get_random_string
from simplechoice.models import Game, Attribute, Event, Answer, Decision
from simplechoice.forms import NewGameForm, DecisionGameForm


class GameMixin(object):
    """docstring for GameMixin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('game', ''):
            request.session['game'] = get_random_string(length=32)

        self.game, created = Game.objects.get_or_create(key=request.session['game'])
        if created:
            for attr in Attribute.objects.all():
                self.game.attributes.create(attribute=attr, value_max=randint(attr.start_min, attr.start_max))
        return super(GameMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['game'] = self.game
        return super(GameMixin, self).get_context_data(**kwargs)



class IndexView(GameMixin, FormView):
    template_name = 'simplechoice/index.html'
    success_url = reverse_lazy('simplechoice:index')

    def get_form(self, form_class=None):
        if not self.game.name:
            return NewGameForm(self.game, **self.get_form_kwargs())

        elif self.game.status == 1 and self.game.get_decision():
            return DecisionGameForm(self.game, **self.get_form_kwargs())

        #events = self.get_event_query()
        #event = events.filter(kind='victory').first()
        #self.game.status = 3
        #if event:
        #    self.game.text = event.description
        #self.game.save()

        return None

    def form_valid(self, form):
        form.save()

        event = self.get_event()
        print('Find event: {}'.format(event))
        if event:
            self.game.events.create(event=event)
            self.game.status = 4 if event.kind == 'exit' else 2
            #if event.kind == 'exit':
            #    self.game.status = 4

            self.game.save()

        return super(IndexView, self).form_valid(form)

    def get_event(self):
        print('check events')
        for event in self.game.get_event_query():
            n = randint(1,100)
            print(' ', event, n, event.percent)
            if n <= event.percent:
                return event

        return None


class NewView(View):

    def get(self, request, *args, **kwargs):
        del request.session['game']
        return redirect('simplechoice:index')


class ContinueView(GameMixin, View):

    def get(self, request, *args, **kwargs):
        if self.game.status == 2:
            self.game.events.update(seen=True)
            self.game.status = 1
            self.game.save()
        return redirect('simplechoice:index')




class DebugView(GameMixin, TemplateView):
    template_name = "simplechoice/debug.html"

    def get_context_data(self, **kwargs):
        kwargs['events'] = self.game.get_event_query()
        return super(DebugView, self).get_context_data(**kwargs)
