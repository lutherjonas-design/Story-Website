from django.contrib import admin
from .models import Stories, Chapters, Paragraphs, WordsToAdd

admin.site.register(Stories)
admin.site.register(Chapters)
admin.site.register(Paragraphs)
@admin.register(WordsToAdd)
class WordsToAddAdmin(admin.ModelAdmin):
    # Show both word and frequency in the list view
    list_display = ("word", "frequency")

    # Do not make any column link to the change form
    list_display_links = None

    # Safety: even if someone hits the change URL directly, don't allow edits
    def has_change_permission(self, request, obj=None):
        # No editing existing objects
        return False

    def has_add_permission(self, request):
        # Allow adding
        return True

    def has_delete_permission(self, request, obj=None):
        # Allow deleting (single or bulk)
        return True

    def has_view_permission(self, request, obj=None):
        # Ensure users can see the list page and details without change perms
        return True

    # Optional: If you still want a detail page but read-only fields there
    # (this will only be reachable if you re-enable links or direct URL)
    def get_readonly_fields(self, request, obj=None):
        # Make every field read-only if an object exists (i.e., on change view)
        if obj:
            return [f.name for f in obj._meta.fields]
        return super().get_readonly_fields(request, obj)
