from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .models import Comment, Market, Reply, Sport, TeamGame, Trade, User_Market, User_Reputation
from .forms import UserForm, ProfileForm, ActionForm, CommentForm

from .blockchain import *

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('/market/')

    
def index(request):
    all_sport = Sport.objects.all()
    all_user = User.objects.filter(is_staff=False)
    template = loader.get_template('index.html')
    w3 = getWeb3()
    contracts = loadContracts(w3)
    csToken = contracts['csToken_py']
    sports_management = ['Jo', 'Sid', 'Julia', 'Sam', 'Yuanbo', 'Grant', 'Zifan', 'Tom', 'Yihui', 'Luke', 'Yash', 'Lj', 'Daniel', 'Max']
    usernames = [user.username for user in all_user if user.username[0] == '0' and user.first_name not in sports_management]
    firstnames = [user.first_name for user in all_user if user.username[0] == '0' and user.first_name not in sports_management]
    leaders = get_leaderboard(csToken, usernames, firstnames)
    context = {
        'all_sport': all_sport,
        'leaders': leaders
    }
    return HttpResponse(template.render(context, request))


def sport(request, sport_name):
    game_list = []
    template = loader.get_template('sport.html')
    current_user = request.user
    sport = Sport.objects.get(sport_name=sport_name)
    all_game = sport.games.all()
    # participated_game = User_Market.objects.filter(user = current_user)
    # participated_game = [g.game for g in participated_game if g.game.market == sport]
    # unparticipated_game = [g for g in all_game if g not in participated_game]
    # w3 = getWeb3()
    # contracts = loadContracts(w3)
    # csTokenAbi = contracts["csToken_contract"].abi
    # csTokenAddress =  contracts["csToken_contract"].address

    d = {False: 'Open', True: 'Closed'}

    for game in all_game:
        all_trade = Trade.objects.filter(game=game)
        my_trade = [t for t in all_trade if t.user == current_user]
        n_trade = len(my_trade)
        total_trade = all_trade.count()
        game_list.append([game.id, game.desciptin, game.game_close_time, d[game.game_end], n_trade, total_trade])

    context = {
        'sport_name' : sport_name,
        # 'participated_game': participated_game,
        # 'unparticipated_game': unparticipated_game,
        # 'csTokenAbi': csTokenAbi,
        # 'csTokenAddress': csTokenAddress,
        'game_list': game_list
    }
    return HttpResponse(template.render(context, request))

# Blockchain Specific
def game(request, sport_name, game_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    template = loader.get_template('game.html')
    action_form = ActionForm()

    w3 = getWeb3()
    contracts = loadContracts(w3)
    csTokenAbi = contracts["csToken_contract"].abi
    csTokenAddress = contracts["csToken_contract"].address 
    conditionalTokensAbi = contracts["ConditionalTokens_contract"].abi
    conditionalTokensAddress = contracts["ConditionalTokens_contract"].address
    address = game.contract_address
    abi = game.contract_abi
    conditionId = game.condition_id
    positionIdLo = game.positionIdLo
    positionIdHi = game.positionIdHi

    json_abi = contracts["lmsrmm_contract"].abi
    lmsrMarketMaker_contract = w3.eth.contract(address=address,abi=json_abi)
    lmsrMarketMaker = MarketMakersRepo.MarketMakersRepo(w3, lmsrMarketMaker_contract)
    probability0 = lmsrMarketMaker.calcMarginalPrice(0)
    probability1 = lmsrMarketMaker.calcMarginalPrice(1)
    
    pie_data = [float(probability0 / 100), float(probability1 / 100)]
    this_game_user = User_Market.objects.filter(game=game, user=current_user)
    if not this_game_user:
        this_game_user = User_Market(game=game, user=current_user)
        print('new user market created')
        this_game_user.save()

    ConditionalTokens = contracts['ConditionalTokens_py']
    u = Web3.toChecksumAddress(current_user.username)
    balance_lo = ConditionalTokens.balanceOf(u, int(positionIdLo))
    balance_hi = ConditionalTokens.balanceOf(u, int(positionIdHi))

    csToken = contracts['csToken_py']
    balance = csToken.balanceOf(u)

    position_data = [balance_lo, balance_hi]
    history = Trade.objects.filter(user=current_user, game=game)
    message = None

    if game.winner == 'home':
        winner = game.home
    else:
        winner = game.away


    comments = Comment.objects.filter(game=game)

    historical_price = []
    for t in game.trades.all():
        historical_price.append({'x': str(t.time.strftime('%Y-%m-%d %H:%M:%S')), 'value': float(t.market_price)})

    context = {
        'sport_name': sport_name,
        'game': game,
        'pie_data': pie_data,
        'pie_labels': [game.home.team_name, game.away.team_name],
        'position_data': position_data,
        'form': action_form,
        'has_histroy': len(history) != 0,
        'history':history,
        'has_message': message != None,
        'message': message,
        'marketAddress': address,
        'marketAbi': abi,
        'marketConditionId': conditionId,
        'csTokenAbi': csTokenAbi,
        'csTokenAddress': csTokenAddress,
        'conditionalTokensAbi': conditionalTokensAbi,
        'conditionalTokensAddress': conditionalTokensAddress,
        'home_position': balance_lo,
        'away_position': balance_hi,
        'balance': balance,
        'winner': winner,
        'positionIdLo': positionIdLo,
        'positionIdHi': positionIdHi,
        'comments': comments,
        'historical_price': historical_price
    }
    return HttpResponse(template.render(context, request))


def post_comment(request, sport_name, game_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    
    if request.method == 'POST':
        bodytxt = request.POST.get('bodytxt')
        if len(bodytxt) == 0:
            pass
        else:
            new_comment = Comment.objects.create(game=game, name=current_user, body=bodytxt)

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))


def reply_comment(request, sport_name, game_id, comment_id):
    current_user = request.user
    comment = Comment.objects.get(id=comment_id)
    
    if request.method == 'POST':
        bodytxt = request.POST.get('replytxt')
        if len(bodytxt) == 0:
            pass
        else:
            new_reply = Reply.objects.create(parent=comment, name=current_user, body=bodytxt)
            new_reply.save()

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))

def update_reputation(user, change):
    # try:
    #     obj = User_Reputation.objects.get(user=user)
    #     obj.ups = obj.ups + change[0]
    #     obj.downs = obj.downs + change[1]
    #     obj.save()
    # except User_Reputation.DoesNotExist:
    #     obj = User_Reputation.create(user=user, ups=change[0], downs=change[1])
    #     obj.save()
    return

def like_comment(request, game_id, comment_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    sport_name = game.market.sport_name
    comment = Comment.objects.get(id=comment_id)
    comment.likes.add(current_user)
    disliked = current_user in comment.dislikes.all()
    if disliked:
        comment.dislikes.remove(current_user)
        change = [1, -1]
    else:
        change = [1, 0]
    update_reputation(current_user, change)

    comment.save()

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))

def dislike_comment(request, game_id, comment_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    sport_name = game.market.sport_name
    comment = Comment.objects.get(id=comment_id)
    comment.dislikes.add(current_user)
    comment.save()
    liked = current_user in comment.likes.all()
    if liked:
        comment.likes.remove(current_user)
        change = [-1, 1]
    else:
        change = [0, 1]
    update_reputation(current_user, change)

    comment.save()

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))

def cancel_like_comment(request, game_id, comment_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    sport_name = game.market.sport_name
    comment = Comment.objects.get(id=comment_id)
    comment.likes.remove(current_user)
    change = [-1, 0]
    update_reputation(current_user, change)

    comment.save()

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))

def cancel_dislike_comment(request, game_id, comment_id):
    current_user = request.user
    game = TeamGame.objects.get(id=game_id)
    sport_name = game.market.sport_name
    comment = Comment.objects.get(id=comment_id)
    comment.dislikes.remove(current_user)
    change = [0, -1]
    update_reputation(current_user, change)

    comment.save()

    return redirect(reverse('game_page', kwargs={'sport_name':sport_name, 'game_id':game_id}))


@require_http_methods(["GET", "POST"])
def trade_success(request):
    current_user = request.user
    game_id = request.POST.get('game')
    game = TeamGame.objects.get(id=game_id)
    option = request.POST.get('option')
    side = request.POST.get('team')
    if side == '0':
        team = game.home
    else:
        team = game.away
    amount = request.POST.get('amount')
    time = datetime.now()
    Trade.objects.create(user=current_user, game=game, team = team, option=option, amount=amount, time=time)
    return

@require_http_methods(["GET", "POST"])
def redeem_success(request):
    current_user = request.user
    game_id = request.POST.get('game')
    game = TeamGame.objects.get(id=game_id)
    user_game = User_Market.get(user=current_user, game=game)
    user_game.redeemed = True
    user_game.save()
    return

@require_http_methods(["GET", "POST"])
def before_buy_complete(request):
    current_user = request.user
    game_id = request.POST.get('game')
    game = TeamGame.objects.get(id=game_id)
    user_game = User_Market.get(user=current_user, game=game)
    user_game.before_buy = True
    user_game.save()
    return

@require_http_methods(["GET", "POST"])
def before_sell_complete(request):
    current_user = request.user
    game_id = request.POST.get('game')
    game = TeamGame.objects.get(id=game_id)
    user_game = User_Market.get(user=current_user, game=game)
    user_game.before_sell = True
    user_game.save()
    return

@require_http_methods(["GET", "POST"])
def save_trade(request):
    current_user = request.user
    game_id = request.POST.get('game')
    game = TeamGame.objects.get(id=game_id)
    option = request.POST.get('option')
    side = request.POST.get('team')
    if side == '0':
        team = game.home
    else:
        team = game.away
    amount = request.POST.get('amount')
    time = datetime.now()
    # cost = request.POST.get('cost')

    # if option == 'Sell':
    #     cost = cost + 1
    # else:
    #     cost = cost - 1
    
    # market_price = cost / amount
    market_price = request.POST.get('mp')

    up = request.POST.get('up')
    down = request.POST.get('down')
    tx_receipt = request.POST.get('tx')
    Trade.objects.create(user=current_user, game=game, team = team, option=option, amount=amount, market_price = market_price, estimate_low = down, estimate_high = up, time=time, tx_receipt=tx_receipt)
    return
