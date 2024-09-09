from rest_framework.decorators import api_view
from rest_framework.response import Response

from home.models import Person
from home.serializers import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from rest_framework.decorators import action

class LoginAPI(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,  
                 'message':serializer.errors
            })
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password= serializer.data['password'])
        if user is None:
            return Response({
                'status': False,
                'message': 'Invalid credentials'
            })
       
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'status': True , 'message':'user Login',  'token': token.key})
class RegisterApi(APIView):

    def post(self, request):
        data=request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status': False,  
                 'message':serializer.errors
            })

        serializer.save()
        return Response({'status': True , 'message':'user created'})

@api_view(['GET','POST'])
def index(request):
    courses = {
        'course_name': 'Python',
        'learn': ['Flask', 'Django', 'Tornado', 'FastAPI'],
        'course_provider': 'Scaler'
    }

    if request.method == 'GET':
        print('You hit a GET method')
        return Response(courses)
    
    elif request.method == 'POST':
        data = request.data
        print(data)
        print('You hit a POST method')
        return Response(courses)


# Login

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer( data= data)

    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message': 'success'})
    return Response(serializer.errors)

#Person
class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        try:
            print(request.user)
            objs= Person.objects.all()
            page = request.GET.get('page' , 1)
            page_size = 3 
        
            paginator = Paginator(objs, page_size)
        
            serializer = PeopleSerializer(paginator.page(page) , many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'sataus':False,
                'message':'Invalid Page'
            })
        # print(Person.objects.all())
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
   

#People

@api_view(['GET', 'POST'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.all()
        serializer = PeopleSerializer(objs , many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PeopleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            
        return Response(serializer.errors)

class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    @action(detail=True, methods=['GET'])
    def send_mail_to_person(self ,  request, pk):
        obj = Person.objects.get(pk=pk)
        serializer = PeopleSerializer(obj)
        return Response({
            'status': True,
            'message':'email sent successfully' 
        })
