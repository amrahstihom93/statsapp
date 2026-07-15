from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField


class mlearn(models.Model):
    """Stores saved machine learning model metadata and results."""
    mlearn_id = models.CharField(max_length=250, blank=True)
    mlearn_name = models.CharField(max_length=250, blank=True)
    mlearn_method = models.CharField(max_length=250, blank=True, default='linear_regression')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # parameters stores model metrics (r2, p-value, etc.) as JSON
    parameters = JSONField(default=dict)
    test = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.mlearn_name

    class Meta:
        verbose_name = 'ML Model'
        verbose_name_plural = 'ML Models'
