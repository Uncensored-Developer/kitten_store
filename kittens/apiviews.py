from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Kitten
from .serializers import KittenSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_kitten(request, pk):
    try:
        puppy = Kitten.objects.get(pk=pk)
    except Kitten.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single puppy
    if request.method == 'GET':
        return Response({})
    # delete a single puppy
    elif request.method == 'DELETE':
        return Response({})
    # update details of a single puppy
    elif request.method == 'PUT':
        return Response({})


@api_view(['GET', 'POST'])
def get_post_kittens(request):
    # get all puppies
    if request.method == 'GET':
        puppies = Kitten.objects.all()
        serializer = KittenSerializer(puppies, many=True)
        return Response(serializer.data)
    # insert a new record for a puppy
    elif request.method == 'POST':
        return Response({})
