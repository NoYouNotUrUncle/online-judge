import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0121_per_problem_sub_access_control'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_banned_problem_voting',
            field=models.BooleanField(default=False,
                                      help_text="User will not be able to vote on problems' point values.",
                                      verbose_name='banned from voting'),
        ),
        migrations.CreateModel(
            name='ProblemPointsVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(help_text='The amount of points you think this problem deserves.',
                                               validators=[django.core.validators.MinValueValidator(1),
                                                           django.core.validators.MaxValueValidator(50)],
                                               verbose_name='How much this vote is worth')),
                ('note', models.TextField(blank=True, default='', help_text='Justification for problem points value.',
                                          max_length=2048, verbose_name='note to go along with vote')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='problem_points_votes', to='judge.Problem')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                            related_name='problem_points_votes', to='judge.Profile')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
    ]
