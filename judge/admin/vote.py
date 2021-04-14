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
    list_display = ('points', 'voter', 'problem', 'note')
    search_fields = ('voter', 'problem')

    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('judge.edit_own_problem'):
            return False
        if request.user.has_perm('judge.edit_all_problem') or obj is None:
            return True
        return obj.problem.is_editor(request.profile)


    # finally works but doesnt load page
    def get_urls(self):
        return [
            url(r'^(\d+)/$', self.judge_view, name='judge_vote'),
        ] + super(VoteAdmin, self).get_urls()

    def judge_view(self, request, id):
        if not request.user.has_perm('judge.edit_own_problem') and not request.user.has_perm('judge.edit_all_problem'):
            raise PermissionDenied()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
