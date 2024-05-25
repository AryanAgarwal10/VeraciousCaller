from django.shortcuts import render
import logging
from authentication.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Contact
from .serializers import ContactCreationSerializer
from rest_framework import permissions
from django.db.models import Q
from rest_framework import status
# Create your views here.
class ContactList(ListCreateAPIView):

    serializer_class = ContactCreationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)


class ContactDetailView(GenericAPIView):

    serializer_class = ContactCreationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,**kwargs):
        id=kwargs['id']
        try:
            contact=Contact.objects.get(id=id)

        except Contact.DoesNotExist:
            return Response({
                 'message':'No Contact found for id'
                },status=status.HTTP_400_BAD_REQUEST)
           
        phone_number=contact.phone_number
        email=""
        if contact.owner==request.user:
    
            user=User.objects.filter(phone_number=phone_number)
            if user:
                email=user.email

        res={
            'id':contact.id,
            'phone_number':contact.phone_number,
            'name': contact.name,
            'email':email
        }
        return Response({
            'data':res,
        },status=status.HTTP_200_OK)
    
class ContactNameSearchView(GenericAPIView):
    serializer_class = ContactCreationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request,**kwargs):
        query=kwargs['name']
        contacts_start_with_query= Contact.objects.filter(name__istartswith=query)
        contacts_contains_query=Contact.objects.filter(~Q(name__istartswith=query),Q(name__icontains=query))
        contacts=contacts_start_with_query.union(contacts_contains_query)
        data=[{"id":contact.id,"name": contact.name, "phone_number": contact.phone_number} for contact in contacts]
        return Response({
            'data':data,
        },status=status.HTTP_200_OK)

class ContactPhoneSearchView(GenericAPIView):
    serializer_class = ContactCreationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request,**kwargs):
        query=kwargs['phone']
        
        user=User.objects.filter(phone_number=query)
        print("phone ",query)
        if user.exists():
            data=[{"name":user.name,"phone_number":user.phone_number}for user in user]
        else:
            contacts= Contact.objects.filter(phone_number=query)
            data=[{"id":contact.id,"name": contact.name, "phone_number": contact.phone_number} for contact in contacts]
        return Response({
            'data':data,
        },status=status.HTTP_200_OK)