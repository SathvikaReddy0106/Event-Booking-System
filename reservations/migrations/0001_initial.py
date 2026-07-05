
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seats', '0001_initial'),
        ('showtimes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('HELD', 'Held'), ('BOOKED', 'Booked'), ('CANCELLED', 'Cancelled')], default='HELD', max_length=20)),
                ('hold_expiry', models.DateTimeField(blank=True, null=True)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='seats.seat')),
                ('showtime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='showtimes.showtime')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'reservations',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['showtime'], name='reservation_showtim_b0af89_idx'), models.Index(fields=['status'], name='reservation_status_a87326_idx'), models.Index(fields=['user'], name='reservation_user_id_94b298_idx')],
                'constraints': [models.UniqueConstraint(fields=('seat', 'showtime'), name='unique_seat_showtime')],
            },
        ),
    ]
