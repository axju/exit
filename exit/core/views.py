from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, RedirectView, TemplateView
from django.urls import reverse_lazy

from random import randint

from core.models import Game, Attribute, Exit
from core.forms import NewGameForm, DecisionGameForm


class GameMixin(object):
    """docstring for GameMixin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.session.session_key:
            request.session.create()
        key = request.session.session_key
        self.game, created = Game.objects.get_or_create(key=key)
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
            return DecisionGameForm(self.game, **self.get_form_kwargs())
        return None

    def form_valid(self, form):
        form.save()
        return super(IndexView, self).form_valid(form)


class NewView(View):

    def get(self, request, *args, **kwargs):
        print('adasasdadasdasd')
        request.session.flush()
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
