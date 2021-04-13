from django.db import models
from django.db.models import CASCADE
from judge.models.profile import Profile
from judge.models.problem import Problem
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class ProblemPointsVote(models.Model):
    points = models.FloatField( #How much this vote is worth
        verbose_name='points',
        help_text='The amount of points you think this problem deserves.',
        validators=[
            MinValueValidator(settings.DMOJ_PROBLEM_MIN_USER_POINTS_VOTE),
            MaxValueValidator(settings.DMOJ_PROBLEM_MAX_USER_POINTS_VOTE),
        ],
    )
    #who voted
    voter = models.ForeignKey(Profile, related_name='problem_points_votes', on_delete=CASCADE, db_index=True)
    #what problem is this vote for
    problem = models.ForeignKey(Problem, related_name='problem_points_votes', on_delete=CASCADE, db_index=True)
    note = models.TextField( #note to go along with vote
        verbose_name='note',
        help_text='Justification for problem points value.',
        max_length=2048,
        required=False,
    )

    def __str__(self):
        return f'{self.voter}: {self.points} for {self.problem.code} - "{self.note}"'
