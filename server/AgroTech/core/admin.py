# admin.py
from django.contrib import admin
from .models import CustomUser, Farmer, Organisation, KisanBima, Contract

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_farmer', 'is_organisation')

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'state', 'district', 'land_area')

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gstin', 'state')

@admin.register(KisanBima)
class KisanBimaAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'policy_no', 'aadhar_no', 'pan_no')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_id', 'date_created')
