from django import forms
from .models import Producto, Consulta, Pedido, PedidoDetalle, Turnos, Paciente
from usuarios.models import User
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class ProductoCreate(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


class TurnosCreate(forms.ModelForm):
    class Meta:
        model = Turnos
        fields = ['Paciente', 'FechaTurno', 'HoraTurno', 'Asistencia']


class ConsultaCreate(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'motivo', 'diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'fecha': DatePickerInput(format='%d/%m/%Y'),
        }


class PedidoCreate(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        # para la creación no se necesitan
        exclude = ('vendedor', 'estado', 'subtotal', 'fecha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PedidoView(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendedor'].disabled = True
        self.fields['paciente'].disabled = True
        self.fields['tipo_pago'].disabled = True
        self.fields['subtotal'].disabled = True
        self.fields['fecha'].disabled = True


class PedidoUpdate(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

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
            'FechaTurno': DatePickerInput(format='%d/%m/%Y'),
            'HoraTurno': TimePickerInput(),
        }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['medico'].queryset = User.objects.filter(es_medico=True)
