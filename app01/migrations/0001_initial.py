# Generated by Django 2.0 on 2019-08-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=225)),
                ('role_type', models.CharField(choices=[('scriptwriter', '编剧'), ('Administrator', '管理员'), ('actor', '艺人'), ('audit', '审核')], default='艺人', max_length=225)),
                ('register_time', models.DateField(auto_now_add=True)),
                ('user_state', models.CharField(choices=[('terminate_agreement ', '解约'), ('normal', '正常')], default='正常', max_length=225)),
            ],
        ),
    ]
