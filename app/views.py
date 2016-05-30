"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from datetime import datetime
from .forms import UsuarioForm, UserForm, EnderecoForm, DiferencialForm, ServicoForm, DisponibilidadeForm, PesquisaForm,PesquisaFormSite,ContrataServicoForm
from Colmeia import p_usuario
from Colmeia import p_servico, p_categoria, p_diferencial, p_disponibilidade, p_clienteServico

#PAGINA INICIAL DO SITE (GERAL)

def index(request):
    """Renders the home page."""
    form = UsuarioForm()
    userfrm = UserForm()
    endereco = EnderecoForm()
    frmPesquisa = PesquisaForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/site/indexSite.html',{'form': form, 'userfrm': userfrm,'endereco':endereco,'frmPesquisa': frmPesquisa},
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Início',
            'year':datetime.now().year,
            'servicosPopulares': p_clienteServico.servicosMaisPopulares(),
            'qtContratacoes': p_clienteServico.recuperaQuantidadeServicos(),
        })
    )

def s_quemSomos(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/site/s_quemSomos.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Quem Somos',
            'year':datetime.now().year,
        })
    )

def s_contato(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/site/s_contato.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Contato',
            'year':datetime.now().year,
        })
    )

#PAGINA INICIAL DO SISTEMA
@login_required(redirect_field_name='')
def inicio(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        return render(
            request,
            'app/index.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Index',
                'year':datetime.now().year
            })
    )

#PAGINA INICIAL DO SISTEMA
def search(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/geral/resultados.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Resultados',
            'year':datetime.now().year,
        })
    )

#PAGINA QUEM SOMOS PARA QUEM ESTA LOGADO
@login_required(redirect_field_name='')
def quemSomos(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        return render(
            request,
            'app/geral/quemSomos.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Quem Somos',
                'year':datetime.now().year,
            })
    )
   
#PAGINA INICIAL DO ADMINISTRADOR
@login_required(redirect_field_name='')
def admin(request):
   if not request.user.is_authenticated():
        return HttpResponse('loginpage')
   else:
        return render(
            request,
            'app/admin/admin.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Administrador',
                'qtPrestadores': p_usuario.recuperaQtdPrestPendentes(),
                'qtContratantes': p_usuario.recuperaQtdPrestPendentes(),
                'year':datetime.now().year,
            })
    )

#PAGINA INICIAL DO PRESTADOR
@login_required(redirect_field_name='')
def prestadores(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        users = p_usuario.recuperaPrestadoresPendentesAprovacao()     
        return render(
            request,
            'app/admin/prestadores.html',
            context_instance = RequestContext(request,
            {

                'title':'Colmeia | Prestadores',
                'year':datetime.now().year,
                'usuariosPendentes': users,
            })
    )

#PAGINA INICIAL DO CONTRATANTES
@login_required(redirect_field_name='')
def contratantes(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        users = p_usuario.recuperaContratantesPendentesAprovacao()     
        return render(
            request,
            'app/admin/contratantes.html',
            context_instance = RequestContext(request,
            {

                'title':'Colmeia | Prestadores',
                'year':datetime.now().year,
                'usuariosPendentes': users,
            })
    )
    
#PAGINA INICIAL DOS RELATÓRIOS ADM.
@login_required(redirect_field_name='')
def relatorioAdm(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        return render(
            request,
            'app/admin/relatorioAdm.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Relatorios',
                'year':datetime.now().year,
            })
    )
   

#PAGINA CADASTRAL DO PRESTADOR
@login_required(redirect_field_name='')
def servicosOferecidos(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        frmServico = ServicoForm()
        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        return render(
            request,
            'app/prestador/servicosOferecidos.html', {'frmServico': frmServico},
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Serviços Oferecidos',
                'year':datetime.now().year,
                'msg': msg,    
                'servicos': p_servico.recuperaServicosDoUsuario(request.user.id),
            })

    )

#PAGINA CADASTRAL DO PRESTADOR
@login_required(redirect_field_name='')
def diferenciais(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        frmDiferencial = DiferencialForm()
        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        return render(
            request,
            'app/prestador/diferenciais.html', {'frmDif': frmDiferencial},
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Diferenciais',
                'year':datetime.now().year,
                'frmDif': frmDiferencial,
                'msg': msg,
                'diferenciais': p_diferencial.recuperaDiferenciaisPorPrestador(request.user.id),
            })

    )

#PAGINA DOS SERVIÇOS PRESTADOS
@login_required(redirect_field_name='')
def disponibilidade(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        frmDisponibilidade = DisponibilidadeForm()
        
        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None

        return render(
            request,
            'app/prestador/disponibilidade.html',{'frmDisponibilidade': frmDisponibilidade},
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Disponibilidade',
                'year':datetime.now().year,
                'msg': msg,
                'disponibilidade': p_disponibilidade.recuperaDisponibilidadePorPrestador(request.user.id),
            })
    )

#PAGINA DOS SERVIÇOS PRESTADOS
@login_required(redirect_field_name='')
def gerServicos(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:

        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        return render(
            request,
            'app/prestador/gerServicos.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Gerenciador de Serviços',
                'year':datetime.now().year,
                'msg':msg,
                'servicos' : p_clienteServico.recuperaServicosPorPrestador(request.user.id),
            })
    )

#PAGINA DO COLMEIA PONTOS
@login_required(redirect_field_name='')
def colmeiaPontos(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:

        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        return render(
            request,
            'app/prestador/colmeiaPontos.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Colpontos',
                'year':datetime.now().year,
                'msg': msg,
            })
    )

#PAGINA DO COLMEIA PONTOS
@login_required(redirect_field_name='')
def relPrestador(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        return render(
            request,
            'app/prestador/relatorioPrestador.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Relatorios Prestador',
                'year':datetime.now().year,
            })
    )
       
#VIEWS DOS CONTRATANTES
#PAGINA DOS SERVICOS CONTRATADOS
@login_required(redirect_field_name='')
def pesquisaServicos(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        frmPesquisa = PesquisaForm()
        frmContratar = ContrataServicoForm()
        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        servicos = p_servico.recuperaServicosParaOContratante(request.user.id)
        return render(
            request,
            'app/contratante/pesquisaServicos.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Contratante',
                'year':datetime.now().year,
                'msg': msg,
                'servicos': servicos,
                #'distancias': p_servico.obterDistancias(servicos),
                'frmPesquisa': frmPesquisa,
                'frmContratar' : frmContratar,
            })
    )

#PAGINA CADASTRAL CONTRATANTES 
@login_required(redirect_field_name='')
def servContratados(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        if request.session.has_key('msg'):
            msg = request.session['msg']
            del request.session['msg']
        else:
            msg = None
        return render(
            request,
            'app/contratante/servContratados.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Servicos Contratados',
                'year':datetime.now().year,
                'msg': msg,
                'servicos' : p_clienteServico.recuperaServicosPorCliente(request.user.id),
            })
    )

#PAGINA DOS RELATÓRIOS DE SERVICOS CONTRATADOS
@login_required(redirect_field_name='')
def relContratante(request):
    if not request.user.is_authenticated():
        return HttpResponse('loginpage')
    else:
        return render(
            request,
            'app/contratante/relatorioContratante.html',
            context_instance = RequestContext(request,
            {
                'title':'Colmeia | Relatorios Contratante',
                'year':datetime.now().year,
            })
    )

def sair(request):
    #Renders the about page.
    request.session.flush()
    return redirect('index')
   
def fazLogin(request):
    usuario = request.POST['login']
    senha = request.POST['password']
    
    user = authenticate(username = usuario, password = senha)

    if user is not None:
        if user.is_active:
            login(request, user)
            return render(
                request,
                'app/index.html',
                context_instance = RequestContext(request,
                {
                    'title':'Colmeia | Início',
                    'year':datetime.now().year,
                }))
        else:
            return render(
                request,
                'app/geral/login.html',
                context_instance = RequestContext(request,
                {
                    'title':'Colmeia | Login',
                    'year':datetime.now().year,
                    'logged': 'no', 
                    'msg' : user.first_name + u', seu perfil ainda não foi aprovado pelo administrador. Favor aguardar e-mail que confirma a aprovação do seu cadastro.',
                }))
    else:
         return render(
         request,
        'app/geral/login.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Login',
            'year':datetime.now().year,
            'msg' : 'Usuario ou senha invalidos. Tente novamente.',
        }))

def loginpage(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/geral/login.html',
        context_instance = RequestContext(request,
        {
            'title':'Colmeia | Login',
            'year':datetime.now().year,
        })
    )
