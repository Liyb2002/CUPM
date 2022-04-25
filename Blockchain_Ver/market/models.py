from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Sport(models.Model):
    sport_name = models.CharField(max_length=100)
    def __str__(self):
        return self.sport_name

class Team(models.Model):
    team_name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    def __str__(self):
        return self.team_name

class Market(models.Model):
    name = models.CharField(max_length=50)
    desciptin = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class TeamGame(models.Model):
    home = models.ForeignKey(Team, related_name='home', on_delete=models.CASCADE)
    away = models.ForeignKey(Team, related_name='away', on_delete=models.CASCADE)
    market = models.ForeignKey(Sport, related_name='games', on_delete=models.CASCADE)
    desciptin = models.CharField(max_length=200)
    activated = models.BooleanField(default=False)
    game_day = models.DateField()
    game_time = models.DateTimeField()
    game_end = models.BooleanField(default=False)
    game_close_time = models.DateTimeField()
    pool_id = models.CharField(max_length=256, blank=True)
    market_conf = models.JSONField(default={'null':'null'})
    contract_address = models.CharField(max_length=200, default='need activating')
    contract_abi = models.TextField(default='need activating')
    condition_id = models.TextField(default='need activating')
    positionIdHi = models.TextField(default='need activating')
    positionIdLo = models.TextField(default='need activating')
    CHOICES = (('home', 'home'), ('away', 'away'))
    winner = models.CharField(max_length=4, choices=CHOICES, default='home')
    resolved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.desciptin
    def game_started(self):
        return self.game_time <= timezone.now()
    def activate(self):
        self.activated = True


# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     """Create a matching profile whenever a user object is created."""
#     if created: 
#         profile, new = UserProfile.objects.get_or_create(user=instance)


class Trade(models.Model):
    user = models.ForeignKey(User, related_name='trades', on_delete=models.CASCADE)
    game = models.ForeignKey(TeamGame, related_name='trades', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name='trades', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    CHOICES = (('Buy', 'Buy'), ('Sell', 'Sell'))
    option = models.CharField(max_length=5, choices=CHOICES)
    time = models.DateTimeField(auto_now=True)
    market_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.5)
    estimate_low = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    estimate_high = models.DecimalField(max_digits=10, decimal_places=3, default=1)
    tx_receipt = models.TextField(default='receipt of transaction')
    status = models.IntegerField(default=0)



class User_Market(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(TeamGame, related_name='game_user', on_delete=models.CASCADE)
    home_token = models.DecimalField(max_digits=20, decimal_places=4, default=50.0)
    away_token = models.DecimalField(max_digits=20, decimal_places=4, default=50.0)
    before_buy = models.BooleanField(default=False)
    before_sell = models.BooleanField(default=False)
    redeemed = models.BooleanField(default=False)


class Comment(models.Model):
    game = models.ForeignKey(TeamGame, on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name.username)

class Reply(models.Model):
    parent = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

class User_Reputation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)
    ups = models.IntegerField(default=0)
    downs = models.IntegerField(default=0)




class Profile(models.Model):
    '''
    User Profile. One user will only has one profile
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_address = models.CharField(max_length=256, blank=True)
    avatar = models.ImageField(upload_to='static/pictures/UserPhoto/',
                               default='static/pictures/UserPhoto/default-user.png')
    bio = models.TextField(max_length=500, blank=True)
    website = models.URLField(default='', blank=True)
    address = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorites = models.ManyToManyField(Team)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    '''
    Create user profile if user is created
    '''
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    '''
    Save user profile if there is any changes
    '''
    instance.profile.save()


