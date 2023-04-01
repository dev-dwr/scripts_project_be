from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from .models import Offer, Candidate
from rest_framework.response import Response
from .serializers import OfferSerializer, CandidateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from .filters import OfferFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

NUM_OF_ELEMENTS_PER_PAGE = 4


@api_view(['GET'])
def get_all_offers(req):
    filter_set = OfferFilter(req.GET, queryset=Offer.objects.all().order_by('id'))
    count = filter_set.qs.count()
    paginator = PageNumberPagination()
    paginator.page_size = NUM_OF_ELEMENTS_PER_PAGE
    query_set = paginator.paginate_queryset(filter_set.qs, req)
    serializer = OfferSerializer(query_set, many=True)
    return Response({
        "num": count,
        "num_of_el_per_page": NUM_OF_ELEMENTS_PER_PAGE,
        "offers": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_offer(request):
    request.data["user"] = request.data
    offer_entry = request.data
    job = Offer.objects.create(**offer_entry)
    serializer = OfferSerializer(job, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_existing_offer_by_pk(request, pk):
    def update_offer(old_offer, req):
        old_offer.title = req.data['title']
        old_offer.industry = req.data['industry']
        old_offer.experience = req.data['experience']
        old_offer.salary = req.data['month_salary,']
        old_offer.positions = req.data['positions']
        old_offer.company = req.data['company']
        old_offer.description = req.data['description']
        old_offer.email = req.data['email']
        old_offer.address = req.data['address']
        old_offer.job_type = req.data['job_type']

    offer = get_object_or_404(Offer, id=pk)
    if offer.user != request.user:
        return Response({"message": "Your are not a owner of this offer"}, status=status.HTTP_403_FORBIDDEN)
    update_offer(offer, request)
    offer.save()
    serializer = OfferSerializer(offer, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_offer_by_pk(_, pk):
    offer = get_object_or_404(Offer, id=pk)
    serializer = OfferSerializer(offer, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_offer_by_pk(request, pk):
    offer = get_object_or_404(Offer, id=pk)
    if offer.user != request.user:
        return Response({"message": "Your are not a owner of this offer"}, status=status.HTTP_403_FORBIDDEN)
    offer.delete()
    return Response({'message': 'Offer deleted successfully'},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def get_offer_statistics(_, title):
    def check_valid_offer(received_offers, received_topic):
        if len(received_offers) == 0:
            return Response({'message': f'Not stats found for {received_topic}'})

    args = {'title__icontains': title}
    offers = Offer.objects.filter(**args)
    check_valid_offer(offers, title)
    statistics = offers.aggregate(min_salary=Min('month_salary'), max_salary=Max('month_salary'),
                                  total_offers=Count('title'),
                                  avg_positions=Avg('positions'), avg_salary=Avg('month_salary'))
    return Response(statistics, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_for_the_offer(request, pk):
    def send_error_response(err_msg, status_code):
        return Response({'error': err_msg}, status=status_code)

    def does_user_applied(received_offer, received_user):
        return received_offer.candidate_set.filter(user=received_user).exists()

    def apply_for_offer(received_offer, received_user, cv):
        return Candidate.objects.create(offer=received_offer, user=received_user, cv=cv)

    def is_offer_expired(received_offer):
        return received_offer.expiration_date < timezone.now()

    def does_user_uploaded_cv(cv):
        return cv == ''

    user = request.user
    offer = get_object_or_404(Offer, id=pk)
    if does_user_uploaded_cv(user.userprofile.cv):
        return send_error_response('Upload your cv first', status.HTTP_400_BAD_REQUEST)
    if is_offer_expired(offer):
        return send_error_response('Offer has expired, you cannot apply', status.HTTP_400_BAD_REQUEST)

    if does_user_applied(offer, user):
        return send_error_response('You have already applied for this offer', status.HTTP_400_BAD_REQUEST)

    offer_applied = apply_for_offer(offer, user, user.userprofile.cv)
    return Response({'applied': True, 'offer_id': offer_applied.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_applied_offers(request):
    filter_args = {'user_id': request.user.id}
    offers = Candidate.objects.filter(**filter_args)
    serializer = CandidateSerializer(offers, many=True)
    return Response(serializer.data)
