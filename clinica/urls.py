from django.urls import path, include
from .views import TurnoCreate, TurnoDelete, TurnoUpdate, PacienteCreate, PacienteDelete, PacienteUpdate, TurnosYearArchiveView, TurnosMonthArchiveView, TurnosDayArchiveView, TurnosListView
from django.contrib.auth.decorators import login_required
from . import views
from .models import Turnos
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView

app_name= "clinica"
urlpatterns = [
    path('', views.index, name="index"),
    path('error',  views.error, name="error"),
    path('productos',  views.productos, name="productos"),
    path('productos/<int:producto_id>',  views.producto, name="producto"),
    path('productos/agregar',  views.agregar, name="agregar"),
    path('productos/eliminar/<int:producto_id>',  views.eliminar, name="eliminar"),
    path('productos/actualizar/<int:producto_id>',  views.actualizar, name="actualizar"),
    path('pacientes',  views.pacientes, name="pacientes"),

    path('historial/<int:paciente_id>',  views.historial, name="historial"),
    path('historial/agregar_consulta',  views.agregar_consulta, name="agregar_consulta"),
    path('historial/eliminar_consulta/<int:consulta_id>',  views.eliminar_consulta, name="eliminar_consulta"),
    path('historial/modificar_consulta/<int:consulta_id>',  views.modificar_consulta, name="modificar_consulta"),

    
    path('pedidos',  views.pedidos, name="pedidos"),
    path('pedidos/<int:pedido_id>', views.pedido, name="pedido"),
    path('pedidos/estado/<int:pedido_id>',  views.cambioDeEstado, name="cambioDeEstado"),
    path('pedidos/agregar',  views.agregar_pedido, name="agregar_pedido"),
    path('pedidos/eliminar/<int:pedido_id>',  views.eliminar_pedido, name="eliminar_pedido"),
    path('pedidos/actualizar/<int:pedido_id>',  views.actualizar_pedido, name="actualizar_pedido"),
    path('pedidos/pedido_items/<int:pedido_id>/', views.pedido_items, name="pedido_items"),    
    path('pedidos/pedido_items/<int:pedido_id>/agregar_item', views.agregar_item, name="agregar_item"),
    path('pedidos/detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name="detalle_pedido"),
    path('pedidos/agregar_producto/<int:pedido_id>/', views.agregar_producto, name="agregar_producto"),
    path('pedidos/eliminar_producto/<int:detalle_pedido_id>/', views.eliminar_producto, name="eliminar_producto"),
    path('pedidos/reportePacientePedido', views.reportePacientePedido, name="reportePacientePedido"),
    path('pedidos/reportePacientePedido/<int:filtro>/', views.reportePacientePedido, name="reportePacientePedido"),
    path('pedidos/productoMasVendidos/', views.productoMasVendidos, name="productoMasVendidos"),
    path('pedidos/reporteVentas/<int:anio>/', views.reporteVentas, name="reporteVentas"),
    path('pedidos/reporteVentasAnual/', views.reporteVentas, name="reporteVentasAnual"),

#  viaje de seba con los generic views 
    path('turnos/', TurnosListView.as_view(), name="turnos"),
    path('turnos/<int:pk>', views.TurnoDetailView.as_view(), name='turnos-detail'),
    path('turnos/create/', TurnoCreate.as_view(), name='turno-create'),
    path('turnos/<int:pk>/update/', TurnoUpdate.as_view(), name='turno-update'),
    path('turnos/<int:pk>/delete/', TurnoDelete.as_view(), name='turno-delete'),
    path('turnos/reporte',  views.turnos_reporte, name="turnos_reporte"),
    path('pacientes/reporte_asistencia',  views.reporte_asistencia, name="reporte_asistencia"),

    ################################################################### Turnos
    #path ('turnos',views.turnos, name="turnos"),
    path('turnos/crear', views.crearTurno , name = "crearTurno"),
    path('turnos/actualizar/<int:turno_id>', views.actualizarTurno, name = "actualizarTurno"),
    path('turnos/eliminar/<int:turno_id', views.borrarTurno, name ="borrarTurno"),

    ##################################################################
    path('pacientes/create', views.PacienteCreate, name='paciente_create'),
	path('pacientes/update/<int:pk>', views.PacienteUpdate.as_view(), name='paciente_update'),
	path('pacientes/delete/<int:pk>', views.PacienteDelete.as_view(), name='paciente_delete'),
    path('pacientes/<int:pk>', views.PacienteDetailView.as_view(), name='pacientes-detail'),

    path('turnos_archivo/<int:year>/', TurnosYearArchiveView.as_view(), name="turnos_year_archive"),
        # Example: /2012/08/
    path('turnos_archivo/<int:year>/<int:month>/', TurnosMonthArchiveView.as_view(month_format='%m'), name="turnos_month_numeric"),
    # Example: /2012/aug/
    path('turnos_archivo/<int:year>/<str:month>/', TurnosMonthArchiveView.as_view(), name="archive_month"),
    path('turnos_archivo/<int:year>/<str:month>/<int:day>/', TurnosDayArchiveView.as_view(), name="archive_day"),
#    path('observaciones/', views.ObservacionListView.as_view(), name='observacion-list'),
#    path('observacion/<int:pk>', views.ObservacionDetailView.as_view(), name='observacion-detail'),
#    path('observacion/create', views.ObservacionCreate.as_view(), name='observacion-create'),
#	path('observacion/update/<int:pk>', views.ObservacionUpdate.as_view(), name='observacion-update'),
#	path('observacion/delete/<int:pk>', views.ObservacionDelete.as_view(), name='observacion-delete'),
    # path('turnos/ver_consutla/<int:turno_id>', views.verConsulta, name= 'ver_consulta'),

]
