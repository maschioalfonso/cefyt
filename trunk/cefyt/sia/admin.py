from django.contrib import admin
from sia.models import Alumno, Pais, Materia, Curso, Cursado, Cuota, DescubrimientoOpcion, DescubrimientoCurso

class CuotaAdmin(admin.ModelAdmin):
    list_display = ('cursado', 'alumno', 'numero', 'fecha_de_pago', 'comprobante', 'pagado')

admin.site.register(Pais)
admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Curso)
admin.site.register(Cursado)
admin.site.register(Cuota, CuotaAdmin)
admin.site.register(DescubrimientoOpcion)
admin.site.register(DescubrimientoCurso)
