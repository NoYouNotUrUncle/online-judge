from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext as _

from judge.models.problem import Problem
from judge.models.profile import Profile


class ProblemPointsVote(models.Model):
    points = models.FloatField(  # How much this vote is worth
        verbose_name=_('points'),
        help_text=_('The amount of points you think this problem deserves.'),
        validators=[
            MinValueValidator(settings.DMOJ_PROBLEM_MIN_USER_POINTS_VOTE),
            MaxValueValidator(settings.DMOJ_PROBLEM_MAX_USER_POINTS_VOTE),
        ],
    )
    # who voted
    voter = models.ForeignKey(Profile, related_name='problem_points_votes', on_delete=CASCADE, db_index=True)
    # what problem is this vote for
    problem = models.ForeignKey(Problem, related_name='problem_points_votes', on_delete=CASCADE, db_index=True)
    note = models.TextField(  # note to go along with vote
        verbose_name=_('note'),
        help_text=_('Justification for problem points value.'),
        max_length=2048,
        blank=True,
        default=' ',
    )

    # The name that shows up on the sidebar instead of the model class name
    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __str__(self):
        return f'{self.voter}: {self.points} for {self.problem.code} - "{self.note}"'
