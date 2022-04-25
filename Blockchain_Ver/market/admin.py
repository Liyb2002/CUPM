from os import close
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from django.db.models import query

from .models import *

from .blockchain import *

# from web3 import Web3
import time


class TeamGameAdmin(admin.ModelAdmin):
    list_display = ['desciptin', 'activated', 'game_end', 'game_time', 'game_close_time']
    ordering = ['game_time']
    actions = ['activate', 'end', 'resolve_home_win', 'resolve_away_win', 'recover']

    @admin.action(description='activate the market pool')
    def activate(self, request, queryset):
        print('DEBUG: creating market in admin')
        w3 = getWeb3()
        users = User.objects.all()
        participants_list = [account_admin]
        # participants_list = [user.username for user in users if not user.is_superuser]
        for obj in queryset:
            question_id = obj.id
            market_conf = activate_market(w3, question_id, 2, participants_list)
            lmsrMarketMaker_contract = market_conf['lmsrmm_contract']
            obj.contract_address = market_conf['lmsrAddress']
            obj.contract_abi = lmsrMarketMaker_contract.abi
            obj.condition_id = Web3.toHex(market_conf['conditionId'])
            obj.positionIdLo = market_conf['positionIdLo']
            obj.positionIdHi = market_conf['positionIdHi']
            obj.save()
        queryset.update(activated=True)
    
    @admin.action(description='market the game as ended')
    def end(self, request, queryset):
        w3 = getWeb3()
        contracts = loadContracts(w3)
        abi = contracts['lmsrmm_contract'].abi
        for obj in queryset:
            if not obj.resolved:
                gameAddress = obj.contract_address
                # print('closing market')
                # close_market(w3, gameAddress, abi)
                # queryset.update(winner="away")
                # queryset.update(resolved=True)
                queryset.update(game_end=True)


    @admin.action(description='resolve market: Home team win.')
    def resolve_home_win(self, request, queryset):
        payouts = [1, 0]
        w3 = getWeb3()
        contracts = loadContracts(w3)
        ConditionalTokens = contracts["ConditionalTokens_py"]
        abi = contracts['lmsrmm_contract'].abi
        for obj in queryset:
            if not obj.resolved:
                gameAddress = obj.contract_address
                gameAbi = abi
                question_id = obj.id
                # closing the market
                # close_market(w3, gameAddress, gameAbi)
                # report payout
                # report_payout(w3, ConditionalTokens, question_id, payouts)
                # time.sleep(20)
                # print('market closed. Reporting payout')
                # time.sleep(60)
                print('Payout reported. ')
                queryset.update(winner="home")
                queryset.update(resolved=True)
                queryset.update(game_end=True)
    
    @admin.action(description='resolve market: Away team win.')
    def resolve_away_win(self, request, queryset):
        payouts = [0, 1]
        w3 = getWeb3()
        contracts = loadContracts(w3)
        ConditionalTokens = contracts["ConditionalTokens_py"]
        abi = contracts['lmsrmm_contract'].abi
        for obj in queryset:
            if not obj.resolved:
                gameAddress = obj.contract_address
                gameAbi = obj.contract_abi
                question_id = obj.id

                # condition_id = obj.condition_id
                # print('check conditino prepare')
                # print(ConditionalTokens.getOutcomeSlotCount(condition_id))
                # print(ConditionalTokens.payoutDenominator(condition_id))
                # print(ConditionalTokens.payoutNumerators(condition_id, 0))
                # closing the market
                # print('closing market')
                # close_market(w3, gameAddress, abi)
                # lmsrMarketMaker_contract = w3.eth.contract(address=gameAddress,abi=abi)
                # lmsrMarketMaker = MarketMakersRepo.MarketMakersRepo(w3, lmsrMarketMaker_contract)
                # print(lmsrMarketMaker.getAddress())
                # print(ConditionalTokens.getOutcomeSlotCount(condition_id))
                # report payout
                # print(Web3.keccak(question_id))
                # print(condition_id)
                # account_admin = '0x03abA998B8888A2F8bdA00e5ddb8d4a598Af69BF'
                # print(ConditionalTokens.getConditionId(account_admin, Web3.keccak(question_id), 2))
                # report_payout(w3, ConditionalTokens, question_id, payouts)
                print('market closed. Reporting payout')
                print('Payout reported. ')
                queryset.update(winner="away")
                queryset.update(resolved=True)
                queryset.update(game_end=True)

    @admin.action(description='recover')
    def recover(self, request, queryset):
        queryset.update(winner="home")
        queryset.update(resolved=False)
        queryset.update(game_end=False)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'game', 'created_on')
    list_filter = ('created_on', 'game')
    search_fields = ('name', 'body')

class UserAdmin(admin.ModelAdmin):
    actions = ['add_whitelist']

    @admin.action(description='add user to whitelist')
    def add_whitelist(self, request, queryset):
        w3 = getWeb3()
        contracts = loadContracts(w3)
        whitelist = contracts['whitelist_py']
        participants_list = []
        for obj in queryset:
            # add user to whitelist.
            participants_list.append(obj.username)
        print(participants_list)
        append_whitelist(whitelist, participants_list)


class CommentInline(admin.StackedInline):
    model = Comment

class ReputationInline(admin.StackedInline):
    model = User_Reputation

from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
class UserAdmin(AuthUserAdmin):
    inlines = [CommentInline, ReputationInline]

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)

admin.site.register(Reply)

admin.site.register(TeamGame, TeamGameAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Team)
admin.site.register(Sport)
admin.site.register(Trade)