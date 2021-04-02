from django.db import models
from django.db.models import CASCADE
from judge.models.profile import Profile
from judge.models.problem import Problem
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

class ProblemPointsVote(models.Model):
    points = models.FloatField( #How much this vote is worth
        verbose_name="points",
        help_text="The amount of points you think this problem deserves.",
        validators=[MinValueValidator(settings.DMOJ_PROBLEM_MIN_PROBLEM_POINTS)]
    )
    #who voted
    voter = models.ForeignKey(Profile, related_name="problem_points_votes", on_delete=CASCADE)
    #what problem is this vote for
    problem = models.ForeignKey(Problem, related_name="problem_points_votes", on_delete=CASCADE)
    note = models.TextField( #note to go along with vote
        verbose_name="note",
        help_text="Justification for problem points value.",
        max_length=2048
    )

    def __str__(self):
        return str(self.voter)+": "+str(self.points)+" for "+str(self.problem.code)+" - \""+str(self.note)+"\""