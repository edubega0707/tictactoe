from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
#Q es una libreria que permite realizar consultas con logica
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.

GAME_STATUS_CHOICES=(
 ('F', 'First Player To Move'),
 ('S', 'Second Player To Move'),
 ('W','First Player Wins'),
 ('L','Second Player Wins'),
 ('D','Draw')
)

class GamesQuerySet(models.QuerySet):
    def games_for_user(self,user):
        return self.filter(
            Q(first_player=user)| Q(second_player=user)
        )
    def active(self):
        return self.filter(
            Q(status='F')|Q(status='S')
        )



class Game(models.Model):
 first_player=models.ForeignKey(User, related_name="games_firts_player")
 second_player=models.ForeignKey(User, related_name="games_second_player")

 start_time=models.DateTimeField(auto_now_add=True)
 last_activate=models.DateTimeField(auto_now=True)
 status=models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)
 objects=GamesQuerySet.as_manager()

 def __str__(self):
  return "{0}vs{1}".format(
   self.first_player, self.second_player)


class Move(models.Model):
 x=models.IntegerField()
 y=models.IntegerField()
 comment=models.CharField(max_length=300, blank=True)
 by_firt_player=models.BooleanField()

 game=models.ForeignKey(Game, on_delete=models.CASCADE)