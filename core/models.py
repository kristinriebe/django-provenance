from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create TAP_SCHEMA classes here, 
# see http://www.ivoa.net/documents/TAP/20160428/WD-TAP-1.1-20160428.html
# for the IVOA TAP specification
@python_2_unicode_compatible
class TAP_SCHEMA_schemas(models.Model):
    schema_name = models.CharField(max_length=256)
    utype = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    
    def __str__(self):
        return self.schema_name


@python_2_unicode_compatible
class TAP_SCHEMA_tables(models.Model):
    schema_name = models.CharField(max_length=256)
    table_name = models.CharField(max_length=256)
    table_type = models.CharField(max_length=256)  # ???
    utype = models.CharField(max_length=256, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    table_index = models.IntegerField(null=True)  # used for sorting tables, 0 = first table, 1 = second table etc.

    def __str__(self):
        return self.table_name


@python_2_unicode_compatible
class TAP_SCHEMA_columns(models.Model):
    table_name = models.CharField(max_length=256)
    column_name = models.CharField(max_length=256)
    datatype = models.CharField(max_length=256)
    arraysize = models.IntegerField(null=True)
    size = models.IntegerField(null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    utype = models.CharField(max_length=256, blank=True, null=True)
    unit = models.CharField(max_length=256, blank=True, null=True)
    ucd = models.CharField(max_length=256, blank=True, null=True)
    indexed = models.BooleanField(default=False)
    principal = models.BooleanField(default=True)  # mark the main important columns
    std = models.BooleanField(default=False) # column is defined by some standard
    column_index = models.NullBooleanField(default=False, null=True)

    def __str__(self):
        return self.column_name


@python_2_unicode_compatible
class TAP_SCHEMA_keys(models.Model):
    # describes foreign key relations between tables
    key_id = models.CharField(max_length=256)
    from_table = models.CharField(max_length=256)
    target_table = models.CharField(max_length=256)
    description = models.CharField(max_length=256, blank=True, null=True)
    utype = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.key_id


@python_2_unicode_compatible
class TAP_SCHEMA_key_columns(models.Model):
    # which columns can be used to join the tables; there may be more than one way to join tables
    key_id = models.CharField(max_length=256)
    from_column = models.CharField(max_length=256)
    target_column = models.CharField(max_length=256)

    def __str__(self):
        return self.key_id
