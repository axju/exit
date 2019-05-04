from django.db import models
from django.utils.translation import ugettext_lazy as _

VALUE_KINDS = (
    ('min', 'Min'),
    ('max', 'Max'),
)

class Attribute(models.Model):
    name = models.CharField(_('attribute'), max_length=64)
    description = models.TextField(_('description'), default='...')
    start_min = models.IntegerField(default=80)
    start_max = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Decision(models.Model):
    question = models.TextField(_('question'))
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.question[:30]

    class Meta:
        ordering = ('level', '?')

class DecisionRequireAttribute(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='requires')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='+')
    kind = models.CharField(_('value kind'), max_length=3, choices=VALUE_KINDS)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{}]'.format(self.attribute.name, self.value)

class Answer(models.Model):
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='answers')
    name = models.CharField(_('name'), max_length=128)

    def __str__(self):
        return self.name[:30]

class AnswerGetAttribute(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='+')
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{}]'.format(self.attribute.name, self.value)





class Event(models.Model):
    EXIT_KINDS = (
        ('victory', 'victory'),
        ('failure', 'failure'),
        ('exit', 'exit'),
    )
    name = models.CharField(_('name'), max_length=128)
    description = models.TextField(_('description'), default='')
    level_min = models.IntegerField(default=1)
    level_max = models.IntegerField(default=100)
    kind = models.CharField(_('kind'), max_length=8, choices=EXIT_KINDS)
    percent = models.FloatField(default=10)

    class Meta:
        ordering = ('?', )

    def __str__(self):
        return self.name

    def attributes_count(self):
        return self.attributes.count()
    attributes_count.short_description = 'attributes'

class EventAttribute(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='events')
    kind = models.CharField(_('value kind'), max_length=3, choices=VALUE_KINDS)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{} {}]'.format(self.attribute.name, self.kind, self.value)


class Game(models.Model):
    GAME_STATUS = (
        (0, 'begin'),
        (1, 'choices'),
        (2, 'text'),

        (3, 'victory'),
        (4, 'exit'),

        (5, 'error'),
    )
    key = models.CharField(_('key'), max_length=64)
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)

    status = models.IntegerField(default=0, choices=GAME_STATUS)
    level = models.IntegerField(default=1)

    def __str__(self):
        return '{} - {}'.format(self.key, self.name)

    def decisions_count(self):
        return self.decisions.count()
    decisions_count.short_description = 'Decisions'

    def get_event_query(self):
        events = Event.objects.filter(level_min__lte=self.level, level_max__gte=self.level).exclude(games__game=self)

        for attribute in self.attributes.all():
            events = events.exclude(attributes__kind='min', attributes__attribute=attribute.attribute, attributes__value__gt=attribute.value)
            events = events.exclude(attributes__kind='max', attributes__attribute=attribute.attribute, attributes__value__lt=attribute.value)

        return events

    def get_decision(self):
        """get the curent decision"""
        game_decision = self.decisions.filter(answer__isnull=True).first()
        if game_decision:
            print('Have open decisions')
            return game_decision

        decision = Decision.objects.exclude(games__game=self).first()
        if decision:
            print('Created new decisions')
            game_decision = self.decisions.create(decision=decision)
            self.level = decision.level
            self.save()
            return game_decision

        print('No more decisions. Find exit event')
        events = self.get_event_query()
        event = events.filter(kind='victory').first()
        if event:
            self.events.create(event=event)
            self.status = 3
        else:
            self.status = 5
        self.save()
        return None

    def event(self):
        event = self.events.filter(seen=False).first()
        if event:
            return event.event
        return None

class GameDecision(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='decisions')
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='games')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.decision, self.answer)

class GameEvent(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='events')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='games')
    seen = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.event.name, self.event.kind)

class GameAttribute(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='games')
    value = models.IntegerField(default=1)
    value_max = models.IntegerField(default=100)

    def __str__(self):
        return self.attribute.name + ' -> ' + str(self.value) +'/' + str(self.value_max)
