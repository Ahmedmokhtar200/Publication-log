# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Action(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'action'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Collaborator(models.Model):
    project = models.ForeignKey('Project', models.DO_NOTHING)
    email = models.ForeignKey('Email', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collaborator'


class Conference(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    islisted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'conference.html'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Domain(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domain'


class Email(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'email'


class Event(models.Model):
    action = models.ForeignKey(Action, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class EventProposal(models.Model):
    event = models.OneToOneField(Event, models.DO_NOTHING,
                                 primary_key=True)  # The composite primary key (event_id, proposal_id, project_edit) found, that is not supported. The first column is selected.
    proposal = models.ForeignKey('Proposal', models.DO_NOTHING)
    project_edit = models.ForeignKey('Proposal', models.DO_NOTHING, db_column='project_edit', to_field='project_edit',
                                     related_name='eventproposal_project_edit_set')

    class Meta:
        managed = False
        db_table = 'event_proposal'
        unique_together = (('event', 'proposal', 'project_edit'),)


class EventProposalInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    event_proposal_id = models.ForeignKey(EventProposal, on_delete=models.CASCADE)


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=255)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class Human(models.Model):
    id = models.IntegerField(primary_key=True)  # The composite primary key (id, edit) found, that is not supported. The first column is selected.
    first_name = models.CharField(max_length=45, blank=True, null=True)
    last_name = models.CharField(max_length=45, blank=True, null=True)
    city = models.CharField(max_length=2, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'human_info'
        unique_together = (('id', 'edit'),)

    def __str__(self):
        return self.first_name+''+self.last_name


class HumanInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    human_id = models.ForeignKey(Human, on_delete=models.CASCADE)


class HumanEmail(models.Model):
    human = models.OneToOneField(Human, models.DO_NOTHING,
                                 primary_key=True)  # The composite primary key (human_id, human_edit, email_id) found, that is not supported. The first column is selected.
    human_edit = models.ForeignKey(Human, models.DO_NOTHING, db_column='human_edit', to_field='edit',
                                   related_name='humanemail_human_edit_set')
    email = models.ForeignKey(Email, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'human_email'
        unique_together = (('human_info', 'human_edit', 'email'),)


class Migrations(models.Model):
    migration = models.CharField(max_length=255)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class PasswordResets(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class PersonalAccessTokens(models.Model):
    id = models.BigAutoField(primary_key=True)
    tokenable_type = models.CharField(max_length=255)
    tokenable_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=255)
    token = models.CharField(unique=True, max_length=64)
    abilities = models.TextField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personal_access_tokens'


class Project(models.Model):
    id = models.IntegerField(
        primary_key=True)  # The composite primary key (id, edit) found, that is not supported. The first column is selected.
    title = models.CharField(max_length=155, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    scientific_case = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'project'
        unique_together = (('id', 'edit'),)


class ProjectInfo:
    id = models.IntegerField(primary_key=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)


class Proposal(models.Model):
    id = models.IntegerField(
        primary_key=True)  # The composite primary key (id, project_edit) found, that is not supported. The first column is selected.
    project = models.ForeignKey(Project, models.DO_NOTHING)
    # project_edit = models.ForeignKey(Project, models.DO_NOTHING, db_column='project_edit', to_field='edit',
    #                                  related_name='proposal_project_edit_set')
    duration = models.IntegerField(blank=True, null=True)
    submitted = models.TextField(blank=True, null=True)  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proposal'
        unique_together = (('id', 'project_edit'),)


class ProposalInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    proposal_id = models.ForeignKey(Proposal, on_delete=models.CASCADE)


class Publication(models.Model):
    project = models.ForeignKey(Project, models.DO_NOTHING)
    project_edit = models.ForeignKey(Project, models.DO_NOTHING, db_column='project_edit', to_field='edit',
                                     related_name='publication_project_edit_set')
    conference = models.ForeignKey(Conference, models.DO_NOTHING)
    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=225)
    year = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    file = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'publication'

    def __str__(self):
        return self.title


class PublicationAuthor(models.Model):
    publication = models.OneToOneField(Publication, models.DO_NOTHING,
                                       primary_key=True)  # The composite primary key (publication_id, human_id, human_edit) found, that is not supported. The first column is selected.
    human = models.ForeignKey(Human, models.DO_NOTHING)
    human_edit = models.ForeignKey(Human, models.DO_NOTHING, db_column='human_edit', to_field='edit',
                                   related_name='publicationauthor_human_edit_set')

    class Meta:
        managed = False
        db_table = 'publication_author'
        unique_together = (('publication', 'human_info', 'human_edit'),)


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.name
