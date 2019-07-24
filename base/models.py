from django.contrib.admin.utils import quote
from django.db import models
from django.urls import reverse, NoReverseMatch


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @classmethod
    def full_path(cls):
        module = cls.__module__
        return module + '.' + cls.__name__

    def get_admin_url(self):
        """Returns the admin URL to edit this object
        """
        url_name = 'admin:{}_{}_change'.format(self._meta.app_label,
                                               self._meta.model_name)
        try:
            return reverse(url_name, args=(quote(self.pk),))
        except NoReverseMatch:
            pass

    class Meta:
        abstract = True
