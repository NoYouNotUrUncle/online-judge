from django.contrib import admin


class VoteAdmin(admin.ModelAdmin):
    list_display = ('points', 'voter', 'problem', 'note')
    search_fields = ('voter', 'problem')

    # if the user has edit all problem or edit own problem perms, so curators authors and superusers
    def has_change_permission(self, request, obj=None):
        if not request.user.has_perm('judge.edit_own_problem'):
            return False
        if request.user.has_perm('judge.edit_all_problem') or obj is None:
            return True
        return obj.problem.is_editor(request.profile)

    def lookup_allowed(self, key, value):
        return super(VoteAdmin, self).lookup_allowed(key, value) or key in ('problem__code',)
