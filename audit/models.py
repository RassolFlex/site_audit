from django.db import models


class AuditResult(models.Model):
    """Результаты экспресс-аудита"""
    
    site_url = models.URLField('URL сайта', unique=True)
    audit_date = models.DateTimeField('Дата аудита', auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Успешен'),
            ('failed', 'Не удачен')
        ],
        default='success'
    )
    
    class Meta:
        verbose_name = 'Результат аудита'
        verbose_name_plural = 'Результаты аудитов'
    
    def __str__(self):
        return f"{self.site_url} ({self.audit_date})"
