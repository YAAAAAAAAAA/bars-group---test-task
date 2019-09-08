from django.contrib import admin
from .models import Planet, TestTrials, Questions, Sith


class PlanetModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class TestTrialsModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class QuestionsModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class SithModelAdmin(admin.ModelAdmin):

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Planet, PlanetModelAdmin)
admin.site.register(TestTrials, TestTrialsModelAdmin)
admin.site.register(Questions, QuestionsModelAdmin)
admin.site.register(Sith, SithModelAdmin)