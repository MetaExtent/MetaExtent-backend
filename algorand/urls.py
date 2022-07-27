from django.urls import path

from . import views
from . import marketplaceViews
from . import auctionViews
from . import lendingViews
urlpatterns = [
    path('swap', views.index, name='index'),
    path('optin', views.optin, name='optin'),
    path('checkOptin', views.checkOptin, name='checkOptin'),
    path('checkAssetOptin', views.checkAssetOptin, name='checkAssetOptin'),
    path('accountInfo', views.accountInfo, name='accountInfo'),
    path('poolInfo', views.poolInfo, name='poolInfo'),
    path('swapInfo', views.swapInfo, name='swapInfo'),
    path('showPK', views.showPK, name='showPK'),
    path('createAsset', views.createAsset, name='createAsset'),
    path('createPool', views.createPool, name='createPool'),
    path('addLiquidity', views.addLiquidity, name='addLiquidity'),
    path('getProgram', views.getProgramByte, name='getProgramByte'),
    path('bootstrapInfo', views.bootstrapInfo, name='bootstrapInfo'),
    path('marketplace', marketplaceViews.marketplace, name='marketplace'),
    path('escrow_program', marketplaceViews.escrow_program, name='escrow_program'),
    path('pending_transaction_info', marketplaceViews.pending_transaction_info, name='pending_transaction_info'),
    path('decodeAddress', marketplaceViews.decodeAddress, name='decodeAddress'),
    path('logicSigInfo', marketplaceViews.logicSigInfo, name='logicSigInfo'),
    path('auctionProgram', auctionViews.auctionProgram, name='auctionProgram'),
    path('lendingProgram', lendingViews.lendingProgram, name='lendingProgram'),

]