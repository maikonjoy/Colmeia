# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import sqlite3
from app import models
from app.models import Perfil
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

def contrataServico(request):
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    objServico = models.Servico.objects.get(IdServico = request.GET['id'])
    objClienteServico = models.ClienteServico.create(objUser, objServico, request.POST['DataServico'],request.POST['QtHoras'],request.POST['ValorHora'],request.POST['ValorTotal'],request.POST['Descricao'])

    objClienteServico.save()
    request.session['msg'] = 'Serviço contratado com sucesso! Aguarde aprovação do prestador. '
    return redirect('servicosOferecidos')
    
def alterar(request):
    idObj = request.GET['id']
    objServico = models.Servico.objects.get(IdServico=idObj)
    objSubCategoria = models.SubCategoria.objects.get(IdSubCategoria = request.POST['IdSubCategoria'])
    objCategoria = models.Categoria.objects.get(IdCategoria = objSubCategoria.IdCategoria_id)
    objServico.IdCategoria = objCategoria
    objServico.IdSubCategoria_id = objSubCategoria
    objServico.ValorHora = request.POST['ValorHora']
    objServico.IndicadorTipoServico = request.POST['IndicadorTipoServico']
    objServico.DescricaoServico = request.POST['DescricaoServico']

    objServico.save()
    return redirect('SeD')

#exclui um objeto especifico pelo id e o retorna para confirmar a exclusao do objeto
def excluir(request):
	idObj = request.GET['id']
	objExcluido = models.ClienteServico.objects.get(IdServico=idObj)
	objExcluido.delete()
	return redirect('SeD')

#recupera todos os objetos
def recuperaServicos():
    objServico = models.ClienteServico.objects.all()
    return objServico

#recupera todos um objeto especifico pelo id
def recuperaServico(idObj):
	objServico = models.ClienteServico.objects.get(IdServico=idObj)
	return objServico

#subCategoria, tipoServico, valorHora, descricao

#recupera todos os objetos
def recuperaServicosPorPrestador(id_user, s):
    if (s == ''):
        objServicos = models.ClienteServico.objects.filter(IdUsuario_id = id_user,Situacao = s)
    else:
        objServicos = models.ClienteServico.objects.filter(IdUsuario_id = id_user)
    
    return objServicos

#recupera todos os objetos
def recuperaServicosPorCliente(id_user):
    objServicos = models.ClienteServico.objects.filter(IdUsuario_id = id_user)
    return objServicos

