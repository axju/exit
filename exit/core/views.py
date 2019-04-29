from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse_lazy

from random import randint
from django.utils.crypto import get_random_string
from core.models import Game, Attribute, Exit, Answer, Decision
from core.forms import NewGameForm, DecisionGameForm


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
    template_name = 'core/index.html'
    success_url = reverse_lazy('core:index')

    def get_form(self, form_class=None):
        if self.game.status == 0:
            return NewGameForm(self.game, **self.get_form_kwargs())

        elif self.game.status == 1:

            if self.game.decisions.filter(answer__isnull=True).count() > 0:
                return DecisionGameForm(self.game, **self.get_form_kwargs())

            decision = Decision.objects.exclude(games__game=self.game).first()
            if decision:
                self.game.decisions.create(decision=decision)
                self.game.level = decision.level
                self.game.save()
                return DecisionGameForm(self.game, **self.get_form_kwargs())
            else:
                exits = self.get_exit_query()
                exit = exits.filter(kind='victory').first()
                self.game.status = 3
                if exit:
                    self.game.text = exit.description
                self.game.save()

        return None

    def form_valid(self, form):
        form.save()

        exit = self.get_exit()
        if exit:
            self.game.text = exit.description
            self.game.status = 2
            if exit.kind == 'exit':
                self.game.status = 4

            self.game.save()

        return super(IndexView, self).form_valid(form)

    def get_exit_query(self):
        exits = Exit.objects.filter(level_min__lte=self.game.level, level_max__gte=self.game.level)
        for attribute in self.game.attributes.all():
            exits = exits.exclude(attributes__kind='min', attributes__attribute=attribute.attribute, attributes__value__gte=attribute.value)
            exits = exits.exclude(attributes__kind='max', attributes__attribute=attribute.attribute, attributes__value__lte=attribute.value)
        return exits

    def get_exit(self):
        for exit in self.get_exit_query():
            n = randint(1,100)
            if n <= exit.percent:
                return exit

        return None


class NewView(View):

    def get(self, request, *args, **kwargs):
        del request.session['game']
        return redirect('core:index')


class ContinueView(GameMixin, View):

    def get(self, request, *args, **kwargs):
        self.game.status = 1
        self.game.save()
        return redirect('core:index')




class DebugView(GameMixin, TemplateView):
    template_name = "core/debug.html"

    def get_context_data(self, **kwargs):
        exits = Exit.objects.filter(level_min__lte=self.game.level)
        for attribute in self.game.attributes.all():
            exits = exits.exclude(attributes__kind='min', attributes__attribute=attribute.attribute, attributes__value__gte=attribute.value)
            exits = exits.exclude(attributes__kind='max', attributes__attribute=attribute.attribute, attributes__value__lte=attribute.value)

        kwargs['exits'] = exits
        return super(DebugView, self).get_context_data(**kwargs)
