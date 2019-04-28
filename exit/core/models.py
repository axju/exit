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





class Exit(models.Model):
    EXIT_KINDS = (
        ('victory', 'victory'),
        ('failure', 'failure'),
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

class ExitAttribute(models.Model):
    exit = models.ForeignKey(Exit, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='exits')
    kind = models.CharField(_('value kind'), max_length=3, choices=VALUE_KINDS)
    value = models.IntegerField(default=1)

    def __str__(self):
        return '{} [{} {}]'.format(self.attribute.name, self.kind, self.value)


class Game(models.Model):
    key = models.CharField(_('key'), max_length=64)
    name = models.CharField(_('name'), max_length=256, null=True, blank=True)

    status = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

    def __str__(self):
        return '{} - {}'.format(self.key, self.name)

class GameDecision(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='decisions')
    decision = models.ForeignKey(Decision, on_delete=models.CASCADE, related_name='games')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.decision, self.answer)

class GameAttribute(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name='games')
    value = models.IntegerField(default=1)
    value_max = models.IntegerField(default=100)

    def __str__(self):
        return self.attribute.name + ' -> ' + str(self.value) +'/' + str(self.value_max)
