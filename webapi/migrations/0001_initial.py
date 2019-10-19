# Generated by Django 2.2.6 on 2019-10-19 14:02

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Geners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.CharField(max_length=50, verbose_name='reference_id')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'unique_together': {('reference_id', 'name')},
            },
        ),
        migrations.CreateModel(
            name='WatchedList',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='code nmae')),
            ],
        ),
        migrations.CreateModel(
            name='SpokenLanguages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_639_1', models.CharField(max_length=250, verbose_name='iso_639_1')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'unique_together': {('iso_639_1', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ProductionCountries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iso_3166_1', models.CharField(max_length=250, verbose_name='iso_3166_1')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
            ],
            options={
                'unique_together': {('iso_3166_1', 'name')},
            },
        ),
        migrations.CreateModel(
            name='ProductionCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='name')),
                ('reference_id', models.CharField(max_length=50, verbose_name='reference_id')),
                ('logo_path', models.CharField(blank=True, max_length=250, null=True, verbose_name='logo_path')),
                ('origin_country', models.CharField(max_length=250, verbose_name='origin_country')),
            ],
            options={
                'unique_together': {('name', 'reference_id', 'logo_path', 'origin_country')},
            },
        ),
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adult', models.BooleanField(default=False, verbose_name='adult')),
                ('backdrop_path', models.CharField(blank=True, max_length=250, null=True, verbose_name='backdrop path')),
                ('budget', models.BigIntegerField(verbose_name='budget')),
                ('belongs_to_collection', jsonfield.fields.JSONField(blank=True, null=True)),
                ('home_page', models.CharField(blank=True, max_length=250, null=True, verbose_name='home page')),
                ('reference_id', models.CharField(max_length=250, unique=True, verbose_name='reference id')),
                ('imdb_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='imdb id')),
                ('original_language', models.CharField(max_length=250, verbose_name='original language')),
                ('original_title', models.CharField(max_length=250, verbose_name='original title')),
                ('overview', models.TextField(blank=True, null=True, verbose_name='overview')),
                ('popularity', models.BigIntegerField(verbose_name='popularity')),
                ('poster_path', models.CharField(blank=True, max_length=250, null=True, verbose_name='poster path')),
                ('release_date', models.DateField(verbose_name='release date')),
                ('revenue', models.BigIntegerField(blank=True, null=True, verbose_name='revenue')),
                ('runtime', models.IntegerField(blank=True, null=True, verbose_name='run time')),
                ('status', models.CharField(max_length=250, verbose_name='status')),
                ('tagline', models.CharField(blank=True, max_length=250, null=True, verbose_name='tag line')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('video', models.BooleanField(default=False, verbose_name='vedio')),
                ('vote_average', models.BigIntegerField(verbose_name='vote average')),
                ('vote_count', models.BigIntegerField(verbose_name='vote count')),
                ('geners', models.ManyToManyField(to='webapi.Geners')),
                ('production_company', models.ManyToManyField(to='webapi.ProductionCompany')),
                ('production_countries', models.ManyToManyField(to='webapi.ProductionCountries')),
                ('spoken_languages', models.ManyToManyField(to='webapi.SpokenLanguages')),
            ],
        ),
        migrations.CreateModel(
            name='WatchedMovies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_list', to='webapi.WatchedList')),
                ('movies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watched_user', to='webapi.Movies')),
            ],
            options={
                'unique_together': {('code', 'movies')},
            },
        ),
    ]