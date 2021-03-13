from django.db import models
from usuarios.models import User
from django.urls import reverse
import datetime
from django.utils import timezone

#  PerfilVentas, PerfilMedico


# Create your models here.


class Producto(models.Model):
    descripcion = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    TIPOS = (("L", "Lente"), ("E", "Estuche"), ("G", "Gotita"), ("A", "Accesorios"))
    tipo = models.CharField(max_length=1, choices=TIPOS, default="L")
    ENFOQUE = (("L", "Lejos"), ("C", "Cerca"))
    enfoque = models.CharField(max_length=1, choices=ENFOQUE, blank=True, null=True)
    LADO = (("I", "Izqierda"), ("D", "Derecha"))
    lado = models.CharField(max_length=1, choices=LADO, blank=True, null=True)
    armazon = models.BooleanField(default=False)

    def __str__(self):
        if self.tipo == "E":
            tipo = "Estuche"
        if self.tipo == "G":
            tipo = "Gotita"
        if self.tipo == "A":
            tipo = "Accesorios"
        if self.tipo == "L":
            tipo = "Lente"
            enfoque = "Cerca"
            if self.enfoque == "L":
                enfoque = "Lejos"
            lado = "Der."
            if self.lado == "I":
                lado = "Izq."
            armazon = "s/armazón"
            if self.armazon:
                armazon = "c/armazón"
            return f"{self.id} - {tipo} {enfoque} {lado} {armazon} {self.descripcion} ${self.precio} "
        return f"{self.id} - {tipo} {self.descripcion} ${self.precio}"

    def productoView(self):
        if self.tipo == "E":
            tipo = "Estuche"
        if self.tipo == "G":
            tipo = "Gotita"
        if self.tipo == "A":
            tipo = "Accesorios"
        if self.tipo == "L":
            tipo = "Lente"
            enfoque = "Cerca"
            if self.enfoque == "L":
                enfoque = "Lejos"
            lado = "Der."
            if self.lado == "I":
                lado = "Izq."
            armazon = "s/armazón"
            if self.armazon:
                armazon = "c/armazón"
            return f"{tipo} {enfoque} {lado} {armazon} {self.descripcion} "
        return f"{tipo} {self.descripcion} "


# class Paciente(models.Model):
#     nombre = models.CharField(max_length = 120)
# place = models.OneToOneField(
#     Place,
#     on_delete=models.CASCADE,
#     primary_key=True,
# )
# class Doctor(models.Model):
#     nombre = models.CharField(max_length = 120)
# place = models.OneToOneField(
#     Place,
#     on_delete=models.CASCADE,
#     primary_key=True,
#     nombre = models.CharField(max_length = 120)
# )


class Paciente(models.Model):
    medico = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True,null=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    direccion = models.CharField(max_length=60)
    telefono = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def get_absolute_url(self):
        return reverse("clinica:pacientes-detail", kwargs={"pk": self.id})


class Pedido(models.Model):
    vendedor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="user", null=True
    )
    paciente = models.ForeignKey(
        Paciente, on_delete=models.CASCADE, related_name="clinica_paciente", null=True
    )
    TIPO_PAGO = (
        ("T", "Tarjeta de credito"),
        ("B", "Billetera virtual"),
        ("E", "Efectivo"),
        ("D", "Debito"),
    )
    tipo_pago = models.CharField(max_length=1, default="E", choices=TIPO_PAGO)
    ESTADO = (
        ("PT", "Pendiente"),
        ("PD", "Pedido"),
        ("TL", "Taller"),
        ("FL", "Finalizado"),
    )
    estado = models.CharField(max_length=2, default="PT", choices=ESTADO)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fecha = models.DateTimeField(auto_now=True, auto_now_add=False)
    fechaCreacion = models.DateField(auto_now=True, auto_now_add=False)

    def verSubTotal(self):
        return f"${self.subtotal}"


class PedidoDetalle(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, blank=False, null=True
    )
    pedido = models.ForeignKey(
        Pedido, on_delete=models.SET_NULL, blank=False, null=True
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, blank=True
    )

    def subtotal(self):
        return round(self.precio * self.cantidad, 2)

    """def save(self, *args, **kwargs):
        self.total = self.producto.precio * Decimal(self.cantidad)  
        producto = Producto.objects.get(id=self.producto.id)
        pedido = Pedido.objects.get(id=self.pedido.id)
        detalle = DetallePedido.objects.filter(id=self.id)
        if detalle:
            if self.cantidad > detalle[0].cantidad:
                pedido.subtotal += self.total - detalle[0].total
            else:
                pedido.subtotal -= detalle[0].total - self.total
        else:
            if pedido.subtotal:
                pedido.subtotal += self.total
            else:
                pedido.subtotal = self.total
        producto.save()
        pedido.save()
        super().save(*args, **kwargs)
        def obtenerCantidad(self):
            return f"{self.cantidad} {'unidades' if self.cantidad > 1 else 'unidad'}
        def __str__(self):
            return self.producto.nombre"""


class Consulta(models.Model):
    observaciones = models.TextField()
    motivo = models.CharField(max_length=150)
    diagnostico = models.CharField(max_length=150)
    tratamiento = models.CharField(max_length=150)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=False,null=False)

    def __str__(self):
        return self.motivo


#  viaje de seba con los generic views
class Turnos(models.Model):
    Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, blank=False,null=False)
    FechaTurno = models.DateField()
    HoraTurno = models.TimeField()
    Opciones = (("P", "Pendiente"), ("A", "Asistió"), ("F", "Faltó"))
    Asistencia = models.CharField(max_length=1, choices=Opciones, blank=True, null=True)
    #    FechaAlta = models.DateField(auto_now=True)
    #    FechaBaja = models.DateField(blank=True,null=True)

    def _str_(self):
        return f"{self.id} {self.Paciente} {self.FechaTurno} {self.HoraTurno}"

    def get_absolute_url(self):
        return reverse("clinica:turnos-detail", kwargs={"pk": self.id})


# class Observacion(models.Model):
#    Paciente = models.ForeignKey(Paciente,  on_delete=models.CASCADE, blank=False,null=True)
#    Fecha = models.DateField(auto_now=True)
#    Consulta = models.ForeignKey(Consulta,  on_delete=models.CASCADE, blank=False,null=True)
#    def get_absolute_url(self):
#        return reverse('clinica:observacion-detail', kwargs={'pk':self.id})
