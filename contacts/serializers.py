from contacts.models import Contact
from rest_framework import serializers

class ContactCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['id','phone_number','name']

    def validate(self,attrs):
        request=self.context.get('request')
        contact=Contact.objects.filter(owner=request.user,phone_number=attrs.get('phone_number'))
        if contact:
            message ="Contact already exists"
            raise serializers.ValidationError(message)
        return{
            'phone_number':attrs.get('phone_number'),
            'name':attrs.get('name')
        }
        
    def create(self,validated_data):
        request=self.context.get('request')
        contact=Contact.objects.create_contact(
            owner=request.user,
            phone_number=validated_data.get('phone_number'),
            name=validated_data.get('name')
        )
        return contact
    