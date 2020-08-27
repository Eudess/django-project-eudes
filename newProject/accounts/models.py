from django.db import models

class User(models.Model):
    email = models.CharField(verbose_name='E-mail', max_length=100, unique=True, primary_key=True)
    password = models.CharField(verbose_name='Password', max_length=100)
    name = models.CharField(verbose_name='Nome', max_length=100, blank=True)
    sobrenome = models.CharField(verbose_name='Sobrenome', max_length=100, blank=True)
    is_active = models.BooleanField(verbose_name='Está Ativo?', blank=True, default=True)
    is_trusty = models.BooleanField(verbose_name="Email Confirmado?", default=False)
    date_joined = models.DateTimeField(verbose_name='Data de Cadastro', auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user'
