from django import forms
from random import randint
from simplechoice.models import Decision, Answer, Event

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

        game_decision = self.game.get_decision()
        if not game_decision:
            print('error')
            return

        decision = game_decision.decision
        OPTIONS = [ (a.pk, a.name) for a in decision.answers.order_by('?')]
        self.fields['decision'] = forms.ChoiceField(label=decision.question, widget=forms.RadioSelect(), choices=OPTIONS)


    def save(self):
        print('Save form')
        print('Data', self.cleaned_data['decision'])
        decision = self.game.get_decision()
        if not decision:
            print('error')
            return

        answer = Answer.objects.get(pk=self.cleaned_data['decision'])
        decision.answer = answer
        decision.save()
        print('Save answer {}'.format(answer))

        for attr in answer.attributes.all():
            attribute = self.game.attributes.get(attribute=attr.attribute)
            value = min(attribute.value + attr.value, attribute.value_max)
            attribute.value = max(value, 0)
            attribute.save()
        self.game.save()
