# Parametrización del sistema

Está sección detalla la parametrización del sistema que debe hacer un usuario Administrador.

## Alta de cursos

Un _curso_ es un conjunto de _materias_ más una descripción opcional.
Un _cursado_ (o cohorte) es una entidad basada en un _curso_ que además
contiene información temporal y económica.

Una materia puede ser usada en distintos cursos.<br>
Por ej.: 'Matemática' puede formar parte tanto del curso 'Electrónica' como así también del curso 'Arquitectura'. 

Un cursado está compuesto por un curso y además contiene información de los costos económicos.<br>
Debe crearse un nuevo cursado por cada dictado de un curso.

Por ej.: el cursado _Electrónica 2015 (primer semestre)_
está basado en el curso _Electrónica_, y en éste dictado tiene un costo de $350, en cambio, el cursado _Electrónica 2015 (segundo semestre)_ tiene un costo de $450.

De ésta forma no es necesario crear un curso en cada dictado, solamente se crea un nuevo cursado
indicando los nuevos valores.


### Materias
Las _materias_ están compuestas por:

- Nombre.

Una misma materia puede formar parte de distintos _cursos_.


### Cursos
Los _cursos_ están compuestos por:

- Nombre.
- Materias: Conjunto de materias que contiene.
- Descripción (Opcional).

Un mismo curso puede formar parte de distintos _cursados_.

### Cursado
Los _cursados_ están compuestos por:

- Nombre: Nombre del cursado (o cohorte).
- Curso: Curso en el que está basado. 
- Duración: Cantidad de meses de duración.
- Costo de inscripción en pesos.
- Costo de inscripción en dólares.
- Costo certificado en pesos.
- Costo certificado en dólares.
- Valor cuota en pesos.
- Valor cuota en dólares.
- Inscripción abierta: Si está tildado, éste cursado aparecerá 
  disponible para inscripción en las cuentas de los alumnos.


## ¿Cómo conoció el curso?
Un alumno al inscribirse a un curso, se le preguntará cómo conoció el curso. Las opciones
que podrá elegir se parametrizan desde _Descubrimiento de los cursos (opciones)_, que están compuesto por:

- Opción: Por ej. _"Lo conocí por publicidad en Internet"_.

Se pueden agregar tantas opciones como se deseen.

Los resultados de las opciones elegidas por los alumnos se visualizan desde _Descubrimiento de los cursos_, allí se mostrará el nombre del _alumno_, el  _curso_ (es decir, al cursado o cohorte) al que se inscribió y la opción elegida.


## Países
Al registrarse al sistema, un alumno deberá seleccionar su País de residencia. Los países listados se parametrizan desde _Paises_, con el campo:

- Nombre.
 

# Cuenta del alumno

## Registro
Cada alumno deberá registrarse al sistema ingresando los datos:

- Nombre
- Apellido
- Documento
- Domicilio
- País
- Provincia
- Localidad
- Teléfono
- Teléfono alternativo
- Fecha de nacimiento (Formato DD/MM/AAAA)
- Correo electrónico
- Contraseña

Una vez registrado, ingresará a su cuenta utilizando el correo electrónico y la contraseña.

## Inscripción
En su cuenta, el alumno visualizará todos los _cursados_ cuya opción _Inscripción Abierta_ está activada (ver [Parametrización del sistema -> Cursado](#cursado)).

Podrá elegir un curso e inscribirse, seleccionando además cómo conoció el curso (ver [Parametrización del sistema -> ¿Cómo conoció el curso?](#cómo-conoció-el-curso)).

Al inscribirse se generarán las cuotas para ese curso, y el alumno las podrá visualizar desde _Ver estado de cuotas_.