from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .form import (
    ProductoCreate,
    PedidoCreate,
    PedidoDetalleCreate,
    PedidoUpdate,
    PedidoView,
    ConsultaCreate,
    TurnosCreate,
    PacienteForm,
)
from .models import Producto, Paciente, Consulta, Pedido, PedidoDetalle, Turnos, User
from .form import (
    ProductoCreate,
    PedidoCreate,
    PedidoDetalleCreate,
    PedidoUpdate,
    PedidoView,
    ConsultaCreate,
    TurnosCreate,
    Turno_Form,
)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from django import forms
from django.db.models import Count, QuerySet
from django.contrib.auth import get_user_model
import operator


import django_filters
from .filters import TurnosFilter, ReporteFilter
import datetime
from django.contrib.auth.decorators import login_required

from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView

from django.contrib.auth.mixins import LoginRequiredMixin

# from .models import Turnos
# from .form import TurnosCreate

# Create your views here.


def index(request):
    # De acuerdo al perfil debemos redeireccionarlo
    return render(request, "index.html")


def error(request, mensaje):
    # De acuerdo al perfil debemos redeireccionarlo
    return render(request, "error.html", {"mensaje": mensaje})


@login_required
def productos(request):
    if request.user.is_staff:
        return render(request, "productos.html", {"productos": Producto.objects.all()})
    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def producto(request, producto_id):
    if request.user.is_staff:
        unProducto = Producto.objects.get(id=producto_id)
        return render(request, "producto.html", {"producto": unProducto})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def agregar(request):
    if request.user.is_staff:
        upload = ProductoCreate()
        if request.method == "POST":
            upload = ProductoCreate(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                return redirect("clinica:productos")
            else:
                return HttpResponse(
                    """your form is wrong, reload on <a href = "{{ url : 'clinica:productos'}}">reload</a>"""
                )
        else:
            return render(request, "agregar.html", {"upload_form": upload})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def eliminar(request, producto_id):
    if request.user.is_staff:
        producto_id = int(producto_id)
        try:
            producto_sel = Producto.objects.get(id=producto_id)

        except Producto.DoesNotExist:
            return redirect("clinica:productos")
        producto_sel.delete()
        return render(request, "eliminar.html")

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def actualizar(request, producto_id):
    if request.user.is_staff:
        producto_id = int(producto_id)
        try:
            producto_sel = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return redirect("index")
        producto_form = ProductoCreate(request.POST or None, instance=producto_sel)
        if producto_form.is_valid():
            producto_form.save()
            return redirect("clinica:productos")
        return render(request, "agregar.html", {"upload_form": producto_form})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


####################################################################################################

def turnos(request):
    return render(request, "turnos.html", {"turno": Turnos.objects.all()})


def crearTurno(request):
    upload = TurnosCreate()
    if request.method == "POST":
        upload = TurnosCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect("clinica:turnos")
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : 'clinica:turnos'}}">reload</a>"""
            )
    else:
        return render(request, "agregarturno.html", {"upload_form": upload})


def borrarTurno(request, turno_id):
    turno_id = int(turno_id)
    try:
        turno_elegido = Turnos.objects.get(id=turno_id)

    except Turnos.DoesNotExist:
        return redirect("clinica:turnos")
    turno_elegido.delete()
    return render(request, "eliminarturno.html")


def actualizarTurno(request, turno_id):
    turno_id = int(turno_id)
    try:
        turno_elegido = Producto.objects.get(id=turno_id)
    except Turnos.DoesNotExist:
        return redirect("index")
    turno_form = TurnosCreate(request.POST or None, instance=turno_elegido)
    if turno_form.is_valid():
        turno_form.save()
        return redirect("clinica:turnos")
    return render(request, "actualizarturno.html", {"upload_form": turno_form})


#########################################################################################################

@login_required
def pacientes(request):
    #    usuario = {'usuario': request.User}
    # NO me deja pasar nunca igual...
    #    if not usuario==True:
    # Aca hay un problema con la url del httpresponse para volver a loguearse si no es medico
    #        return HttpResponse("""Usted no es medico. Si lo es vuelva a <a href = " {{ url : 'usuarios:loguin'}}">loguearse</a> loguearse""")
    if request.user.es_medico:
        return render(request, "pacientes.html", {"pacientes": Paciente.objects.filter(medico_id=request.user.id)})
    if request.user.es_secretaria:
        return render(request, "pacientes.html", {"pacientes": Paciente.objects.all()})
    return render(request, "error.html", {'mensaje': 'No tiene permiso para acceder al sitio'})

class PacienteDetailView(generic.DetailView):
    model = Paciente
    context_object_name = "paciente"
    queryset = Paciente.objects.all()

    def get_object(self):
        paciente = super().get_object()
        paciente.save()
        return paciente

@login_required
def historial(request, paciente_id):
    # habria q agregar un if
    paciente = Paciente.objects.get(id=paciente_id)
    consultas = Consulta.objects.filter(paciente=paciente)


#    consultas = Consulta.objects.filter(turno_id=turno)
        # observacionesTotales = Observacion.objects.all()
        # observaciones = observacionesTotales.filter(Paciente_id=paciente_id)
    return render(request, "historial.html",{
            "consultas": consultas,
            "paciente": paciente,
            # "observaciones": observaciones,
        })
@login_required
def agregar_consulta(request):

    upload = ConsultaCreate()
    if request.method == "POST":
        upload = ConsultaCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload = ConsultaCreate(request.POST, request.FILES)
            f = upload.save(commit=False)
            f.save()
            return redirect("clinica:pacientes")
        else:
            return HttpResponse(
                """your form is wrong, reload on <a href = "{{ url : 'clinica:pacientes' }}" >Recargar</a>"""
            )
    else:
        return render(
            request,
            "agregar_consulta.html",
            {"upload_form": upload, "mensaje": "Paso por acá 1"},
        )


@login_required
def eliminar_consulta(request, consulta_id):
    consulta_id = int(consulta_id)
    try:
        consulta_sel = Consulta.objects.get(id=consulta_id)

    except Consulta.DoesNotExist:
        return redirect("clinica:pacientes")
    consulta_sel.delete()
    return render(request, "eliminar_consulta.html")


@login_required
def modificar_consulta(request, consulta_id):
    consulta_id = int(consulta_id)
    try:
        consulta_sel = Consulta.objects.get(id=consulta_id)
    except Consulta.DoesNotExist:
        return redirect("pacientes")
    consulta_form = ConsultaCreate(request.POST or None, instance=consulta_sel)
    if consulta_form.is_valid():
        consulta_form.save()
        return redirect("clinica:pacientes")
    return render(request, "agregar_consulta.html", {"upload_form": consulta_form})


# ------------------------------------Inicio Pedidos------------------------------------------------


@login_required
def pedidos(request):
    if request.user.es_ventas:
        return render(
            request,
            "pedidos.html",
            {"pedidos": Pedido.objects.filter(vendedor=request.user).order_by("-id")},
        )
    if request.user.es_taller:
        # return render(request,"pedidos.html",{"pedidos": Pedido.objects.filter(estado="TL" ).order_by("-id")},)
        return render(
            request,
            "pedidos.html",
            {
                "pedidos": Pedido.objects.all()
                .exclude(estado="PT")
                .exclude(estado="PD")
                .order_by("-id")
            },
        )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def pedido(request, pedido_id):
    if request.user.es_taller or request.user.es_ventas:
        unPedido = Pedido.objects.get(id=pedido_id)
        if request.user.es_taller and (
            unPedido.estado == "FL" or unPedido.estado == "TL"
        ):
            return render(request, "pedido.html", {"pedido": unPedido})
        else:
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {
                    "mensaje": "No tiene permiso para acceder a la información solicitada"
                },
            )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def agregar_pedido(request):
    if request.user.es_ventas:
        # instanciar la fecha actual
        # upload = PedidoCreate(initial={'estado': 'PT','vendedor': request.user})
        upload = PedidoCreate()
        # upload.vendedor = request.user
        # upload.fields['vendedor'].disabled = True
        # upload.estado = 'PT'
        if request.method == "POST":
            upload = PedidoCreate(request.POST, request.FILES)
            if upload.is_valid():
                f = upload.save(commit=False)
                f.vendedor = request.user
                f.fecha = datetime.datetime.now()
                f.subtotal = 0
                f.estado = "PT"
                f.save()
                # pedido = Pedido.objects.last()
                return redirect("clinica:detalle_pedido", f.id)
            else:
                return render(
                    request, "agregar_pedido.html", {"upload_form": PedidoCreate()}
                )
        else:
            return render(request, "agregar_pedido.html", {"upload_form": upload})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def eliminar_pedido(request, pedido_id):
    # solo superusuario puede eliminar un pedido
    if request.user.es_superuser:
        pedido_id = int(pedido_id)
        try:
            pedido_sel = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {"mensaje": "Hubo un error al recuperar el Pedido"},
            )
        pedido_sel.delete()
        # return render(request, "eliminar_pedido.html")
        return redirect("clinica:pedidos")

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def actualizar_pedido(request, pedido_id):
    # solo superusuario puede modificar un pedido
    if request.user.es_superuser:
        pedido_id = int(pedido_id)
        try:
            pedido_sel = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {"mensaje": "Hubo un error al recuperar el Pedido"},
            )
        pedido_form = PedidoCreate(request.POST or None, instance=pedido_sel)
        if pedido_form.is_valid():
            pedido_form.save()
            return redirect("clinica:pedidos")
        return render(request, "agregar.html", {"upload_form": pedido_form})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def pedido_items(request, pedido_id):
    if request.user.es_ventas or request.user.es_taller:
        unPedido = Pedido.objects.get(id=pedido_id)
        items = PedidoDetalle.objects.filter(pedido_id=unPedido.id)
        f = formAgregarProducto()
        return render(
            request,
            "pedido_items.html",
            {"pedido": unPedido, "items": items, "form": f},
        )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def agregar_item(request, pedido_id):
    if request.user.es_ventas:
        unPedido = Pedido.objects.get(id=pedido_id)
        upload = PedidoDetalleCreate(instance=unPedido)
        # upload.initial['pedido_id'] = 4
        if request.method == "POST":
            upload = PedidoDetalleCreate(request.POST, request.FILES)
            if upload.is_valid():
                upload.save()
                return redirect("clinica:pedidos")
            else:
                # redireccionar a una página de error
                return render(
                    request,
                    "error.html",
                    {"mensaje": "Hubo un error al validar el Pedido"},
                )
        else:
            return render(request, "agregar_item.html", {"upload_form": upload})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


class formAgregarProducto(forms.Form):
    cantidad = forms.IntegerField(label="Cantidad")


@login_required
def detalle_pedido(request, pedido_id):
    if request.user.es_ventas or request.user.es_taller:
        unPedido = Pedido.objects.get(id=pedido_id)
        # formPedido = PedidoView(instance=unPedido)
        # if (request.user.is_authenticated):
        #     formPedido.fields['estado'].disabled = False
        items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by("-id")
        # hay que obtener sólo los productos que no están en el pedido
        productosPedido = items.values_list("producto")
        productos_disponibles = Producto.objects.exclude(id__in=productosPedido)

        if request.user.es_taller and (
            not (unPedido.estado == "TL" or unPedido.estado == "FL")
        ):
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {
                    "mensaje": "No tiene permiso para acceder a la información solicitada"
                },
            )

        # return render(request, 'pedido_items.html', {'pedido': unPedido, 'items': items, 'productos_disponibles': productos_disponibles,'formPedido': formPedido})
        return render(
            request,
            "pedido_items.html",
            {
                "pedido": unPedido,
                "items": items,
                "productos_disponibles": productos_disponibles,
            },
        )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def agregar_producto(request, pedido_id):
    if request.user.es_ventas:
        unPedido = Pedido.objects.get(id=pedido_id)
        # formPedido = PedidoView(instance=unPedido)
        # if (request.user.is_authenticated and request.user.es_vendedor()):
        # formPedido.fields['estado'].disabled = False

        detalle_item = PedidoDetalle()
        detalle_item.pedido = unPedido

        if request.method == "POST":
            producto = Producto.objects.get(id=int(request.POST["productos"]))
            detalle_item.producto = producto
            detalle_item.cantidad = int(request.POST["cantidad"])
            detalle_item.precio = producto.precio
            # creo que necesitamos commit false hasta que el pedido se actualice el precio?
            detalle = detalle_item.save()
            # actualizar unPedido.subtotal+detalle_item.total el total del pedido y guardar
            unPedido.subtotal = unPedido.subtotal + round(
                detalle_item.precio * detalle_item.cantidad, 2
            )
            # unPedido.estado = request.POST["estado"]
            unPedido.save()
            # formPedido = PedidoView(instance=unPedido)
            # formPedido.fields['estado'].disabled = False
            items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by("-id")
            # hay que obtener sólo los productos que no están en el pedido
            productosPedido = items.values_list("producto")
            productos_disponibles = Producto.objects.exclude(id__in=productosPedido)
            return HttpResponseRedirect(
                reverse("clinica:detalle_pedido", args=(pedido_id,))
            )
        else:
            return render(
                request,
                "pedido_items.html",
                {
                    "pedido": unPedido,
                    "items": items,
                    "productos_disponibles": productos_disponibles,
                },
            )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def cambioDeEstado(request, pedido_id):
    if request.user.es_ventas or request.user.es_taller:
        pedido_id = int(pedido_id)
        try:
            pedido_sel = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {"mensaje": "Hubo un error al recuperar el Pedido"},
            )
        if pedido_sel.estado == "FL" or pedido_sel.estado == "PD":
            # redireccionar a una página de error
            return render(
                request,
                "error.html",
                {"mensaje": "No puede modificar el estado actual del Pedido"},
            )
        # Comprobamos si se ha enviado el formulario
        if request.method == "POST":
            estado = request.POST["estado"]
            if not estado == "SL":
                pedido_sel.estado = estado
                pedido_sel.save()
                return redirect("clinica:pedidos")
            else:
                return render(
                    request,
                    "pedido.html",
                    {
                        "pedido": pedido_sel,
                        "mensaje": "Debe seleccionar un estado válido!!",
                    },
                )

        return render(request, "pedido.html", {"pedido": pedido_sel, "mensaje": ""})

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


@login_required
def eliminar_producto(request, detalle_pedido_id):
    if request.user.es_ventas:
        detalle = PedidoDetalle.objects.get(id=int(detalle_pedido_id))
        unPedido = Pedido.objects.get(id=detalle.pedido.id)
        unPedido.subtotal = round(
            unPedido.subtotal - (detalle.precio * detalle.cantidad), 2
        )
        unPedido.save()
        detalle.delete()
        items = PedidoDetalle.objects.filter(pedido_id=unPedido.id).order_by("-id")
        productosPedido = items.values_list("producto")
        productos_disponibles = Producto.objects.exclude(id__in=productosPedido)

        return render(
            request,
            "pedido_items.html",
            {
                "pedido": unPedido,
                "items": items,
                "productos_disponibles": productos_disponibles,
            },
        )

    # redireccionar a una página de error
    return render(
        request, "error.html", {"mensaje": "No tiene permiso para acceder al sitio"}
    )


def reportePacientePedido0(request, filtro):
    fecha_actual = datetime.date.today()
    week = fecha_actual.isocalendar()[1]
    month = fecha_actual.month
    # obtengo la semana/mes y recupero los pacientes
    # redireccionar a una página de
    # results = Members.objects.raw('SELECT * FROM myapp_members GROUP BY designation')
    # pedidos = Pedido.objects.raw('SELECT *, count(id) as "count", SUM(subtotal) as "montoTotal" FROM clinica_pedido GROUP BY paciente_id')

    # week = 49
    # fechaCreacion__month=month,
    # fechaCreacion__week=week
    # pedidos = Pedido.objects.filter(fechaCreacion__week=week).order_by("-id") ok
    # pedidos = Pedido.objects.filter(fechaCreacion__month=month, fechaCreacion__week=week).order_by("-id") ok
    # pedidos = Pedido.objects.filter(fechaCreacion__year=year, fechaCreacion__week=week).order_by("-id") ok

    # pedidos = Pedido.objects.values('paciente').order_by('paciente_id').annotate(count=Count('id')) no anda
    # pedidos = Pedido.objects.order_by('paciente').values('paciente')
    # pedidos = Pedido.objects.group_by('paciente').annotate(cantidad=Count('pedido')).order_by('paciente').distinct() nop
    # pedidos = Pedido.objects.filter(fechaCreacion__week=week).order_by("-id")
    # pedidos = Pedido.objects.filter(fechaCreacion__month=month).order_by("-id")

    # query = Pedido.objects.all().query
    # query.group_by = ['paciente']
    # pedidos = QuerySet(query=query)

    # pedidos = Pedido.objects.filter(fechaCreacion__year=2020, fechaCreacion__week=49).order_by("-id")
    # pedidos = Pedido.objects.filter(fechaCreacion__week=47).order_by("-id")
    filtro = int(filtro)

    if filtro == 1 or filtro == 0:
        if filtro == 1:
            titulo = "Pacientes que realizaron pedidos en el mes"
            pedidos = Pedido.objects.filter(fechaCreacion__month=month).order_by(
                "-paciente_id"
            )
            # return render(request, "reportepedidos.html", {"pedidos": listaPedidos, 'mensaje': 'Mensual venimos del POST', 'filtro':filtro},)
        if filtro == 0:
            titulo = "Pacientes que realizaron pedidos en la semana"
            pedidos = Pedido.objects.filter(fechaCreacion__week=week).order_by(
                "-paciente_id"
            )

        listaPedidos = []
        for pedido in pedidos:
            if not listaPedidos.__contains__(pedido.paciente):
                listaPedidos.append((pedido.paciente))

        # elto = {'mes':meses[mes-1], 'vendedor': vendedor, 'ventas': ventas, 'cantidad':pedidosVendedor.__len__()}

        return render(
            request,
            "reportepedidos.html",
            {"pedidos": listaPedidos, "titulo": titulo},
        )
    else:
        return render(
            request, "error.html", {"mensaje": "Hubo un error al procesar la solicitud"}
        )


def reportePacientePedido(request, filtro):
    fecha_actual = datetime.date.today()
    week = fecha_actual.isocalendar()[1]
    month = fecha_actual.month
    filtro = int(filtro)

    if filtro == 1 or filtro == 0:
        listaPacientes = []
        pacientes = Paciente.objects.all()
        for paciente in pacientes:
            if filtro == 1:
                titulo = "Pacientes que realizaron pedidos en el mes"
                listaPedidos1 = Pedido.objects.filter(
                    fechaCreacion__month=month, paciente=paciente, estado="FL"
                )
                listaPedidos2 = Pedido.objects.filter(
                    fechaCreacion__month=month, paciente=paciente, estado="PD"
                )

            if filtro == 0:
                titulo = "Pacientes que realizaron pedidos en la semana"
                listaPedidos1 = Pedido.objects.filter(
                    fechaCreacion__week=week, paciente=paciente, estado="FL"
                )
                listaPedidos2 = Pedido.objects.filter(
                    fechaCreacion__week=week, paciente=paciente, estado="PD"
                )

            total = 0
            for pedido in listaPedidos1:
                total = total + pedido.subtotal

            for pedido in listaPedidos2:
                total = total + pedido.subtotal

            cantidad = listaPedidos1.__len__() + listaPedidos2.__len__()

            if cantidad > 0:
                listaPacientes.append(
                    {"paciente": paciente, "total": total, "cantidad": cantidad}
                )

        return render(
            request,
            "reportepedidos.html",
            {"pacientes": listaPacientes, "titulo": titulo, "week": week, "mes": month},
        )
    else:
        return render(
            request, "error.html", {"mensaje": "Hubo un error al procesar la solicitud"}
        )


def reporteVentas(request, anio):
    if anio == 0:
        anio = datetime.date.today().year

    fecha_actual = datetime.date.today()
    month = 12
    if fecha_actual.year == anio:
        month = fecha_actual.month
    elif fecha_actual.year > anio:
        month = 12
    else:
        # recargar con un error adecuado
        return render(
            request, "error.html", {"mensaje": "Hubo un error al procesar la solicitud"}
        )

    # pedidos=Pedido.objects.filter(fechaCreacion__month=month).order_by("-vendedor_id")
    vendedores = get_user_model().objects.filter(es_ventas=True)
    listaVentas = []
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    rango = range(1, month + 1)
    for mes in rango:
        for vendedor in vendedores:
            # controlar el estado del Pedido = PD o FL
            pedidosVendedor = Pedido.objects.filter(
                vendedor=vendedor, fechaCreacion__month=mes
            ).order_by("-id")
            ventas = 0
            for pedidoVendedor in pedidosVendedor:
                ventas = ventas + pedidoVendedor.subtotal

            elto = {
                "mes": meses[mes - 1],
                "vendedor": vendedor,
                "ventas": ventas,
                "cantidad": pedidosVendedor.__len__(),
            }
            listaVentas.append(elto)

    return render(
        request,
        "reporte_ventas.html",
        {"pedidos": listaVentas, "vendedores": vendedores},
    )


def reporteVentasAnual(request):
    anio = datetime.date.today().year
    myDate = datetime.now()
    # formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
    formatedDate = myDate.strftime("%Y")
    return render(request, "reportes/reporte_ventas.html", {"date": formatedDate})
    # return HttpResponseRedirect(reverse("clinica:reporteVentas", args=(anio,)))
    # return redirect("clinica:pedidos" datetime.date.today.month)

def productoMasVendidos(request):
    fecha_actual = datetime.date.today()
    month = fecha_actual.month
    pedidos = Pedido.objects.filter(fechaCreacion__month=month ).filter(estado = 'PD')
    pedidoDetalle = []
    #producto = []
    for pedido in pedidos:
        pedidoDetal = PedidoDetalle.objects.filter(pedido_id = pedido.id)
        #pedidoDetalle.append(pedidoDetal)
        for  pedidoDet in pedidoDetal:
            pedidoDetalle.append(pedidoDet)

    dic_prod = {}
    # for prod in pedidoDetalle:

    #     producto = str(prod.producto.pk)
    #     if producto in dic_prod:
    #         dic_prod[producto] = dic_prod[producto] + prod.cantidad
    #     else:
    #         dic_prod[producto] =  prod.cantidad

    for prod in pedidoDetalle:

        producto = str(prod.producto)
        if producto in dic_prod:
            dic_prod[producto] = dic_prod[producto] + prod.cantidad
        else:
            dic_prod[producto] =  prod.cantidad        
   
    sortedDict = sorted(dic_prod.items(),key=operator.itemgetter(1), reverse= True)
    #Out: [('fourth', 1), ('third', 2), ('first', 3), ('second', 4)]
    print(dic_prod)
    print(sortedDict)

    return render(request, "reporteProductosVendidos.html", {"pedidos": sortedDict})        

# ------------------------------------Fin Pedidos------------------------------------------------

#  viaje de seba con los generic views
class TurnosListView(generic.ListView):
    model = Turnos

    def get_queryset(self):
        qs = self.model.objects.all()
        turnos_filtered_list = TurnosFilter(self.request.GET, queryset=qs)
        return turnos_filtered_list.qs


class TurnoDetailView(generic.DetailView):
    model = Turnos
    context_object_name = "turnos"
    queryset = Turnos.objects.all()

    #    def get_context_data(self, **kwargs):
    #        context = super().get_context_data(**kwargs)
    #        context["turnos_list"] = Turnos.objects.all()
    #        return context

    def get_object(self):
        turno = super().get_object()
        turno.save()
        return turno


class TurnoCreate(CreateView):
    model = Turnos
    fields = "__all__"

    def get_form(self):
        form = super().get_form()
        form.fields["FechaTurno"].widget = DatePickerInput(format="%d/%m/%Y")
        form.fields["HoraTurno"].widget = TimePickerInput()
        return form


class TurnoUpdate(UpdateView):
    model = Turnos
    fields = ["Paciente", "HoraTurno", "FechaTurno", "Asistencia"]


class TurnoDelete(DeleteView):
    model = Turnos
    success_url = reverse_lazy("clinica:turnos")

#este usa el medico
@login_required
def turnos_reporte(request):
    # medico = request.user
    # pacientes = Paciente.objects.filter(medico=medico)
    # pacientes_mostrar = []
    # for paciente in pacientes:
    #     filtro = Turnos.objects.filter(Paciente=paciente.paciente_id)
    #     if (list.isEmpty()):
    #         pacientes_mostrar     

    filter = TurnosFilter(request.GET)
    context = {
        "filter": filter,
         }
    return render(request, "clinica/turnos-reporte.html", context )

@login_required
def reporte_asistencia(request):
    filter = ReporteFilter(request.GET, queryset=Turnos.objects.all())

    return render(request, "clinica/reporte-asistencia.html", {"filter": filter})

# class PacienteCreate(generic.CreateView):
#     model = Paciente
#     fields = ('medico',)

#     def get_form(self):
#         User = get_user_model()
#         form = super().get_form()
#         self.fields['medico'].queryset = User.objects.filter(es_medico = True)
#        return form

@login_required
def PacienteCreate(request):
    if request.user.es_secretaria:
        upload = PacienteForm()
        if request.method == "POST":
            upload = PacienteForm(request.POST, request.FILES)
            f = upload.save(commit=False)
            f.save()
            return redirect("clinica:pacientes-detail", f.id)
        else:
            return render(request, "paciente_form.html", {"upload_form": PacienteForm()})
    else:
        return render(request, "paciente_form", {"upload_form": upload})



class PacienteUpdate(generic.UpdateView):
    model = Paciente
    fields = "__all__"


class PacienteDelete(generic.DeleteView):
    model = Paciente
    success_url = reverse_lazy("clinica:pacientes")


# def add(request):
#     # Creamos un formulario vacío
#     form = PersonaForm()

#     # Comprobamos si se ha enviado el formulario
#     if request.method == "POST":
#         # Añadimos los datos recibidos al formulario
#         form = PersonaForm(request.POST)
#         # Si el formulario es válido...
#         if form.is_valid():
#             # Guardamos el formulario pero sin confirmarlo,
#             # así conseguiremos una instancia para manejarla
#             instancia = form.save(commit=False)
#             # Podemos guardarla cuando queramos
#             instancia.save()
#             # Después de guardar redireccionamos a la lista
#             return redirect('/')

#     # Si llegamos al final renderizamos el formulario
#     return render(request, "core/add.html", {'form': form})

# def edit(request, persona_id):
#     # Recuperamos la instancia de la persona
#     instancia = Persona.objects.get(id=persona_id)

#     # Creamos el formulario con los datos de la instancia
#     form = PersonaForm(instance=instancia)

#     # Comprobamos si se ha enviado el formulario
#     if request.method == "POST":
#         # Actualizamos el formulario con los datos recibidos
#         form = PersonaForm(request.POST, instance=instancia)
#         # Si el formulario es válido...
#         if form.is_valid():
#             # Guardamos el formulario pero sin confirmarlo,
#             # así conseguiremos una instancia para manejarla
#             instancia = form.save(commit=False)
#             # Podemos guardarla cuando queramos
#             instancia.save()

#     # Si llegamos al final renderizamos el formulario
#     return render(request, "core/edit.html", {'form': form})

# def delete(request, persona_id):
#     # Recuperamos la instancia de la persona y la borramos
#     instancia = Persona.objects.get(id=persona_id)
#     instancia.delete()

#     # Después redireccionamos de nuevo a la lista
#     return redirect('/')

# <ul>
#     {% for persona in personas %}
#     <li>
#         {{ persona.nombre }}, {{ persona.edad }} años
#         <a href="/edit/{{ persona.id }}">Editar</a>
#         <a href="/delete/{{ persona.id }}"
#           onClick="return confirm('¿Seguro que quieres borrar a {{persona.nombre}}?');">
#             Borrar
#         </a>
#     </li>
#     {% endfor %}
# </ul>


class TurnosYearArchiveView(LoginRequiredMixin, YearArchiveView):
    login_url = "usuarios:login"
    redirect_field_name = "redirect_to"

    queryset = Turnos.objects.all()
    date_field = "FechaTurno"
    make_object_list = True
    allow_future = True


class TurnosMonthArchiveView(MonthArchiveView):
    queryset = Turnos.objects.all()
    date_field = "FechaTurno"
    allow_future = True


class TurnosDayArchiveView(DayArchiveView):
    queryset = Turnos.objects.all()
    date_field = "FechaTurno"
    allow_future = True


# class ObservacionListView(generic.ListView):
#    model = Observacion

#    def get_queryset(self):
#        qs = self.model.objects.all()
#        observacion_filtered_list = ObservacionFilter(self.request.GET, queryset=qs)
#        return observacion_filtered_list.qs


# class ObservacionDetailView(generic.DetailView):
#    model = Observacion
#    context_object_name= 'observacion'
#    queryset= Observacion.objects.all()

#    def get_object(self):
#        observacion= super().get_object()
#        observacion.save()
#        return observacion

# class ObservacionCreate(generic.CreateView):
#    model = Observacion
#    fields = '__all__'


# class ObservacionUpdate(generic.UpdateView):
#    model = Observacion
#    fields = '__all__'

# class ObservacionDelete(generic.DeleteView):
#    model = Observacion
#    success_url = reverse_lazy('clinica:turnos/observacion')

# def verConsulta(request, turno_id):
#     turno = Turnos.objects.get(id=turno_id)
#     try:
#         consulta = Consulta.objects.get(turno_id=turno.id)
#     except Consulta.DoesNotExist:
#         return redirect("clinica:agregar_consulta", consulta.id)

#         # raise render(request, "agregar_consulta.html", {'upload_form': ConsultaCreate()})
#     return redirect("clinica:modificar_consulta", consulta.id)
