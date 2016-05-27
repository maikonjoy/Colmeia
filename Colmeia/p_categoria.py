from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.template import RequestContext
from django.core import serializers

#recupera todos os objetos CATEGORIA
def recuperaCategorias():
    objCategoria = models.Categoria.objects.all()
    return objCategoria

#recupera todos os objetos SUB-CATEGORIA
def recuperaSubCategorias():
    objCategoria = models.SubCategoria.objects.all().values_list('IdSubCategoria','DescricaoSubCategoria')
    return objCategoria

#recupera todos um objetos SUBCATORIA por CATEGORIA selecionada
def recuperaSubCategoriasPorCategoria(request):
    idCategoria = request.POST['idCategoria']
    objSubCategoria = models.SubCategoria.objects.filter(IdCategoria_id=idCategoria)
    data = serializers.serialize('json', objSubCategoria)
    return HttpResponse(data)

#recupera todos os objetos SUBCATEGORIA
def recuperaSubCategoria(idSubCategoria):
    objSubCategoria = models.SubCategoria.objects.get(IdSubCategoria = idSubCategoria)
    return objSubCategoria


