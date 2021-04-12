from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _, pgettext, ungettext

from judge.models import ProblemPointsVote

from judge.utils.raw_sql import use_straight_join

class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem_code', 'problem_name', 'user_column')
    search_fields = ('problem__code', 'problem__name', 'user__user__username')

    def get_queryset(self, request):
        queryset = ProblemPointsVote.object.select_related('problem', 'user__user').only(
            'problem', 'voter', 'points', 'note'
        )
        use_straight_join(request)
        # subject to change, currently assume to give the queryset to people that has perms to edit the problems
        if not request.user.has_perm('judge.edit_all_problem'):
            id = request.profile.id
            queryset = queryset.filter(Q(problem__authors__id=id) | Q(problem__curators__id=id)).distinct()
        return queryset



    def problem_code(self, obj):
        return obj.problem.code
    problem_code.short_description = _('Problem code')
    problem_code.admin_order_field = 'problem__code'

    def problem_name(self, obj):
        return obj.problem.name
    problem_name.short_description = _('Problem name')
    problem_name.admin_order_field = 'problem__name'

    def user_column(self, obj):
        return obj.user.user.username
    user_column.admin_order_field = 'user__user__username'
    user_column.short_description = _('User')

    # need to look into to see if works
    def get_urls(self):
        return [
            url('r^(\d+)/judge/$', self.judge_view, name='judge_vote'),
        ] + super(VoteAdmin, self).get_urls()

    def judge_view(self, request, id):
        if not request.user.has_perm('judge.edit_own_problem') and not request.user.has_perm('judge.edit.all_problem'):
            raise PermissionDenied()

        # Not sure if I actually need to call this
        vote = get_object_or_404(ProblemPointsVote, id=id)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

