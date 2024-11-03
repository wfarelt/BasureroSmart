from django.contrib import admin
from .models import Reward, RewardClaim
# Register your models here.

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('name', 'points_required', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'points_required')
    actions = ['activate_rewards', 'deactivate_rewards']

    def activate_rewards(self, request, queryset):
        queryset.update(status=True)
        self.message_user(request, 'Las recompenzas fueron activadas exitosamente')

    def deactivate_rewards(self, request, queryset):
        queryset.update(status=False)
        self.message_user(request, 'Las recompenzas fueron desactivadas exitosamente')

    activate_rewards.short_description = 'Activar recompenzas seleccionadas'
    deactivate_rewards.short_description = 'Desactivar recompenzas seleccionadas'

@admin.register(RewardClaim)
class RewardClaimAdmin(admin.ModelAdmin):
    list_display = ('user', 'reward', 'claim_date', 'status')
    list_filter = ('status', 'claim_date')
    search_fields = ('user__username', 'reward__name', 'status')
    actions = ['mark_as_executed', 'mark_as_canceled']

    def mark_as_executed(self, request, queryset):
        queryset.update(status='Ejecutado')
        self.message_user(request, 'Las reclamaciones fueron marcadas como ejecutadas exitosamente')

    def mark_as_canceled(self, request, queryset):
        queryset.update(status='Anulado')
        self.message_user(request, 'Las reclamaciones fueron marcadas como anuladas exitosamente')

    mark_as_executed.short_description = 'Marcar como ejecutadas'
    mark_as_canceled.short_description = 'Marcar como anuladas'