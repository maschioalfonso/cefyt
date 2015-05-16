from django.contrib import admin
from sia.models import (Alumno, Pais, Materia, Curso, Cursado, Cuota,
                        DescubrimientoOpcion, DescubrimientoCurso)


class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'documento', 'fecha_de_nacimiento',
                    'pais', 'provincia', 'localidad', 'domicilio', 'telefono',
                    'telefono_alter')
    search_fields = ['id']


class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


class CursadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'duracion', 'costo_inscripcion_pesos',
                    'costo_inscripcion_dolares', 'costo_certificado_pesos',
                    'costo_certificado_dolares', 'valor_cuota_pesos',
                    'valor_cuota_dolares', 'inscripcion_abierta')


class CuotaAdmin(admin.ModelAdmin):
    list_display = ('alumno_id', 'id', 'cursado', 'alumno', 'numero',
                    'valor_cuota_pesos', 'valor_cuota_dolares',
                    'es_certificado', 'fecha_de_pago', 'comprobante', 'pagado')

    search_fields = ['id', 'alumno__usuario__username']

    def alumno_id(self, instance):
        return instance.alumno.id


class DescubrimientoCursoAdmin(admin.ModelAdmin):
    list_display = ('cursada', 'alumno', 'opcion')


admin.site.register(Pais)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Materia)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Cursado, CursadoAdmin)
admin.site.register(Cuota, CuotaAdmin)
admin.site.register(DescubrimientoOpcion)
admin.site.register(DescubrimientoCurso, DescubrimientoCursoAdmin)
