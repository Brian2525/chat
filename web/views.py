
from django.shortcuts import render
from .models import Project, Category

def home(request):
    # Obtener todas las categorías
    categories = Category.objects.all()

    # Obtener todos los proyectos
    selected_category = request.GET.get('category')  # Obtener la categoría seleccionada de los parámetros GET
    if selected_category:
        projects = Project.objects.filter(category__id=selected_category)  # Filtrar proyectos por categoría
    else:
        projects = Project.objects.all()  # Mostrar todos los proyectos si no se ha seleccionado categoría

    # Renderizar la plantilla con los proyectos y categorías
    return render(request, 'web/index.html', {'projects': projects, 'categories': categories, 'selected_category': selected_category})
