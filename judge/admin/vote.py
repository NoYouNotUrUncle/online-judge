from django.conf import settings
from django.conf.urls import url
from django.contrib import admin, messages
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


class VoteAdmin(admin.ModelAdmin):
    list_display = ('points', 'voter', 'problem', 'note')
    search_fields = ('voter', 'problem')

    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('judge.edit_own_problem'):
            return False
        if request.user.has_perm('judge.edit_all_problem') or obj is None:
            return True
        return obj.problem.is_editor(request.profile)


