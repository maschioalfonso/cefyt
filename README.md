##Dictado de cursos##

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

###Ejemplo###
To Do


##¿Cómo conoció el curso?##
Un alumno al inscribirse a un curso, se le preguntará cómo conoció el curso. Las opciones
que podrá elegir se parametrizan desde *Descubrimiento de los cursos (opciones)*, que están compuesto por:

* Opción: Por ej. *"Lo conocí por publicidad en Internet"*.

Se pueden agregar tantas opciones como se deseen.

Los resultados de las opciones elegidas por los alumnos se visualizan desde *Descubrimiento de los cursos*, allí se mostrará el nombre del *alumno*, el  *curso* (es decir, al cursado o cohorte) al que se inscribió y la opción elegida.


##Países##
Al registrarse al sistema, un alumno deberá seleccionar su País de residencia. Los países listados se parametrizan desde *Paises*, con el campo:

* Nombre.
 







###En construcción###
####Crear, modificar, eliminar####
 

* Agregar: `admin->` **`<<nombre_modelo>>`** `->Agregar <<nombre_modelo>>`.
* Modificar: en `admin->` **`<<nombre_modelo>>`** clickear en el modelo que desea modificar.
* Borrar: en `admin->` **`<<nombre_modelo>>`** tildar el(los) modelo(s), seleccionar `Acción: Eliminar` **`<<nombre_modelo>>`** `seleccionados/as` y presionar `Ejecutar`.