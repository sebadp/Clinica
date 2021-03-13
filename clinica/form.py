from django import forms
from .models import  Producto, Consulta, Pedido, PedidoDetalle, Turnos, Paciente
# from.models import Turnos
from usuarios.models import User
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
import django_filters

class ProductoCreate(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if (self.instance.tipo== 'L'):
    #         self.fields['enfoque'].disabled = False
    #         self.fields['lado'].disabled = False
    #         self.fields['armazon'].disabled = False
#_________________________________________________________________________________________     
class TurnosCreate(forms.ModelForm):
    class Meta:
        model = Turnos
        fields = ['Paciente', 'FechaTurno', 'HoraTurno', 'Asistencia']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['medico'].queryset = User.objects.filter(es_medico=True)

#________________________________________________________________________

class ConsultaCreate(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'motivo', 'diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'fecha' : DatePickerInput(format='%d/%m/%Y'),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['medico'].queryset = User.objects.filter(es_medico=True)

class PedidoCreate(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        # para la creación no se necesitan
        exclude=('vendedor', 'estado', 'subtotal', 'fecha')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['vendedor'].disabled = True
        # self.fields['subtotal'].disabled = True
        # self.fields['estado'].value = 'PT'
        # self.fields['estado'].disabled = True
        # self.fields['fecha'].disabled = True
        # self.fields['vendedor'].queryset = User.objects.filter(es_ventas=True)

class PedidoView(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendedor'].disabled = True
        self.fields['paciente'].disabled = True
        self.fields['tipo_pago'].disabled = True
        # self.fields['estado'].disabled = True
        self.fields['subtotal'].disabled = True
        self.fields['fecha'].disabled = True
    
class PedidoUpdate(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        # para update solo cambia el estado
        # exclude=('vendedor', 'paciente', 'tipo_pago', 'subtotal', 'fecha')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)               

class PedidoDetalleCreate(forms.ModelForm):
    class Meta:
        model = PedidoDetalle
        fields = ('producto', 'cantidad')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class Turno_Form(forms.ModelForm):
    class Meta:
        model = Turnos
        fields = ['Paciente', 'FechaTurno', 'HoraTurno', 'Asistencia']
        widgets = {
            'FechaTurno' : DatePickerInput(format='%d/%m/%Y'),
            'HoraTurno' : TimePickerInput(),
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        # exclude = ('medico',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = User.objects.filter(es_medico = True)


    # def get_form(self):
    #     form = super().get_form()
    #     self.fields['medico'].queryset = User.objects.filter(es_medico = True)
    #     return form

# class Observacion_Form(forms.ModelForm):
#     class Meta:
#         model = Observacion
#         fields = '__all__'
#         widgets = {
#             'Fecha' : DatePickerInput(format='%d/%m/%Y'),
#         }