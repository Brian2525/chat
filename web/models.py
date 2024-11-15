from django.db import models



# Modelo para las categorías
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Nombre de la categoría

    def __str__(self):
        return self.name

# Modelo para los proyectos
class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')  # Relación con categoría
    title = models.CharField(max_length=200)  # Título del proyecto
    description = models.TextField()  # Descripción del proyecto
    image = models.ImageField(upload_to='media/web/projects/')  # Imagen del proyecto
    url = models.URLField()  # URL del proyecto

    def __str__(self):
        return self.title

