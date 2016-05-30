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
import datetime
from django.db import connection

def contrataServico(request):
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    objServico = models.Servico.objects.get(IdServico = request.GET['id'])
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'AP')
    objClienteServico = models.ClienteServico.create(objUser, objServico, request.POST['DataServico'],request.POST['QtHoras'],request.POST['ValorHora'],request.POST['ValorTotal'],request.POST['Descricao'],objSituacao)

    objClienteServico.save()
    request.session['msg'] = 'Serviço contratado com sucesso! Aguarde aprovação do prestador. '
    return redirect('servContratados')
    
#def alterar(request):
#    idObj = request.GET['id']
#    objServico = models.Servico.objects.get(IdServico=idObj)
#    objSubCategoria = models.SubCategoria.objects.get(IdSubCategoria = request.POST['IdSubCategoria'])
#    objCategoria = models.Categoria.objects.get(IdCategoria = objSubCategoria.IdCategoria_id)
#    objServico.IdCategoria = objCategoria
#    objServico.IdSubCategoria_id = objSubCategoria
#    objServico.ValorHora = request.POST['ValorHora']
#    objServico.IndicadorTipoServico = request.POST['IndicadorTipoServico']
#    objServico.DescricaoServico = request.POST['DescricaoServico']

#    objServico.save()
#    return redirect('SeD')

#exclui um objeto especifico pelo id e o retorna para confirmar a exclusao do objeto
def excluir(request):
	idObj = request.GET['id']
	objExcluido = models.ClienteServico.objects.get(IdClienteServico=idObj)
	objExcluido.delete()
	return redirect('SeD')

#recupera todos os objetos
def recuperaServicos():
    objClienteServico = models.ClienteServico.objects.filter(IdServico__IdUsuario_id != id_user)
    return objClienteServico


    

#recupera todos um objeto especifico pelo id
def recuperaServico(idObj):
	objServico = models.ClienteServico.objects.get(IdServico=idObj)
	return objServico

#subCategoria, tipoServico, valorHora, descricao

#recupera todos os objetos
def recuperaServicosPorPrestador(id_user):
    objServicos = models.ClienteServico.objects.filter(IdServico__IdUsuario_id = id_user)
    return objServicos

#recupera todos os objetos
def recuperaServicosPorCliente(id_user):
    objServicos = models.ClienteServico.objects.filter(IdUsuario_id = id_user)
    return objServicos

#MARCA O SERVIÇO COMO ACEITO
def aceitarServico(request):
    id = request.GET['id']
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    objClienteServico.DataHoraConfirmacao = datetime.datetime.now()
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'AG')
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    request.session['msg'] = 'Serviço confirmado com sucesso!'
    return redirect('gerServicos')

#CANCELA O SERVICO POR SOLICITACAO DO PRESTADOR
def cancelarServicoP(request):
    id = request.GET['id']
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'CP')
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    request.session['msg'] = 'Serviço cancelado com sucesso!'
    return redirect('gerServicos')

#MUDA O STATUS DO SERVIÇO PARA EXECUTADO
def executarServico(request):
    id = request.GET['id']
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'EX')
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    request.session['msg'] = 'Serviço marcado como EXECUTADO com sucesso!'
    return redirect('gerServicos')

#CANCELA O SERVICO POR SOLICITACAO DO CLIENTE
def cancelarServicoC(request):
    id = request.GET['id']
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'CC')  
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    request.session['msg'] = 'Serviço cancelado com sucesso!'
    return redirect('servContratados')

#AVALIAÇÃO DO SERVICO PELO CLIENTE
def avaliarServico(request):
    id = request.GET['id']
    av = request.GET['av']
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'AV')
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.Avaliacao = av
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    request.session['msg'] = 'Serviço avaliado com sucesso!'
    return redirect('servContratados')

#RECUPERA OS 6 SERVICOS MAIS POPULARES
def servicosMaisPopulares():
    cursor = connection.cursor()
    
    cursor.execute('SELECT C.DescricaoCategoria, SUB.DescricaoSubCategoria, COUNT(CS.IdServico_id) AS Qt_Ocorrencias,(SELECT COUNT(*) FROM app_clienteservico AS QT) AS QT, ((COUNT(CS.IdServico_id)*1.0)/(SELECT COUNT(*) FROM app_clienteservico)*1.0)*100 AS Percentual FROM app_categoria AS C JOIN app_subcategoria AS SUB ON C.IdCategoria = SUB.IdCategoria_id JOIN app_servico AS S ON S.IdSubCategoria_id = SUB.IdSubCategoria JOIN app_clienteservico AS CS ON CS.IdServico_id = S.IdServico GROUP BY (SUB.DescricaoSubCategoria) ORDER BY COUNT(CS.IdServico_id) DESC LIMIT 7;')
    rows = cursor.fetchall()
    return rows

def pesquisa(request):
    IdCategoria = request.POST['IdCategoria']
    IdSubCategoria = request.POST['IdSubCategoria']
    PalavraChave = request.POST['PalavraChave']
    DiasSemana = request.POST['DiasSemana']
    IdCategoria = request.POST['IdCategoria']
def recuperaQuantidadeServicos():
    servicos = models.ClienteServico.objects.all().count()
    return servicos