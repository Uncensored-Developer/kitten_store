from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Kitten
from .serializers import KittenSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_kitten(request, pk):
    try:
        kitten = Kitten.objects.get(pk=pk)
    except Kitten.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single kitten
    if request.method == 'GET':
        serializer = KittenSerializer(kitten)
        return Response(serializer.data)
    # delete a single kitten
    elif request.method == 'DELETE':
        kitten.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single kitten
    elif request.method == 'PUT':
        serializer = KittenSerializer(kitten, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_kittens(request):
    # get all kittens
    if request.method == 'GET':
        puppies = Kitten.objects.all()
        serializer = KittenSerializer(puppies, many=True)
        return Response(serializer.data)
    # insert a new record for a kitten
    elif request.method == 'POST':
        data = {
            'name': request.data['name'],
            'age': int(request.data['age']),
            'breed': request.data['breed'],
            'color': request.data['color']
        }
        serializer = KittenSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
