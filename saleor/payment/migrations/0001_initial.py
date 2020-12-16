# Generated by Django 3.1.2 on 2020-12-02 18:16

from decimal import Decimal
import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import saleor.payment


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('to_confirm', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('charge_status', models.CharField(choices=[('not-charged', 'Not charged'), ('pending', 'Pending'), ('partially-charged', 'Partially charged'), ('fully-charged', 'Fully charged'), ('partially-refunded', 'Partially refunded'), ('fully-refunded', 'Fully refunded'), ('refused', 'Refused'), ('cancelled', 'Cancelled')], default='not-charged', max_length=20)),
                ('token', models.CharField(blank=True, default='', max_length=512)),
                ('total', models.DecimalField(decimal_places=3, default=Decimal('0.0'), max_digits=12)),
                ('captured_amount', models.DecimalField(decimal_places=3, default=Decimal('0.0'), max_digits=12)),
                ('currency', models.CharField(max_length=3)),
                ('billing_email', models.EmailField(blank=True, max_length=254)),
                ('billing_first_name', models.CharField(blank=True, max_length=256)),
                ('billing_last_name', models.CharField(blank=True, max_length=256)),
                ('billing_company_name', models.CharField(blank=True, max_length=256)),
                ('billing_address_1', models.CharField(blank=True, max_length=256)),
                ('billing_address_2', models.CharField(blank=True, max_length=256)),
                ('billing_city', models.CharField(blank=True, max_length=256)),
                ('billing_city_area', models.CharField(blank=True, max_length=128)),
                ('billing_postal_code', models.CharField(blank=True, max_length=256)),
                ('billing_country_code', models.CharField(blank=True, max_length=2)),
                ('billing_country_area', models.CharField(blank=True, max_length=256)),
                ('cc_first_digits', models.CharField(blank=True, default='', max_length=6)),
                ('cc_last_digits', models.CharField(blank=True, default='', max_length=4)),
                ('cc_brand', models.CharField(blank=True, default='', max_length=40)),
                ('cc_exp_month', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('cc_exp_year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000)])),
                ('payment_method_type', models.CharField(blank=True, max_length=256)),
                ('customer_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('extra_data', models.TextField(blank=True, default='')),
                ('return_url', models.URLField(blank=True, null=True)),
                ('checkout', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='checkout.checkout')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='order.order')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(blank=True, default='', max_length=512)),
                ('kind', models.CharField(choices=[('auth', 'Authorization'), ('pending', 'Pending'), ('action_to_confirm', 'Action to confirm'), ('refund', 'Refund'), ('refund_ongoing', 'Refund in progress'), ('capture', 'Capture'), ('void', 'Void'), ('confirm', 'Confirm'), ('cancel', 'Cancel')], max_length=25)),
                ('is_success', models.BooleanField(default=False)),
                ('action_required', models.BooleanField(default=False)),
                ('action_required_data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('currency', models.CharField(max_length=3)),
                ('amount', models.DecimalField(decimal_places=3, default=Decimal('0.0'), max_digits=12)),
                ('error', models.CharField(choices=[(saleor.payment.TransactionError['INCORRECT_NUMBER'], 'incorrect_number'), (saleor.payment.TransactionError['INVALID_NUMBER'], 'invalid_number'), (saleor.payment.TransactionError['INCORRECT_CVV'], 'incorrect_cvv'), (saleor.payment.TransactionError['INVALID_CVV'], 'invalid_cvv'), (saleor.payment.TransactionError['INCORRECT_ZIP'], 'incorrect_zip'), (saleor.payment.TransactionError['INCORRECT_ADDRESS'], 'incorrect_address'), (saleor.payment.TransactionError['INVALID_EXPIRY_DATE'], 'invalid_expiry_date'), (saleor.payment.TransactionError['EXPIRED'], 'expired'), (saleor.payment.TransactionError['PROCESSING_ERROR'], 'processing_error'), (saleor.payment.TransactionError['DECLINED'], 'declined')], max_length=256, null=True)),
                ('customer_id', models.CharField(max_length=256, null=True)),
                ('gateway_response', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ('already_processed', models.BooleanField(default=False)),
                ('searchable_key', models.CharField(blank=True, max_length=512, null=True)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='payment.payment')),
            ],
            options={
                'ordering': ('pk',),
            },
        ),
    ]