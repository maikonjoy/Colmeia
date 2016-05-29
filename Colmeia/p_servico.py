#-*- coding: utf-8 -*-
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
import urllib
import json

def incluir(request):
    objSubCategoria = models.SubCategoria.objects.get(IdSubCategoria = request.POST['IdSubCategoria'])
    objCategoria = models.Categoria.objects.get(IdCategoria = objSubCategoria.IdCategoria_id)
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    objServico = models. Servico.create(objCategoria, objSubCategoria, objUser , request.POST['IndicadorTipoServico'],request.POST['DescricaoServico'],request.POST['ValorHora'])
    objServico.save()
    request.session['msg'] = 'Dados inseridos com sucesso'
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
    request.session['msg'] = 'Dados alterados com sucesso'
    return redirect('servicosOferecidos')
    

#exclui um objeto especifico pelo id e o retorna para confirmar a exclusao do objeto
def excluir(request):
	idObj = request.GET['id']
	objExcluido = models.Servico.objects.get(IdServico=idObj)
	objExcluido.delete()
	request.session['msg'] = 'Registro excluído com sucesso.'
	return redirect('servicosOferecidos')

#recupera todos os objetos
def recuperaServicosParaOContratante(id_user):
    objServico = models.Servico.objects.exclude(IdUsuario_id = id_user)
    return objServico

def obterDistancias():
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=en-EN&sensor=false".format(str('Rua Expedicionarios 416, Lagoa Santa'),str('Rua Sergipe 31, Menezes'))
    result= json.load(urllib.urlopen(url))
    print result
    print resul.status.rows.elements.duration.value
    teste = json.dumps(result)
    print teste
    return json.dumps(result)
    
    

#recupera todos um objeto especifico pelo id
def recuperaServico(idObj):
	objServico = models.Servico.objects.get(IdServico=idObj)
	return objServico

#subCategoria, tipoServico, valorHora, descricao

#recupera todos os objetos
def recuperaServicosDoUsuario(id_user):
    objServicos = models.Servico.objects.filter(IdUsuario_id = id_user)
    return objServicos


