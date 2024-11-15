from django.db import models



class Visitor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Thread(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    thread_id = models.CharField(max_length=255, unique=True)  # Almacena el thread_id de la API
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Thread {self.thread_id} - Visitor {self.visitor.name}"

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
    )
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role.capitalize()} - {self.content[:50]}"

# Create your models here.
