from django.forms import widgets
from rest_framework import serializers
from modelsapp.models import Contact

class RestAppSerializer(serializers.ModelSerializer):
      """
         This is a serializer class for contact web api
      """
      class Meta:
           model = Contact
           fields = ('first_name','last_name','sur_name','email','phone')

