# Generated by Django 3.1.8 on 2021-07-16 01:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('entire_order', 'Entire order'), ('shipping', 'Shipping'), ('specific_product', 'Specific products, collections and categories')], default='entire_order', max_length=20)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(db_index=True, max_length=12, unique=True)),
                ('usage_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('used', models.PositiveIntegerField(default=0, editable=False)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('apply_once_per_order', models.BooleanField(default=False)),
                ('apply_once_per_customer', models.BooleanField(default=False)),
                ('discount_value_type', models.CharField(choices=[('fixed', 'TWD'), ('percentage', '%')], default='fixed', max_length=10)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=12)),
                ('min_spent_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('min_checkout_items_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='product.Category')),
                ('collections', models.ManyToManyField(blank=True, to='product.Collection')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
            options={
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('fixed', 'TWD'), ('percentage', '%')], default='fixed', max_length=10)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('categories', models.ManyToManyField(blank=True, to='product.Category')),
                ('collections', models.ManyToManyField(blank=True, to='product.Collection')),
                ('products', models.ManyToManyField(blank=True, to='product.Product')),
            ],
            options={
                'ordering': ('name', 'pk'),
                'permissions': (('manage_discounts', 'Manage sales and vouchers.'),),
            },
        ),
        migrations.CreateModel(
            name='VoucherTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(max_length=10)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='discount.voucher')),
            ],
            options={
                'ordering': ('language_code', 'voucher'),
                'unique_together': {('language_code', 'voucher')},
            },
        ),
        migrations.CreateModel(
            name='VoucherCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_email', models.EmailField(max_length=254)),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to='discount.voucher')),
            ],
            options={
                'ordering': ('voucher', 'customer_email'),
                'unique_together': {('voucher', 'customer_email')},
            },
        ),
    ]