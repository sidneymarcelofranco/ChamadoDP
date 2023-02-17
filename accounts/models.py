from django.db import models

class LoginAudit(models.Model):

    NomeDeGuerra = models.CharField(
        'Nome de Guerra',
        max_length=60,
        null=True, blank=True
    )

    CpfDoUsuario = models.CharField(
        'CPF', max_length=11,
        null=True, blank=True,
        db_index=True
    )

    PostoGraduacao = models.CharField(
        'Nome de Guerra',
        max_length=60,
        null=True, blank=True
    )

    ReUsuario = models.CharField(
        'Nome de Guerra',
        max_length=60,
        null=True, blank=True
    )

    OpmCod = models.CharField(
        'Código de OPM',
        max_length=60,
        null=True, blank=True
    )

    OpmCod1 = models.CharField(
        'Código de OPM1',
        max_length=60,
        null=True, blank=True
    )

    OpmCod2 = models.CharField(
        'Código de OPM2',
        max_length=60,
        null=True, blank=True
    )

    OpmCod3 = models.CharField(
        'Código de OPM3',
        max_length=60,
        null=True, blank=True
    )

    OpmCod4 = models.CharField(
        'Código de OPM4',
        max_length=60,
        null=True, blank=True
    )

    OpmCod5 = models.CharField(
        'Código de OPM5',
        max_length=60,
        null=True, blank=True
    )

    DataDoLogin = models.DateTimeField(
        'Login em:',
        auto_now_add=True,
        auto_now=False,
        editable=False
    )
    
    IpDoUsuario = models.CharField(
        'IP do Usuário',
        max_length=60,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ("Auditoria de login")
        verbose_name_plural = ("Auditoria de logins")

    def __str__(self):
        return self.NomeDeGuerra
