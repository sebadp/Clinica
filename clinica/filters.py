from .models import Turnos, Paciente
import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ModelChoiceFilter
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput


class TurnosFilter(django_filters.FilterSet):

    Anio = django_filters.NumberFilter(field_name="FechaTurno", lookup_expr='year')
    Mes = django_filters.NumberFilter(field_name="FechaTurno", lookup_expr='month')
    Dia = django_filters.NumberFilter(field_name="FechaTurno", lookup_expr='day')
    Paciente = ModelChoiceFilter(queryset=Paciente.objects.filter(medico=2))


    class Meta:
        model = Turnos
        fields = [ 'Anio', 'Mes', 'Dia']
        widgets = {
            'Anio' : DatePickerInput(),
            'Mes' : DatePickerInput(),
            'Dia' : DatePickerInput(),

        }



class ReporteFilter(django_filters.FilterSet):


    start_date = DateFilter(field_name="FechaTurno", label=("Fecha desde"), lookup_expr='gte')
    end_date = DateFilter(field_name="FechaTurno", label=("Fecha hasta"), lookup_expr='lte')
    class Meta:
        model = Turnos
        fields = ['Paciente', 'Asistencia', 'start_date', 'end_date']
        widgets = {
            'start_date' : DatePickerInput(),
            'end_date' : DatePickerInput(),
        }


# class ObservacionFilter(django_filters.FilterSet):
#     fecha = DateFilter(field_name="Fecha", lookup_expr='gte')

#     class Meta:
#         model = Observacion
#         fields = ['Paciente', 'Fecha']
#         widgets = {
#             'fecha' : DatePickerInput(),

#         }