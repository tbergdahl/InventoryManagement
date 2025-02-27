# Generated by Django 4.2.6 on 2025-02-27 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='NonPerishableInventoryItem',
            fields=[
                ('inventoryitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventory.inventoryitem')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('inventory.inventoryitem',),
        ),
        migrations.CreateModel(
            name='PerishableInventoryItem',
            fields=[
                ('inventoryitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='inventory.inventoryitem')),
                ('expiry_date', models.DateField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('inventory.inventoryitem',),
        ),
    ]
