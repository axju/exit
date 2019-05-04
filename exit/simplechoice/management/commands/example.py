from django.simplechoice.management.base import BaseCommand, CommandError
from simplechoice.models import Decision, Attribute

class Command(BaseCommand):
    help = 'Create some example data'

    def add_decision(self, level, question, answers):
        decision, created = Decision.objects.get_or_create(
            question=question,
            level=level)
        if not created:
            self.stdout.write(self.style.WARNING('Decision already exists'))
            return
        for name in answers:
            if type(name) is list:
                answers = decision.answers.create(name=name[0])
                answers.attributes.create(attribute=name[1], value=name[2])
            elif type(name) is str:
                decision.answers.create(name=name)
        self.stdout.write(self.style.SUCCESS('Create decision'))

    def handle(self, *args, **options):
        intelligenz, _ = Attribute.objects.get_or_create(
            name='Intelligenz',
            description='Wie schlau bist du?'
        )

        leichtsinnig, _ = Attribute.objects.get_or_create(
            name='Leichtsinnig',
            description='Gehst du gerne Risiken ein?'
        )

        aktive, _ = Attribute.objects.get_or_create(
            name='Aktive',
            description='Wie aktive bist du? Ligst du nur auf dem Sofa, oder bist du viel unterwegs?'
        )

        self.add_decision(
            question='Draußen scheint die Sonne, doch im TV läuft deine Lieblings Serie. Gehst du raus oder guckst du TV?',
            level=6,
            answers=[['Draußen spielen', aktive, 2], ['TV gucken', aktive, -1]]
        )
        self.add_decision(
            question='Du hast etwas Taschengeld bekommen. Du kannst dir jetzt was zu Naschen kaufen oder du Sparst das Geld für Später.',
            level=8,
            answers=[['Naschen', intelligenz, 5], 'Sparen']
        )
        self.add_decision(
            question='Du bist alleine zu Hause, was machst du?',
            level=14,
            answers=['Freunde einladen', 'Pizza und TV']
        )
        self.add_decision(
            question='Ein Freund bietet dir eine Zigarette an. Nimmst du sie?',
            level=14,
            answers=['Klar', 'Nein']
        )
        self.add_decision(
            question='Ein älterer Freund läd dich zu einer Party ein. Deine Eltern haben dir verbotn hinzugehen. Gehst du trotzdem?',
            level=14,
            answers=['Ja', 'Nein']
        )
