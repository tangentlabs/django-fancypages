from django.db import models


class AbstractFancyPage(models.Model):
    class Meta:
        abstract = True


class AbstractContainer(models.Model):
    class Meta:
        abstract = True


class AbstractWidgetModel(models.Model):
    class Meta:
        abstract = True
