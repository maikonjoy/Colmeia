#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect

def incluir(request):
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    idTipo = request.POST['IdTipoDiferencial']
    objTipoDiferencial = models.TipoDiferencial.objects.get(IdTipoDiferencial = idTipo)
    objDiferencial = models.Diferencial.create(objUser, objTipoDiferencial, request.POST['Ano'],request.POST['TituloDiferencial'],request.POST['DescricaoDiferencial'])
    objDiferencial.save()
    request.session['msg'] = 'Dados inseridos com sucesso'
    return redirect('diferenciais')

def alterar(request):
	idObj = request.GET['id']
	objDiferencial = models.Diferencial.objects.get(IdDiferencial=idObj)
	
	objDiferencial.IdUsuario_id = request.user.id
	objDiferencial.IdTipoDiferencial_id = request.POST['IdTipoDiferencial']
	objDiferencial.Ano = request.POST['Ano']
	objDiferencial.TituloDiferencial = request.POST['TituloDiferencial']
	objDiferencial.DescricaoDiferencial = request.POST['DescricaoDiferencial']
	objDiferencial.save()
	request.session['msg'] = 'Dados alterados com sucesso'
	return redirect('diferenciais')

#exclui um objeto especifico pelo id e o retorna para confirmar a exclusao do objeto
def excluir(request):
	idObj = request.GET['id']
	objExcluido = models.Diferencial.objects.get(IdDiferencial=idObj)
	objExcluido.delete()
	request.session['msg'] = 'Registro excluido com sucesso!'
	return redirect('diferenciais')

#recupera todos os objetos
def recuperaDiferencial():
    objDiferencial = models.Diferencial.objects.all()
    return objDiferencial

#recupera todos um objeto especifico pelo id
def recuperaDiferencial(idObj):
	objDiferencial = models.Diferencial.objects.get(IdDiferencial=idObj)
	return objDiferencial

#subCategoria, tipoDiferencial, valorHora, descricao

#recupera todos os objetos
def recuperaDiferenciaisPorPrestador(id_user):
    objDiferenciais = models.Diferencial.objects.filter(IdUsuario_id = id_user)
    return objDiferenciais


