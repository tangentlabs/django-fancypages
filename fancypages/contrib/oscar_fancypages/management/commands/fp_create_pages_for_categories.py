from django.db.models import get_model
from django.core.management.base import NoArgsCommand, CommandError


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        # this makes the management command work nicely with the South
        # frozen ORM
        if 'orm' in options:
            orm = options['orm']
            try:
                Category = orm['catalogue.Category']
            except KeyError:
                CommandError(
                    "could not find model 'Category'. Aborting command."
                )
            try:
                FancyPage = orm['fancypages.FancyPage']
            except KeyError:
                CommandError(
                    "could not find model 'FancyPage'. Aborting command."
                )
        else:
            Category = get_model('catalogue', 'Category')
            FancyPage = get_model('fancypages', 'FancyPage')

        for category in Category.objects.all():
            # let's check if a FP for this category already exists. If so
            # we just ignore it since we don't want to override any data
            try:
                FancyPage.objects.get(slug=category.slug)
            except FancyPage.DoesNotExist:
                pass
            else:
                continue
            # there seems to be no FP for this category so let's create one.
            fp = FancyPage()
            for field in category._meta.fields:
                setattr(fp, field.attname, getattr(category, field.attname))
            fp.category_ptr = category
            fp.save()
