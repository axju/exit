import json
from django.core.management.base import BaseCommand, CommandError
from core.models import Decision, Attribute

class Command(BaseCommand):
    help = 'Import game data'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete curent game data',
        )

    def handle(self, *args, **options):
        if options['delete']:
            Decision.objects.all().delete()
            Attribute.objects.all().delete()

        with open(options['filename'], encoding='utf8') as json_file:
            data = json.load(json_file)

        for attribute in data.get('attributes', []):
            attri, created = Attribute.objects.get_or_create(**attribute)
            self.stdout.write(self.style.SUCCESS('Add attribute {}'.format(attri.pk)))

        for question in data.get('questions', []):
            decision, created = Decision.objects.get_or_create(**question['decision'])
            if not created:
                continue

            self.stdout.write(self.style.SUCCESS('Add decision {}'.format(decision.pk)))

            for require in question.get('requires', []):
                attri, _ = Attribute.objects.get_or_create(name=require.get('attribute', 'ERROR'))
                decision.requires.create(attribute=attri, kind=require.get('kind', 'min'), value=require.get('value', 1))

            for answer in question.get('answers', []):
                a = decision.answers.create(name=answer['text'])
                for data in answer.get('attributes', []):
                    attri, _ = Attribute.objects.get_or_create(name=data.get('attribute', 'ERROR'))
                    a.attributes.create(attribute=attri, value=data.get('value', 1))
