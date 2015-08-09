from django.forms import widgets
from rest_framework import serializers
from modelsapp.models import Contact

class RestAppSerializer(serializers.ModelSerializer):
      class Meta:
           model = Contact
           fields = ('first_name','last_name','sur_name','email','phone')

