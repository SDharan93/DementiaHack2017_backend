from django.db import models


# Move the models to separate files one day...
class Instructions(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True),
    Author = models.CharField(max_length=255, default=""), # Make this a user reference one day...
    intentID = models.CharField(max_length=255),


class Steps(models.Model):
    title = models.CharField(max_length=255),
    message = models.CharField(max_length=255),
    failureCount = models.IntegerField(default=0)
    media = models.ForeignKey(Instructions, related_name='media')


# Used to control possible assets
class Media(models.Model):
    audio = models.CharField(max_length=255, default=""),
    video = models.CharField(max_length=255, default=""),
    picture = models.CharField(max_length=255, default="")
    step = models.ForeignKey(Steps, related_name='step')


# Possible action types. Used to determine the type of question the user is asking
ACTION_CHOICES = (
    ('chef', 'recipeRecommendation'),
)


class Action(models.Model):
    actionType = models.CharField(max_length=50, choices=ACTION_CHOICES),
    title = models.CharField(max_length=255)
