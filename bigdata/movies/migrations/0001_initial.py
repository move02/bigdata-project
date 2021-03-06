# Generated by Django 2.1.5 on 2019-05-26 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('movie_id', models.IntegerField()),
                ('imdb_id', models.CharField(blank=True, max_length=200)),
                ('overview', models.CharField(max_length=200)),
                ('popularity', models.FloatField(default=0)),
                ('poster', models.URLField()),
                ('release_date', models.DateField()),
                ('revenue', models.IntegerField(default=0)),
                ('runtime', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=200)),
                ('tagline', models.CharField(max_length=200)),
                ('video', models.BooleanField()),
                ('vote_avg', models.FloatField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('original_language', models.CharField(max_length=200)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Collection')),
                ('genres', models.ManyToManyField(to='movies.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='ProductionCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductionCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('movie_id', models.IntegerField()),
                ('rating', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SpokenLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_id', models.IntegerField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='production_companies',
            field=models.ManyToManyField(to='movies.ProductionCompany'),
        ),
        migrations.AddField(
            model_name='movie',
            name='production_countries',
            field=models.ManyToManyField(to='movies.ProductionCountry'),
        ),
        migrations.AddField(
            model_name='movie',
            name='spoken_languages',
            field=models.ManyToManyField(to='movies.SpokenLanguage'),
        ),
    ]
