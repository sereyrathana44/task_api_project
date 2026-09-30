from django.db import models


class Task(models.Model):
    """
    ម៉ូដែលសាមញ្ញមួយសម្រាប់តំណាងឱ្យកិច្ចការមួយ (Task) —
    ល្អសម្រាប់បង្ហាញពីរបៀបបំប្លែងម៉ូដែលទៅជា JSON API ដោយប្រើ DRF Serializers។
    """

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
