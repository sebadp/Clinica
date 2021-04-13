# Clínica Privada
Sistema MVC desarrollado con Django y Python.

	El sistema ofrece :
		. Gestión de Historial clínico. Búsqueda de pacientes por fecha de consulta.
		. Gestión de Pacientes y Turnos.
		. Sistema de Ventas para la toma de pedidos.
		. Canal de comunicación entre los Vendedores y el Taller.
		. Informes personalizados para la Gerencia:
			. Pacientes que asistieron a los turnos en la semana/mes. 
			. Pacientes que no asistieron a los turnos en la semana/mes. 
			. Pacientes que hicieron por lo menos un Pedido en la semana/mes.        	
			. Productos más vendidos en el mes. 
			. Ventas totales por mes clasificadas por Vendedores.
		. Autenticación de Usuarios y Permisos. Los grupos disponibles son: 
			. Gerencia. Médico. Secretario. Vendedor. Taller.


Si les interesa saber más acerca de sus funciones y usos, en esta Web Presentación he puesto a disposición la documentación donde explico cada función y otros detalles de diseño: https://sebadp.github.io/clinica.github.io/

## Casos de uso:
* Gerente:. Puede visualizar todos los datos y realizar los siguientes reportes 
	. Pacientes que asistieron a los turnos en la semana/mes. 
	. Pacientes que no asistieron a los turnos en la semana/mes. 
	. Pacientes que hicieron por lo menos un Pedido en la semana/mes.        			
	. Productos más vendidos en el mes. 
	. Ventas totales por mes clasificadas por Vendedores.
	. Puede crear usuarios.
	
	![gerencia](https://user-images.githubusercontent.com/66728448/114524941-0ad9df00-9c1c-11eb-8d2b-f3d8c980aa66.gif)

        		
* Médico:
	. Puede agregar observaciones al historial médico de sus pacientes, ver el listado de Pacientes filtrando por día, mes o año.
	. Solo puede ver los pacientes atendidos que se le fueron asignados.
 			
	![medicos](https://user-images.githubusercontent.com/66728448/114525000-1927fb00-9c1c-11eb-84f1-d723fb6f40fd.gif)

		
* Secretario:
. Puede agregar, modificar o eliminar los turnos de los Pacientes.
	
	![pacientes](https://user-images.githubusercontent.com/66728448/114525088-2fce5200-9c1c-11eb-8ff5-c892a272289a.gif)
	
	
* Ventas:	
 	. Puede generar un pedido para el paciente, donde detalla los productos que quiere adquirir, el precio, un subtotal, tipo de pago (tarjeta de crédito, 		debido, billetera virtual o efectivo).
	. El producto tiene nombre, si está clasificado como Lente tendrá la opción de Lejos/Cerca, Izquierda/Derecha, si incluye Armazón o no.
 	Una vez que se genera el pedido queda en estado “Pendiente”.
	. El rol de Ventas puede cambiar el estado a “Pedido” o mandarlo a “Taller”.
 	
	![venta](https://user-images.githubusercontent.com/66728448/114525184-4674a900-9c1c-11eb-9c30-a1b4de6ae8f1.gif)

	
* Taller:. Solo visualiza la lista de pedidos (con todos los detalles de los productos sin los precios).
	. El Taller puede confirmar cambiando el estado del pedido a “Finalizado”.

	![taller](https://user-images.githubusercontent.com/66728448/114525214-4c6a8a00-9c1c-11eb-9444-fc1c46b96188.gif)


## Comenzando: 
Pre-requisitos : Necesitas tener instalado Python y Pip instalados en tu sistema.

### Clonar el repositorio 

1: Abre tu terminal y posicionate en el directorio donde quieres clonar el repositorio.
	
	>>mkdir Clinica # para crear el directorio llamado Clinica
	>>cd Clinica

2: Tipea en tu terminal:
	
	*>> git clone https://github.com/sebadp/Clinica

### Instalación 

3: Crear un entorno virtual e instalar lo que haya en “requeriments.txt”:

	>>cd ..
	>>python -m venv venv   # Crea el entorno virtual dentro de la carpeta venv
	>>source venv/bin/activate
	>>cd Clinica
	>>pip install -r requirements.txt # Instala los requerimientos para el sistema.

4: Inicializa el sistema:

	>>python manage.py makemigrations
	>>python manage.py migrate
	>>python manage.py runserver

5: Abre tu navegador web y explora el sistema en tu localhost.

## Ejecutando las pruebas 

Para ejecutar las pruebas debes situarte dentro de la carpeta contenedora del archivo manage.py y ejecutar el siguiente comando desde la terminal:

	>>python3 manage.py test

Analice las pruebas end-to-end 
Cada una de las pruebas chequea el funcionamiento correcto de cada "Caso de Uso".

## Despliegue 

El paquete está preparado para desplegar en Heroku, ya tiene su Procfile e incluídas todas las importaciones en los archivos de configuración.

1. Para realizar el despliegue tienes que modificar el archivo manage.py y wsgi.py o asgi.py.

2. En cada uno debes de sustituir la variable 'Tpclinica.settings.local'  por 'Tpclinica.settings.production'.

## Construido con 

Desarrollado en un entorno GNU/Linux, en lenguaje Python, con el framework Django. 
La base de datos que utilizamos es Postgre.

## Autores 

Originalmente desarrollado como Trabajo Final del curso de Desarrollo Web Fullstack con Javascript y Python, por: 
. Aguirre Mariano
. Cruz Martinez Melisa
. Dávila Paz Sebastián
. Duarte Edgar

Refactorizado, documentado y desplegado por Sebastián Dávila.

## Licencia 

Este proyecto está bajo la Licencia (MIT) - mira el archivo LICENSE.md para detalles

## Gracias por comentar 

Se agradece cualquier tipo de aporte, comentario o crítica constructiva. Enviar a :  sebastian.davila.personal@gmail.com
