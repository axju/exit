from django import forms

from core.models import Decision, Answer

class BasicGameForm(forms.Form):

    def __init__(self, game, *args, **kwargs):
        super(BasicGameForm, self).__init__(*args, **kwargs)
        self.game = game


class NewGameForm(BasicGameForm):
    name = forms.CharField()

    def save(self):
        self.game.name = self.cleaned_data['name']
        self.game.status = 1
        self.game.save()
        print(self.game.status)


class DecisionGameForm(BasicGameForm):

    def __init__(self, game, *args, **kwargs):
        super(DecisionGameForm, self).__init__(game, *args, **kwargs)

        decision = self.game.decisions.filter(answer__isnull=True).first()
        if decision:
            decision = decision.decision
        else:
            decision = self.new_decision()

        if decision:
            OPTIONS = [ (a.pk, a.name) for a in decision.answers.order_by('?')]
            self.fields['decision'] = forms.ChoiceField(label=decision.question, widget=forms.RadioSelect(), choices=OPTIONS)

    def new_decision(self):
        decision = Decision.objects.exclude(games__game=self.game).first()
        if decision:
            self.game.decisions.create(decision=decision)
        else:
            self.game.status = 10
            self.game.save()
        return decision

    def save(self):
        decision = self.game.decisions.get(answer__isnull=True)
        if not decision:
            print('error')
            return

        print(self.cleaned_data['decision'])
        answer = Answer.objects.get(pk=self.cleaned_data['decision'])
        decision.answer = answer
        decision.save()

        for attr in answer.get.all():
            print(attr.attribute.name, attr.value)
            print(attr)
            attribute = self.game.attributes.get(attribute=attr.attribute)
            value = min(attribute.value + attr.value, attribute.value_max)
            attribute.value = max(value, 0)
            attribute.save()

        decision = self.new_decision()
        if self.game.status == 1:
            self.game.level = decision.level
        self.game.save()
