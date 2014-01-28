from django.core.management.base import NoArgsCommand, CommandError

from fancypages.utils import (FP_PAGE_MODEL, FP_NODE_MODEL, get_node_model,
                              get_page_model)


class Command(NoArgsCommand):
    """
    Create new pages for every existing node that doesn't have a corresponding

    """

    def handle_noargs(self, **options):
        # this makes the management command work nicely with the South
        # frozen ORM
        if 'orm' in options:
            orm = options['orm']
            try:
                Category = orm[FP_NODE_MODEL]
            except KeyError:
                CommandError(
                    "could not find model 'Category'. Aborting command.")
            try:
                FancyPage = orm[FP_PAGE_MODEL]
            except KeyError:
                CommandError(
                    "could not find model 'FancyPage'. Aborting command.")
        else:
            Category = get_node_model()
            FancyPage = get_page_model()

        for category in Category.objects.filter(page=None):
            # there seems to be no FP for this category so let's create one.
            FancyPage.objects.create(node=category)
