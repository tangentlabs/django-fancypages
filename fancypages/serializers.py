import json


class BaseSerializer(object):

    def serialize(self, tile):
        raise NotImplemented()


class JsonSerializer(BaseSerializer):

    def serialize(self, tile):
        print tile
