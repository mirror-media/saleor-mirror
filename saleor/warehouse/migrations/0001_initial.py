# Generated by Django 3.1.2 on 2020-12-02 18:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shipping', '0001_initial'),
        ('order', '0001_initial'),
        ('product', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.address')),
                ('shipping_zones', models.ManyToManyField(blank=True, related_name='warehouses', to='shipping.ShippingZone')),
            ],
            options={
                'ordering': ('-slug',),
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='product.productvariant')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.warehouse')),
            ],
            options={
                'ordering': ('pk',),
                'unique_together': {('warehouse', 'product_variant')},
            },
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_allocated', models.PositiveIntegerField(default=0)),
                ('order_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='order.orderline')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocations', to='warehouse.stock')),
            ],
            options={
                'ordering': ('pk',),
                'unique_together': {('order_line', 'stock')},
            },
        ),
    ]