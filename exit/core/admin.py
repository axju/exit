from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin

from core.models import Attribute
from core.models import Game, GameDecision
from core.models import Decision, DecisionRequireAttribute, Answer, AnswerGetAttribute
from core.models import Exit, ExitAttribute

class AttributeAdmin(admin.ModelAdmin):
    pass

class GameDecisionInline(admin.TabularInline):
    model = GameDecision

class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status', 'level', 'decisions_count')
    inlines = [GameDecisionInline,]

class AnswerGetAttributeInline(NestedTabularInline):
    model = AnswerGetAttribute
    extra = 1
    fk_name = 'answer'

class AnswerInline(NestedTabularInline):
    model = Answer
    extra = 1
    fk_name = 'decision'
    inlines = [AnswerGetAttributeInline, ]

class DecisionRequireAttributeInline(NestedTabularInline):
    model = DecisionRequireAttribute
    extra = 1
    fk_name = 'decision'

class DecisionAdmin(NestedModelAdmin):
    model = Decision
    inlines = [DecisionRequireAttributeInline, AnswerInline]
    list_display = ('__str__', 'level')

class ExitAttributeInline(admin.TabularInline):
    model = ExitAttribute

class ExitAdmin(admin.ModelAdmin):
    inlines = [ExitAttributeInline,]



admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(Exit, ExitAdmin)
