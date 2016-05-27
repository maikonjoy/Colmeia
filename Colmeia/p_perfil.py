from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.shortcuts import render

def incluir(request):
    objPerfil = Perfil.create(request.GET['IdPerfil'], request.GET['DescricaoPerfil'], request.GET['DataHoraInclusao'],request.GET['DataHoraExclusao'])
    print objPerfil.valor
    print objPerfil.descricao
    objPerfil.save()
    
#recupera todos os objetos
def recuperaPerfil():
    objPerfil = models.Perfil.objects.all()
    return objPerfil

#recupera todos um objeto especifico pelo id
def recuperaPerfil(idObj):
	objPerfil = models.Perfil.objects.get(IdPerfil=idObj)
	return objPerfil

#recupera todos os objetos
def recuperaPerfilLivre():
    objPerfil = models.Perfil.objects.all()
    cursor = connection.cursor()
    cursor.execute('SELECT P.DescricaoPerfil FROM app_perfil where P.IdPerfil <> 1')
    rows = cursor.fetchall()
    return rows