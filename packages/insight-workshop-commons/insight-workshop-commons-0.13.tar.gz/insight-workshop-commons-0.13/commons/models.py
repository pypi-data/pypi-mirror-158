import uuid
from cuser.fields import CurrentUserField
from django.core import checks
from django.core.exceptions import FieldDoesNotExist
from django.db import models

from .utils import unique_slugify


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = '-updated_at',
        abstract = True


class CuserModel(models.Model):
    created_by = CurrentUserField(
        add_only=True,
        related_name="%(app_label)s_%(class)s_created",
        on_delete=models.SET_NULL,
        null=True
    )

    updated_by = CurrentUserField(
        related_name="%(app_label)s_%(class)s_modified",
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        abstract = True

    @classmethod
    def _check_fields(cls, **kwargs):
        # register a check so that developers wont change the type of
        # created_by or updated_by during subclassing
        errors = super()._check_fields()
        try:
            created_by = cls._meta.get_field('created_by')
        except FieldDoesNotExist:
            created_by = None  # means created_by has been removed, so just ignore it
        if not (isinstance(created_by, CurrentUserField) or created_by is None):
            errors.append(
                checks.Error(
                    "created_by should be either CurrentUserField or None, currently is %s" %
                    type(created_by),
                    id='BootCamp1',
                    obj=cls
                )
            )
        try:
            updated_by = cls._meta.get_field('updated_by')
        except FieldDoesNotExist:
            updated_by = None  # means created_by has been removed, so just ignore it
        if not (isinstance(updated_by, CurrentUserField) or updated_by is None):
            errors.append(
                checks.Error(
                    "updated_by should be either CurrentUserField or None, currently is %s" %
                    type(updated_by),
                    id='BootCamp1',
                    obj=cls
                )
            )
        return errors


class BaseModel(CuserModel, TimeStampModel):
    class Meta:
        ordering = '-updated_at',
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super().save(force_insert=False, force_update=False, using=None,
                            update_fields=None)


class SlugModel(models.Model):
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    class Meta:
        abstract = True

    def _get_slug_text(self):
        assert any([hasattr(self, 'name'), hasattr(self, 'title')])
        slug_text = ''
        if hasattr(self, 'name'):
            slug_text = self.name.lower()
        elif hasattr(self, 'title'):
            slug_text = self.title.lower()
        return slug_text

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = self._get_slug_text()
            unique_slugify(self, slug_text)
        return super().save(*args, **kwargs)


class UUIDBaseModel(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta(BaseModel.Meta):
        abstract = True


def get_file_upload_path(_, filename):
    import os
    extension = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), extension)
    return os.path.join('uploads/', filename)


class FileUpload(UUIDBaseModel):
    file = models.FileField(upload_to=get_file_upload_path)
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# This table should only be inherited in the Speciality model ('speciality.models') because BaseModel was not inherited
# previously in the Speciality model and it has to be inherited later (because table had no timestamp field)
class NullableTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = '-updated_at',
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

