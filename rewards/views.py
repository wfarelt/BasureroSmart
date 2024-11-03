from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Reward, RewardClaim
from core.models import WasteContainer, User
from .forms import RewardForm, RewardClaimForm, WasteContainerForm 
from django.views.generic import CreateView, ListView, UpdateView
    

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

class RewardListView(ListView):
    model = Reward
    template_name = 'rewards/reward_list.html'
    context_object_name = 'rewards'
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Recompensas'
        return context
    
class RewardCreateView(CreateView):
    model = Reward
    form_class = RewardForm
    template_name = 'rewards/reward_form.html'
    success_url = reverse_lazy('list_reward')
    
class RewardUpdateView(UpdateView):
    model = Reward
    form_class = RewardForm
    template_name = 'rewards/reward_form.html'
    success_url = reverse_lazy('list_reward')

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

class RewardClaimListView(ListView):
    model = RewardClaim
    template_name = 'rewards/claim_list.html'
    context_object_name = 'claims'
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

class WasteContainerListView(ListView):
    model = WasteContainer
    template_name = 'rewards/container_list.html'
    context_object_name = 'containers'
    # añadir titulo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Contenedores'
        return context

class WasteContainerCreateView(CreateView):
    model = WasteContainer
    form_class = WasteContainerForm
    template_name = 'rewards/container_form.html'
    success_url = reverse_lazy('list_container')

class WasteContainerUpdateView(UpdateView):
    model = WasteContainer
    form_class = WasteContainerForm
    template_name = 'rewards/container_form.html'
    success_url = reverse_lazy('list_container')