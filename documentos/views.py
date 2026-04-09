from rest_framework import viewsets
from .models import Documento, Proveedor, Categoria, Cliente
from .serializers import DocumentoSerializer, ProveedorSerializer, CategoriaSerializer, ClienteSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Documento.objects.filter(negocio_id=negocio_id)
        return Documento.objects.all()

class ProveedorViewSet(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Proveedor.objects.filter(negocio_id=negocio_id)
        return Proveedor.objects.all()

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Categoria.objects.filter(negocio_id=negocio_id)
        return Categoria.objects.all()

class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer

    def get_queryset(self):
        negocio_id = self.request.query_params.get('negocio_id')
        if negocio_id:
            return Cliente.objects.filter(negocio_id=negocio_id)
        return Cliente.objects.all()