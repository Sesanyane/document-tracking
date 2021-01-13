from django.contrib import admin
from django.contrib.auth import get_user
from django.contrib.auth.models import User

from edc_model_admin import audit_fieldset_tuple

from ..admin_site import document_tracking_admin
from ..forms import CourierForm, SendDocumentForm
from ..models import Courier, SendDocument

from .modeladmin_mixins import ModelAdminMixin

from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter


@admin.register(Courier, site=document_tracking_admin)
class CourierAdmin(
        ModelAdminMixin, admin.ModelAdmin):

    form = CourierForm

    fieldsets = (
        (None, {
            'fields': (
                'full_name',
                'cell',
                'email',
            )}),
        audit_fieldset_tuple)

    search_fields = ['full_name', 'cell', 'email',]


@admin.register(SendDocument, site=document_tracking_admin)
class SendDocumentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SendDocumentForm
    search_fields = ['doc_identifier']

    fieldsets = (
        (None, {
            'fields': (
                'doc_identifier',
                'department',
                'send_to',
                'status',
                'priority',
                'comment',
                'action_date',
                'group',)}),
        ('If Document is Hard Copy', {
            'fields': ('courier',
                       'receiver_at_destination',
                       'final_destination')}),
        audit_fieldset_tuple)

    radio_fields = {
        # "department": admin.VERTICAL,
        "status": admin.VERTICAL,
        "priority": admin.VERTICAL,
    }

    # autocomplete_fields = ['department']

    filter_horizontal = ('group', 'department', 'send_to',
                         'receiver_at_destination', 'final_destination')

    list_filter = (
        ('department', RelatedDropdownFilter),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(SendDocumentAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form

    # def get_readonly_fields(self, request, obj=None):
    #     fields = super().get_readonly_fields(request, obj)
    #     # username = None
    #     if request.user.is_authenticated:
    #         user_created = obj.user_created if obj else None
    #         # username = SendDocument.objects.get()
    #         if user_created and user_created == get_user(request).username:
    #             fields = ('status', ) + fields
    #         else:
    #             fields = ('department', 'send_to', 'priority', 'comment',
    #                       'action_date', 'group', 'courier', 'doc_identifier',
    #                       'receiver_at_destination', 'final_destination') \
    #                      + fields
    #     return fields
