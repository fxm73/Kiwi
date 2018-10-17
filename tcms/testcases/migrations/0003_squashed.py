# Generated by Django 2.1.2 on 2018-10-18 11:50

import datetime
from django.conf import settings
from django.db import migrations, models


def forward_duration_field(apps, schema_editor):
    TestCase = apps.get_model('testcases', 'TestCase')

    for tc in TestCase.objects.all():
        tc.estimated_time_new = datetime.timedelta(seconds=tc.estimated_time)
        tc.save()


def reverse_duration_field(apps, schema_editor):
    TestCase = apps.get_model('testcases', 'TestCase')

    for tc in TestCase.objects.all():
        tc.estimated_time = tc.estimated_time_new.total_seconds()
        tc.save()


def forward_cc_list(apps, schema_editor):
    TestCaseEmailSettings = apps.get_model('testcases', 'TestCaseEmailSettings')
    Contact = apps.get_model('testcases', 'Contact')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Site = apps.get_model('sites', 'Site')

    content_type = ContentType.objects.get_for_model(TestCaseEmailSettings)
    site = Site.objects.get_current()

    for email_settings in TestCaseEmailSettings.objects.all():
        contacts = Contact.objects.filter(
            content_type=content_type.pk,
            object_pk=email_settings.case.pk,
            site=site.pk).all()

        new_cc = []
        for contact in contacts:
            new_cc.append(contact.email)

        email_settings.new_cc_list = ','.join(new_cc)
        email_settings.save()


class Migration(migrations.Migration):
    # because renaming tables in transaction fails while testing on SQLite
    atomic = False

    dependencies = [
        ('testcases', '0002_squashed'),
        ('management', '0002_squashed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestCaseCategory',
            new_name='Category',
        ),
        migrations.AlterField(
            model_name='TestCase',
            name='category',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE,
                                    related_name='category_case', to='testcases.Category'),
        ),
        migrations.AlterField(
            model_name='TestCaseTag',
            name='tag',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='management.Tag'),
        ),
        migrations.AlterField(
            model_name='TestCase',
            name='tag',
            field=models.ManyToManyField(
                related_name='case', through='testcases.TestCaseTag', to='management.Tag'),
        ),
        migrations.RenameModel(
            old_name='TestCaseBug',
            new_name='Bug',
        ),
        migrations.RenameModel(
            old_name='TestCaseBugSystem',
            new_name='BugSystem',
        ),
        migrations.AlterField(
            model_name='Bug',
            name='bug_system',
            field=models.ForeignKey(
                default=1, on_delete=models.deletion.CASCADE, to='testcases.BugSystem'),
        ),
        migrations.AddField(
            model_name='testcase',
            name='estimated_time_new',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),

        migrations.RunPython(forward_duration_field, reverse_duration_field),

        migrations.RemoveField(
            model_name='testcase',
            name='estimated_time',
        ),
        migrations.RenameField(
            model_name='testcase',
            old_name='estimated_time_new',
            new_name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='testcasetext',
            name='action_checksum',
        ),
        migrations.RemoveField(
            model_name='testcasetext',
            name='breakdown_checksum',
        ),
        migrations.RemoveField(
            model_name='testcasetext',
            name='effect_checksum',
        ),
        migrations.RemoveField(
            model_name='testcasetext',
            name='setup_checksum',
        ),
        migrations.AlterModelOptions(
            name='testcasestatus',
            options={'verbose_name': 'Test case status',
                     'verbose_name_plural': 'Test case statuses'},
        ),
        migrations.AlterModelTable(
            name='bug',
            table=None,
        ),
        migrations.AlterModelTable(
            name='bugsystem',
            table=None,
        ),
        migrations.AlterModelTable(
            name='category',
            table=None,
        ),
        migrations.AlterModelTable(
            name='contact',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcase',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcasecomponent',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcaseplan',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcasestatus',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcasetag',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcasetext',
            table=None,
        ),
        migrations.CreateModel(
            name='HistoricalTestCase',
            fields=[
                ('case_id', models.IntegerField(blank=True, db_index=True)),
                ('create_date', models.DateTimeField(blank=True,
                                                     db_column='creation_date',
                                                     editable=False)),
                ('is_automated', models.IntegerField(db_column='isautomated', default=0)),
                ('is_automated_proposed', models.BooleanField(default=False)),
                ('script', models.TextField(blank=True, null=True)),
                ('arguments', models.TextField(blank=True, null=True)),
                ('extra_link', models.CharField(blank=True,
                                                default=None,
                                                max_length=1024,
                                                null=True)),
                ('summary', models.CharField(max_length=255)),
                ('requirement', models.CharField(blank=True, max_length=255, null=True)),
                ('alias', models.CharField(blank=True, max_length=255)),
                ('estimated_time', models.DurationField(default=datetime.timedelta(0))),
                ('notes', models.TextField(blank=True, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[
                 ('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('author', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                             on_delete=models.deletion.DO_NOTHING,
                                             related_name='+',
                                             to=settings.AUTH_USER_MODEL)),
                ('case_status', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                  on_delete=models.deletion.DO_NOTHING,
                                                  related_name='+',
                                                  to='testcases.TestCaseStatus')),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                               on_delete=models.deletion.DO_NOTHING,
                                               related_name='+', to='testcases.Category')),
                ('default_tester', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                     on_delete=models.deletion.DO_NOTHING,
                                                     related_name='+',
                                                     to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL,
                                                   related_name='+', to=settings.AUTH_USER_MODEL)),
                ('priority', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                               on_delete=models.deletion.DO_NOTHING,
                                               related_name='+', to='management.Priority')),
                ('reviewer', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                               on_delete=models.deletion.DO_NOTHING,
                                               related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical test case',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.AlterField(
            model_name='testcase',
            name='case_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='testcaseemailsettings',
            name='new_cc_list',
            field=models.TextField(default=''),
        ),

        migrations.RunPython(forward_cc_list),

        migrations.AlterIndexTogether(
            name='contact',
            index_together=set(),
        ),
        migrations.RemoveField(
            model_name='contact',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='site',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.RenameField(
            model_name='testcaseemailsettings',
            old_name='new_cc_list',
            new_name='cc_list',
        ),
        migrations.RemoveField(
            model_name='historicaltestcase',
            name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='testcase',
            name='estimated_time',
        ),
        migrations.RemoveField(
            model_name='testcasetag',
            name='user',
        ),
    ]
