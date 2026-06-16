from django import forms

from clientes.models import Cliente


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "email", "telefone", "cpf", "endereco"]
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Nome completo"}),
            "email": forms.EmailInput(attrs={"placeholder": "email@exemplo.com"}),
            "telefone": forms.TextInput(attrs={"placeholder": "(00) 00000-0000"}),
            "cpf": forms.TextInput(attrs={"placeholder": "CPF opcional"}),
            "endereco": forms.Textarea(attrs={"placeholder": "Endereço completo para entrega", "rows": 4}),
        }
