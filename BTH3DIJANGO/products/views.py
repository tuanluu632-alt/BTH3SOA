from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product
from .serializers import ProductSerializer


@api_view(['GET', 'POST'])
def products(request):

    # GET /products/
    if request.method == 'GET':

        product_list = Product.objects.all()

        serializer = ProductSerializer(
            product_list,
            many=True
        )

        return Response(serializer.data)


    # POST /products/
    if request.method == 'POST':

        serializer = ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):

    try:

        product = Product.objects.get(id=id)

    except Product.DoesNotExist:

        return Response(
            {
                'message': 'Không tìm thấy sản phẩm'
            },
            status=status.HTTP_404_NOT_FOUND
        )


    # GET /products/<id>/
    if request.method == 'GET':

        serializer = ProductSerializer(product)

        return Response(serializer.data)


    # PUT /products/<id>/
    if request.method == 'PUT':

        serializer = ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    # DELETE /products/<id>/
    if request.method == 'DELETE':

        product.delete()

        return Response(
            {
                'message': 'Xóa sản phẩm thành công'
            },
            status=status.HTTP_204_NO_CONTENT
        )