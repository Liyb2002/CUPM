from django.http import HttpResponse
from django.template import context, loader

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader

from market.blockchain import *




def leaderboard(request):
    template = loader.get_template('leaderboard.html')
    all_user = User.objects.filter(is_staff=False)
    w3 = getWeb3()
    contracts = loadContracts(w3)
    csToken = contracts['csToken_py']
    sport_management = ['0x80D1429B0DAf2f893Ac8AeEBA0CE7ac25Baa13fa', '0x9593C62eBc67A4b5Ed5C751D80064bC9e9d916f7','0xB2051DC42dCbB8835a3d806527b26715d4A1d343','0x044ABeBbe4f157df44AcA451CbaA3256C748B3c4','0x22198052Ee473fbE80CeBEFA422974Af56669ee3','0x59Efef7fbFa4c8C2617D39495DB59cacb22b329c','0x62C25d0284e59D856DB60Db2f665f4954F53F4ad','0xeCA86340E2E4aA3fdAE65Bde65CCAD36A017296A','0x862aB6d42a841A3A5041F09985Dce51f00a50447', '0xa503e4929D2C9D6b20f60EE77247209b8dEa1259', '0x6573a4beaB481D3b9932718d0f1B4AAe5e32C5A3', '0x1DbcFFE055602fc488395d69D01c63bfd266742e', '0x2C35c36cF2C265f1F596438a0D7661278d6628BA', '0xA46A617187c97E22EE3D4D6E29c2846EA4aa285D', '0xa006692006545b5ec7fa7455a3df5d13bfb07fb8', '0xdd90b23d1d0fb300e212efc16f5214ee1451d5e9', '0x0f0c319ea6b6ac93e49fc03ab40c420fd5450cfc']
    block_users = ['0x5F1f5942a0235d6838922405387061a4d5796dd0' ,'0xe06A0ff2cB2f2D93EEb9Ae6364E8ADd63b4Dea2e' ,'0x5b23CcD374D84bCB1154c06fb962CA09d5E8Ef41','0x62f7aA1937A38411d239C261d3f55e74EE1518aE' , '0x7b5d4F37b38cb3f9d9F491a41e57aDcb576F5a1D', '0x923D99Db4aDde8f529C0cc391E683ba1c81D2230',  '0xc92b638b41634037BE16524E8B28597388e6c9b0', '0x1E7A34BcfD1ceC6A2072b3f6361953f4fAeD98E9', '0x1b4abFf8b7eA7328C57F6c1933513eE845a65DA7', '0x005488616CBc846a12a177f028AD7a6D927Be6F5', '0x9B960a8Eea781557b80C86797DcCE2514068A7b2', '0xE421dBC4f259D8a7b127a111A2CD3b6a0E1b76F7', '0x8DA7CA6dD81D6aF38023444d1cA30b69B3f662ba', '0xAe9FC78FdF4F15929F59d6B9a45B5674a82C3843','0x8c97cAb392f8fdE18398197837c1De4beA055365', '0xeca235C88f65633f334D2a12Fbc1E2beBaA65cad','0xb944F86123739E5e148002D188bC58867251961c', '0xaB3258b5Eb6A643AE772EC7f11d3AA8747701E3A','0x69569aE60C531CA68fF1d098e71054B439fa2d2a','0x19813F963674F02b10513ECA6c9cF838D94468fF','0x00AFa2135D21C473a83E5B2D5ace1fE23391D606', '0xEA699d1b67407E4257c192c2b2A4DAe559c25821', '0xaaf26Ca4Ee6aF18DA2E3CCFe0C8689Cad0eA608d', '0xAe9FC78FdF4F15929F59d6B9a45B5674a82C3843']
    sport_management = [s.lower() for s in sport_management]
    block_users = [s.lower() for s in block_users]
    block_usernames = [user.username for user in all_user if user.username in block_users]
    block_firstnames = [user.first_name for user in all_user if user.username in block_usernames]
    sport_usernames = [user.username for user in all_user if user.username in sport_management]
    sport_firstnames = [user.first_name for user in all_user if user.username in sport_usernames]
    sportleaders = get_leaderboard(csToken, sport_usernames, sport_firstnames)
    blockleaders = get_leaderboard(csToken, block_usernames, block_firstnames)
    context = {
        'sportleaders': sportleaders,
        'blockleaders': blockleaders,
    }
    return HttpResponse(template.render(context, request))
    
def index(request):
    template = loader.get_template('columbia.html')
    context = {}
    return HttpResponse(template.render(context, request))