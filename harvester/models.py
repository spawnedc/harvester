from django.db import models
from django.core import serializers

import json

class HarvesterBaseModel(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def to_json(self):
        serialized_self = json.loads(serializers.serialize('json', [ self, ]))[0]

        self_json = serialized_self.get('fields')
        self_json['id'] = serialized_self.get('pk')

        return self_json


class User(HarvesterBaseModel):
    email = models.EmailField()
    data_harvest_app_name = models.CharField(max_length=200)
    data_harvest_auth_key = models.CharField(max_length=200)
    invoice_harvest_app_name = models.CharField(max_length=200)
    invoice_harvest_auth_key = models.CharField(max_length=200)

    def __unicode__(self):
        return self.email