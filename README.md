#Parametrización del sistema#
Está sección detalla la parametrización del sistema que debe hacer un usuario Administrador.

##Alta de cursos##
Un *curso* es un conjunto de *materias* más una descripción opcional.
Un *cursado* (o cohorte) es una entidad basada en un *curso* que además
contiene información temporal y económica.

Una materia puede ser usada en distintos cursos.<br>
Por ej.: 'Matemática' puede formar parte tanto del curso 'Electrónica' como así también del 
curso 'Arquitectura'. 

Un cursado está compuesto por un curso y además contiene 
información de los costos económicos.<br>
Debe crearse un nuevo cursado por cada dictado de un curso.<br> 
Por ej.: el cursado 'Electrónica 2015 (primer semestre)'
está basado en el curso 'Electrónica', y en éste dictado tiene un costo de $350, en cambio,<br>
el cursado 'Electrónica 2015 (segundo semestre)' tiene un costo de $450.

De ésta forma no es necesario crea un curso en cada dictado, solamente se crea un nuevo cursado
indicando los nuevos valores.


#####Materias#####
Las *materias* están compuestas por:

* Nombre.

Una misma materia puede formar parte de distintos *cursos*.


#####Cursos#####
Los *cursos* están compuestos por:

* Nombre.
* Materias: Conjunto de materias que contiene.
* Descripción (Opcional).

Un mismo curso puede formar parte de distintos *cursados*.

#####Cursado#####
Los *cursados* están compuestos por:

* Nombre: Nombre del cursado (o cohorte).
* Curso: Curso en el que está basado. 
* Duración: Cantidad de meses de duración.
* Costo de inscripción en pesos.
* Costo de inscripción en dólares.
* Costo certificado en pesos.
* Costo certificado en dólares.
* Valor cuota en pesos.
* Valor cuota en dólares.
* Inscripción abierta: Si está tildado, éste cursado aparecerá 
  disponible para inscripción en las cuentas de los alumnos.


##¿Cómo conoció el curso?##
Un alumno al inscribirse a un curso, se le preguntará cómo conoció el curso. Las opciones
que podrá elegir se parametrizan desde *Descubrimiento de los cursos (opciones)*, que están compuesto por:

* Opción: Por ej. *"Lo conocí por publicidad en Internet"*.

Se pueden agregar tantas opciones como se deseen.

Los resultados de las opciones elegidas por los alumnos se visualizan desde *Descubrimiento de los cursos*, allí se mostrará el nombre del *alumno*, el  *curso* (es decir, al cursado o cohorte) al que se inscribió y la opción elegida.


##Países##
Al registrarse al sistema, un alumno deberá seleccionar su País de residencia. Los países listados se parametrizan desde *Paises*, con el campo:

* Nombre.
 

#Cuenta del alumno#

## Registro ##
Cada alumno deberá registrarse al sistema ingresando los datos:

* Nombre
* Apellido
* Documento
* Domicilio
* País
* Provincia
* Localidad
* Teléfono
* Teléfono alternativo
* Fecha de nacimiento
* Correo electrónico
* Contraseña

Una vez registrado, ingresará a su cuenta utilizando el correo electrónico y la contraseña.

## Inscripción ##
En su cuenta, el alumno visualizará todos los *cursados* cuya opción 'Inscripción Abierta' está
activada (ver Parametrización del sistema -> Cursado).<br>
Podrá elegir un curso e inscribirse, seleccionando además cómo conoció el curso (ver Parametrización del sistema -> ¿Cómo conoció el curso?).

Al inscribirse se generarán las cuotas para ese curso, y el alumno las podrá visualizar desde
*Ver estado de cuotas*. Si el alumno reside en Argentina, además podrá generar el cupón de pago
para RapiPago.