from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import make_password
from .serializers import RegistrationSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User

EXTENSION_INDEX = 1
CV_FILE_SEPARATOR = ""


@api_view(['POST'])
def register_new_user(request):
    def user_does_not_exists(data):
        return not User.objects.filter(username=data['email']).exists()

    def send_response(msg, res_status):
        return Response({'message': msg}, status=res_status)

    def create_new_user_in_db(data):
        User.objects.create(first_name=data['first_name'],
                            last_name=data['last_name'],
                            username=data['email'],
                            email=data['email'],
                            password=make_password(data['password']))

    registration_data = request.data
    user = RegistrationSerializer(data=registration_data)
    if user.is_valid():
        if user_does_not_exists(registration_data):
            create_new_user_in_db(registration_data)
            return send_response("Success while registering a new user", status.HTTP_201_CREATED)
        else:
            return send_response("User already exists", status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = UserSerializer(request.user)
    return Response(user.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_existing_user_credentials(request):
    def is_passwd_not_empty(password):
        return password != ''

    def update_existing_user(exiting_user_cred, new_user_cred):
        exiting_user_cred.first_name = new_user_cred['first_name']
        exiting_user_cred.last_name = new_user_cred['last_name']
        exiting_user_cred.username = new_user_cred['email']
        exiting_user_cred.email = new_user_cred['email']
        new_passwd = new_user_cred["password"]
        if is_passwd_not_empty(new_passwd):
            existing_user.password = make_password(new_passwd)

    existing_user = request.user
    new_user_credentials = request.data
    update_existing_user(existing_user, new_user_credentials)
    existing_user.save()
    serializer = UserSerializer(existing_user, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_user_cv(request):
    def send_error_response(err_msg, status_code):
        return Response({'error': err_msg}, status=status_code)

    def validate_file_extension(file_name):
        valid_extensions = ["pdf"]
        extension = file_name.split(CV_FILE_SEPARATOR)[EXTENSION_INDEX]
        if extension in valid_extensions:
            return True
        return False

    def file_not_found(file_name):
        return file_name == ''

    user = request.user
    cv = request.FILES['resume']
    if file_not_found(cv):
        return send_error_response("Error occurred, please upload your CV", status.HTTP_400_BAD_REQUEST)

    is_valid_file = validate_file_extension(cv.name)
    if not is_valid_file:
        return send_error_response("Upload only for pdf extension files", status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user, many=False)
    user.userprofile.cv = cv
    user.userprofile.save()
    return Response(serializer.data, status=status.HTTP_200_OK)
