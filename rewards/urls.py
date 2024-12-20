from django.urls import path
from . import views
from .views import train_model_view

urlpatterns = [
    path('', views.home, name='home' ),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Rewards
    path('rewards/create/', views.RewardCreateView.as_view(), name='create_reward' ),
    path('rewards/list', views.RewardListView.as_view(), name='list_reward' ),
    path('rewards/update/<int:pk>', views.RewardUpdateView.as_view(), name='update_reward' ),
    path('rewards/disable/<int:pk>', views.disable_reward, name='disable_reward' ),
    path('rewards/enable/<int:pk>', views.enable_reward, name='enable_reward' ),
    # Rewards Claim
    path('rewards/claim/list', views.RewardClaimListView.as_view(), name='list_claim' ),
    path('rewards/claim/execute/<int:pk>', views.claim_execute, name='execute_claim' ),
    path('rewards/claim/cancel/<int:pk>', views.claim_cancel, name='cancel_claim' ), 
    # Waste Containers
    path('rewards/containers/list', views.WasteContainerListView.as_view(), name='list_container' ),
    path('rewards/containers/create', views.WasteContainerCreateView.as_view(), name='create_container' ),
    path('rewards/containers/update/<int:pk>', views.WasteContainerUpdateView.as_view(), name='update_container' ),
    # Users
    path('users/list', views.UserListView.as_view(), name='list_user' ),
    # Entrenamiento  train_model_view(
    path('train-model/', views.train_model_view, name='train_model' ),
]