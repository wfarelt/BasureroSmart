from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Reward, RewardClaim
from core.models import Transaction
from core.models import WasteContainer, User
from .forms import RewardForm, RewardClaimForm, WasteContainerForm 
from django.views.generic import CreateView, ListView, UpdateView

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin    
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    users_count = User.objects.filter(is_active=True).count()
    rewards_count = Reward.objects.filter(status=True).count()
    containers_count = WasteContainer.objects.count()
    clains_count = RewardClaim.objects.filter(status='Pendiente').count()
    context = {
        'users_count': users_count,
        'rewards_count': rewards_count,
        'containers_count': containers_count,
        'clains_count': clains_count,
    }
    return render(request, 'rewards/home.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso')
            return redirect('home')  # Redirige a la página principal después de iniciar sesión
        else:
            messages.error(request, 'Credenciales incorrectas')
    else:
        form = AuthenticationForm()

    return render(request, 'rewards/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión

class RewardListView(LoginRequiredMixin, ListView):
    model = Reward
    template_name = 'rewards/reward_list.html'
    context_object_name = 'rewards'
    login_url = 'login'
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Recompensas'
        return context
    
class RewardCreateView(LoginRequiredMixin, CreateView):
    model = Reward
    form_class = RewardForm
    template_name = 'rewards/reward_form.html'
    success_url = reverse_lazy('list_reward')
    login_url = 'login'
    
class RewardUpdateView(LoginRequiredMixin, UpdateView):
    model = Reward
    form_class = RewardForm
    template_name = 'rewards/reward_form.html'
    success_url = reverse_lazy('list_reward')
    login_url = 'login'

def disable_reward(request, pk):
    reward = Reward.objects.get(pk=pk)
    reward.status = False
    reward.save()
    return redirect('list_reward')

def enable_reward(request, pk):
    reward = Reward.objects.get(pk=pk)
    reward.status = True
    reward.save()
    return redirect('list_reward')

class RewardClaimListView(LoginRequiredMixin, ListView):
    model = RewardClaim
    template_name = 'rewards/claim_list.html'
    context_object_name = 'claims'
    login_url = 'login'
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Solicitudes de Recompensas'
        return context

def claim_execute(request, pk):
    claim = RewardClaim.objects.get(pk=pk)
    reward = Reward.objects.get(pk=claim.reward.pk)
    reward.stock -= 1
    reward.save()
    claim.status = 'Ejecutado'
    claim.save()
    return redirect('list_claim')

def claim_cancel(request, pk):
    claim = RewardClaim.objects.get(pk=pk)
    claim.status = 'Anulado'
    claim.save()
    return redirect('list_claim')

class WasteContainerListView(LoginRequiredMixin, ListView):
    model = WasteContainer
    template_name = 'rewards/container_list.html'
    context_object_name = 'containers'
    login_url = 'login'
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contenedores'
        return context

class WasteContainerCreateView(LoginRequiredMixin, CreateView):
    model = WasteContainer
    form_class = WasteContainerForm
    template_name = 'rewards/container_form.html'
    success_url = reverse_lazy('list_container')
    login_url = 'login'

class WasteContainerUpdateView(LoginRequiredMixin, UpdateView):
    model = WasteContainer
    form_class = WasteContainerForm
    template_name = 'rewards/container_form.html'
    success_url = reverse_lazy('list_container')
    login_url = 'login'
    
# Lista de usuarios, nombre de usuario, nombre, apellido, correo electrónico, cantidad de transacciones, cantidad de puntos, cantidad de recompensas canjeadas
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'rewards/user_list.html'
    context_object_name = 'users'
    login_url = 'login'
    
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Usuarios'
        context['transactions'] = Transaction.objects.filter(user=self.request.user).count()
        context['claims'] = RewardClaim.objects.filter(user=self.request.user).count()
        return context
    
    