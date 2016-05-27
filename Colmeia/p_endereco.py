# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Endereco
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

def incluir(request): 
    objEndereco = Endereco.create(request.POST['CEP'],request.POST['Estado'],request.POST['Cidade'], request.POST['Bairro'],request.POST['Logradouro'],request.POST['Latitude'],request.POST['Longitude'],request.POST['Numero'],request.POST['Complemento'] )
    objEndereco.save()

def recuperaUltimoEndereco():
    objPerfil = models.Perfil.objects.all()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM app_endereco ORDER BY (IdEndereco) DESC ')
    rows = cursor.fetchall()
    obj = Endereco.objects.latest('IdEndereco')
    return obj