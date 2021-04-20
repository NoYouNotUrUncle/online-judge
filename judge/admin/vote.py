from django.contrib import admin


class VoteAdmin(admin.ModelAdmin):
    list_display = ('points', 'voter', 'problem', 'note')
    search_fields = ('voter', 'problem')

    # if the user has edit all problem or other editing permissions, so superusers
    def has_change_permission(self, request, obj=None):
        if obj is None:
            return request.user.has_perm('judge.edit_own_problem')
        return obj.is_editable_by(request.user)

    def lookup_allowed(self, key, value):
        return super(VoteAdmin, self).lookup_allowed(key, value) or key in ('problem__code',)
