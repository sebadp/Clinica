# Generated by Django 3.1.7 on 2022-08-09 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observaciones', models.TextField()),
                ('motivo', models.CharField(max_length=150)),
                ('diagnostico', models.CharField(max_length=150)),
                ('tratamiento', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=60)),
                ('telefono', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('T', 'Tarjeta de credito'), ('B', 'Billetera virtual'), ('E', 'Efectivo'), ('D', 'Debito')], default='E', max_length=1)),
                ('estado', models.CharField(choices=[('PT', 'Pendiente'), ('PD', 'Pedido'), ('TL', 'Taller'), ('FL', 'Finalizado')], default='PT', max_length=2)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('fechaCreacion', models.DateField(auto_now=True)),
                ('paciente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clinica_paciente', to='clinica.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tipo', models.CharField(choices=[('L', 'Lente'), ('E', 'Estuche'), ('G', 'Gotita'), ('A', 'Accesorios')], default='L', max_length=1)),
                ('enfoque', models.CharField(blank=True, choices=[('L', 'Lejos'), ('C', 'Cerca')], max_length=1, null=True)),
                ('lado', models.CharField(blank=True, choices=[('I', 'Izqierda'), ('D', 'Derecha')], max_length=1, null=True)),
                ('armazon', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Turnos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FechaTurno', models.DateField()),
                ('HoraTurno', models.TimeField()),
                ('Asistencia', models.CharField(blank=True, choices=[('P', 'Pendiente'), ('A', 'Asistió'), ('F', 'Faltó')], max_length=1, null=True)),
                ('Paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.paciente')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('precio', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('pedido', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.pedido')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinica.producto')),
            ],
        ),
    ]
