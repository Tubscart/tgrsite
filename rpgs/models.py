from django.db import models
from django.shortcuts import reverse

from users.models import Member


# Create your models here.
class Rpg(models.Model):
    game_masters = models.ManyToManyField(Member, related_name='rpgs_running', blank=True,
                                          help_text="Who is actually running the event")
    title = models.CharField(max_length=64, verbose_name='Name', help_text="The event's name")
    system = models.CharField(max_length=64, blank=True, help_text="The system that is being used")
    description = models.TextField(max_length=8192, blank=True, help_text="Longform description")
    time_slot = models.CharField(max_length=64, blank=True, help_text="The date/time(s) this event will occur")
    location = models.CharField(max_length=64, blank=True, help_text="The location where this event will occur")
    players_wanted = models.IntegerField()
    is_in_the_past = models.BooleanField(default=False, help_text="Has the event already happened?")

    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False, help_text='Pin this event to the top of the list')
    unlisted = models.BooleanField(default=False, help_text='Prevent this from appearing on the events listing')
    creator = models.ForeignKey(Member, related_name='rpgs_owned', on_delete=models.PROTECT,
                                help_text="The creator of this event")
    members = models.ManyToManyField(Member, blank=True, help_text="The people playing the game")
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title

    def tags_str(self):
        return ', '.join([str(x) for x in self.tags.all()])

    def get_absolute_url(self):
        return reverse("rpgs:detail", args=[self.pk])


class Tag(models.Model):
    name = models.CharField(max_length=72)

    def __str__(self):
        return self.name
