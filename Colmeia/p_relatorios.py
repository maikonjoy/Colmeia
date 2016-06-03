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

#RELATORIO PRESTADOR
def servicosPrestados(id_user):
    cursor = connection.cursor()
    cursor.execute('SELECT distinct IndicadorTipoServico , descricaoServico, COUNT(IdServico) as qtdServico, SUM(ValorTotal) as valorTotal FROM app_servico s inner join app_clienteservico c ON s.IdServico = c.IdServico_id WHERE s.IdUsuario_id =' + id_user +' GROUP BY IndicadorTipoServico , DescricaoServico')
    rows = cursor.fetchall()
    return rows

#RELATORIO CONTRATANTE
def servicosContratados(id_user):
    cursor = connection.cursor()
    cursor.execute('SELECT distinct IndicadorTipoServico , descricaoServico, COUNT(IdServico) as qtdServico, SUM(ValorTotal) as valorTotal FROM app_servico s inner join app_clienteservico c ON s.IdServico = c.IdServico_id WHERE c.IdUsuario_id = '+ str(id_user) +' GROUP BY IndicadorTipoServico , DescricaoServico')
    rows = cursor.fetchall()
    return rows

#RELATORIO ADMIN
def quantidadeUsuariosGeral():
    cursor = connection.cursor()
    cursor.execute('SELECT distinct DescricaoPerfil,  COUNT(user_id) as qtdUsuario  FROM app_usuario u inner join app_perfil p ON u.IdPerfil_id = p.IdPerfil GROUP BY DescricaoPerfil')
    rows = cursor.fetchall()
    return rows

#RELATORIO ADMIN
def quantidadeUsuariosMensal():
    cursor = connection.cursor()
    cursor.execute("SELECT distinct strftime('+%%m+', u.DataHoraInclusao)  as mes ,DescricaoPerfil,  COUNT(user_id) as qtdUsuario  FROM app_usuario u inner join app_perfil p ON u.IdPerfil_id = p.IdPerfil WHERE strftime('%%m', u.DataHoraInclusao) ="+ str(datetime.datetime.today().month)+" GROUP BY DescricaoPerfil,  strftime('%%m', u.DataHoraInclusao) , strftime('%%Y', u.DataHoraInclusao)")
    rows = cursor.fetchall()
    return rows

#RElLATOIO ADMIN
def melhoresAvaliacoes():
    cursor = connection.cursor()
    cursor.execute('SELECT descricaosubcategoria, Avaliacao FROM app_servico S inner join app_subcategoria SUB ON S.IdSubCategoria_id = SUB.IdSubCategoria inner join app_clienteservico c ON s.IdServico = c.IdServico_id WHERE Avaliacao>(SELECT (SUM(Avaliacao)/count(IdClienteServico)) as media FROM app_servico s inner join app_clienteservico c ON s.IdServico = c.IdServico_id) GROUP BY descricaosubcategoria')
    rows = cursor.fetchall()
    return rows

#RELATORIO ADMIN
def pioresAvaliacoes():
    cursor = connection.cursor()
    cursor.execute('SELECT descricaosubcategoria, Avaliacao FROM app_servico s inner join app_subcategoria SUB ON S.IdSubCategoria_id = SUB.IdSubCategoria inner join app_clienteservico c ON s.IdServico = c.IdServico_id WHERE Avaliacao<=(SELECT (SUM(Avaliacao)/count(IdClienteServico)) as media FROM app_servico s inner join app_clienteservico c ON s.IdServico = c.IdServico_id) GROUP BY descricaosubcategoria')
    rows = cursor.fetchall()
    return rows

#SALDO PRONTOS
def saldoPontosPrestador(id_user):
    cursor = connection.cursor()
    cursor.execute('SELECT  sum( ValorTotal) as totalPontos From app_clienteservico c INNER JOIN app_servico s ON c.IdServico_id = s.IdServico WHERE IndicadorTipoServico = 2 and s.IdUsuario_id = 2 EXCEPT SELECT  sum( ValorTotal) as totalPontos From app_clienteservico c INNER JOIN app_servico s ON c.IdServico_id = s.IdServico WHERE IndicadorTipoServico = 2 and c.IdUsuario_id = '+ id_user)
    rows = cursor.fetchall()
    return rows