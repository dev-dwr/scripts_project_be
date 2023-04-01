from rest_framework import serializers
from .models import Offer, Candidate


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()

    class Meta:
        model = Candidate
        fields = ('cv', 'applied_at', 'user', 'job')
