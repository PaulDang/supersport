# Generated by Django 4.2.13 on 2024-05-23 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=150)),
                ('lastName', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('phone', models.CharField(max_length=12)),
                ('address', models.TextField()),
                ('total_price', models.FloatField()),
                ('payment_mode', models.CharField(max_length=150)),
                ('status', models.CharField(choices=[('Created', 'Đã tạo'), ('Shipping', 'Đang vận chuyển'), ('Completed', 'Hoàn thành')], default='Created', max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Đơn hàng',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('total_price', models.FloatField(editable=False, null=True)),
                ('size', models.CharField(max_length=20, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name_plural': 'Chi tiết đơn hàng',
            },
        ),
    ]
