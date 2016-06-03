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
from django.db.models import Count
from django.db.models import Avg

def contrataServico(request):
    objUser = models.Usuario.objects.get(IdUsuario = request.user.id)
    objServico = models.Servico.objects.get(IdServico = request.GET['id'])
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'AP')
    objClienteServico = models.ClienteServico.create(objUser, objServico, request.POST['DataServico'],request.POST['QtHoras'],request.POST['ValorHora'],request.POST['ValorTotal'],request.POST['Descricao'],objSituacao)

    objClienteServico.save()
    request.session['msg'] = 'Serviço contratado com sucesso! Aguarde aprovação do prestador. '
    return redirect('servContratados')

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
    id = request.POST['IdClienteServico']
    av = request.POST['nota']
    
    objClienteServico = models.ClienteServico.objects.get(IdClienteServico = id)
    u = objClienteServico.IdServico.IdUsuario_id
    objSituacao = models.SituacaoServico.objects.get(IdSituacaoServico = 'AV')
    objClienteServico.IdSituacao_id = objSituacao
    objClienteServico.Avaliacao = av
    objClienteServico.DataHoraSituacao = datetime.datetime.now()
    objClienteServico.save()
    
    teste = models.ClienteServico.objects.filter(IdServico__IdUsuario_id = u)
    media = models.ClienteServico.objects.filter(IdServico__IdUsuario_id = u, IdSituacao_id='AV').aggregate(Avg('Avaliacao')).values()[0]
    
    if(media is not None):
        objServico = models.Servico.objects.get(IdServico = objClienteServico.IdServico_id)
        objServico.MediaAvaliacao = media
        objServico.save()
    
    request.session['msg'] = 'Serviço avaliado com sucesso!'
    return HttpResponse('OK')

#RECUPERA OS 6 SERVICOS MAIS POPULARES
def servicosMaisPopulares():
    cursor = connection.cursor()
    
    cursor.execute('SELECT C.DescricaoCategoria, SUB.DescricaoSubCategoria, COUNT(CS.IdServico_id) AS Qt_Ocorrencias,(SELECT COUNT(*) FROM app_clienteservico AS QT) AS QT, ((COUNT(CS.IdServico_id)*1.0)/(SELECT COUNT(*) FROM app_clienteservico)*1.0)*100 AS Percentual FROM app_categoria AS C JOIN app_subcategoria AS SUB ON C.IdCategoria = SUB.IdCategoria_id JOIN app_servico AS S ON S.IdSubCategoria_id = SUB.IdSubCategoria JOIN app_clienteservico AS CS ON CS.IdServico_id = S.IdServico GROUP BY (SUB.DescricaoSubCategoria) ORDER BY COUNT(CS.IdServico_id) DESC LIMIT 7;')
    rows = cursor.fetchall()
    return rows

def pesquisa(request,id_user):
    IdCategoria = request.POST['IdCategoria']
    IdSubCategoria = request.POST['IdSubCategoria']
    servicos = None
    AV = ''
    if (not 'PalavraChave' in request.POST):
        PalavraChave = ''
    else:
        PalavraChave = request.POST['PalavraChave']

    if (not 'DiasSemana' in request.POST):
        if (request.POST['Avaliacao'] == ''):
            servicos = models.Servico.objects.filter(IdSubCategoria_id = IdSubCategoria, DescricaoServico__contains = PalavraChave).exclude(IdUsuario_id = id_user)
        else:
            AV = request.POST['Avaliacao']
            servicos = models.Servico.objects.filter(IdSubCategoria_id = IdSubCategoria, MediaAvaliacao__gte = AV, DescricaoServico__contains = PalavraChave).exclude(IdUsuario_id = id_user)

    elif ('DiasSemana' in request.POST):
        dias = request.POST.getlist('DiasSemana')
        lista = [] #guarda os usuarios com disponibilidade nos dias marcados na busca
        IdUsuarios = models.DisponibilidadeUsuario.objects.filter(idDiaSemana_id__in = dias).values_list('idUsuario_id').annotate(total=Count('idUsuario'))
       #converte o retorno para uma lista comum apenas com o Id dos Usuários sem repetição. 
        for usuario in IdUsuarios:
                lista.append(usuario[0])
        if (request.POST['Avaliacao'] == ''):
            #consulta no banco os servicos 
            servicos = models.Servico.objects.filter(IdSubCategoria_id = IdSubCategoria, IdUsuario_id__in = lista, DescricaoServico__contains = PalavraChave).exclude(IdUsuario_id = id_user)
        else:
            AV = request.POST['Avaliacao']
            servicos = models.Servico.objects.filter(IdSubCategoria_id = IdSubCategoria, IdUsuario_id__in = lista, MediaAvaliacao__gte = AV, DescricaoServico__contains = PalavraChave).exclude(IdUsuario_id = id_user)
    
    return servicos

def recuperaQuantidadeServicos():
    servicos = models.ClienteServico.objects.all().count()
    return servicos