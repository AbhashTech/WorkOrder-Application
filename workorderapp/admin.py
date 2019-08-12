from django.contrib import admin
from .models import Customer, Person, Domain, Workorder, Updates
from easy_select2 import select2_modelform, apply_select2


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('custname', 'custcontact', 'custemail', 'custisactive')
    list_display_links = ('custname',)
    list_editable = ('custcontact', 'custemail', 'custisactive')
    list_filter = ('custisactive',)
    search_fields = ('custname', 'custcontact', 'custemail', 'custaddress')


PersonfForm = select2_modelform(Person, attrs={'width': '400px'})


class PersonAdmin(admin.ModelAdmin):
    list_display = ('personname', 'personcontacttype', 'personcontact', 'personactive', 'personrefcustid',)
    list_display_links = ('personname',)
    list_editable = ('personcontact', 'personactive')
    list_filter = ('personactive',)
    search_fields = ('personname', 'personcontact',)
    form = PersonfForm


DomainAdminForm = select2_modelform(Domain, attrs={'width': '400px'})


class DomainAdmin(admin.ModelAdmin):
    list_display_links = ('domainaddress',)
    list_display = ('domainaddress', 'domainrefcustid')
    search_fields = ('domainaddress', )
    form = DomainAdminForm


class WorkorderAdmin(admin.ModelAdmin):
    form = select2_modelform(Workorder, attrs={'width': '600px'})
    search_fields = ('refdomainid__domainaddress',)
    list_display = ('workorder_number_list','domain_list', 'jobstatus')
    list_filter = ('jobstatus', 'worktype')


class UpdatesAdmin(admin.ModelAdmin):
    form = select2_modelform(Updates, attrs={'width': '600px'})
    search_fields = ('refdomainid__domainaddress',)
    list_display = ('updateid', 'refdomainid', 'work_order_status', 'refwoid')
    list_filter = ('refwoid__jobstatus',)

# Register your models here.
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Workorder, WorkorderAdmin)
admin.site.register(Updates, UpdatesAdmin)
admin.site.site_header = 'AbhashTech CRM Portal'
