from django.contrib import admin

from accounts.models import LoginAudit

@admin.register(LoginAudit)
class LoginAuditAdmin(admin.ModelAdmin):
    model = LoginAudit
    list_display = [ 'NomeDeGuerra', 'CpfDoUsuario', 'ReUsuario','OpmCod', 'OpmCod1', 'OpmCod2','DataDoLogin','IpDoUsuario']  
    list_filter = ['OpmCod1',]
