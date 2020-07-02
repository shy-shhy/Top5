{'a': 1}
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
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
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class ClickNews(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'click_news'


class Comment(models.Model):
    url = models.CharField(max_length=60, blank=True, null=True)
    open_id = models.CharField(max_length=28, blank=True, null=True)
    nickname = models.CharField(max_length=60, blank=True, null=True)
    avatar = models.CharField(max_length=150, blank=True, null=True)
    value = models.CharField(max_length=400, blank=True, null=True)
    comment_id = models.CharField(max_length=50, blank=True, null=True)
    like_count = models.SmallIntegerField(blank=True, null=True)
    id = models.SmallIntegerField(primary_key=True)
    cur = models.DateTimeField(blank=True, null=True)
    verify = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class CommentPrice(models.Model):
    open_id = models.CharField(max_length=50, blank=True, null=True)
    comment_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment_price'


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


class DongqiudiJijin(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    thumb = models.CharField(max_length=255, blank=True, null=True)
    mp4 = models.CharField(max_length=255, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)
    shoucang = models.SmallIntegerField(blank=True, null=True)
    like = models.SmallIntegerField(blank=True, null=True)
    fenxiang = models.SmallIntegerField(blank=True, null=True)
    dianji = models.SmallIntegerField(blank=True, null=True)
    han = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dongqiudi_jijin'


class DongqiudiVidio(models.Model):
    id = models.CharField(max_length=100)
    title = models.CharField(max_length=255, blank=True, null=True)
    thumb = models.CharField(max_length=255)
    mp4 = models.CharField(max_length=100, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)
    shoucang = models.SmallIntegerField(blank=True, null=True)
    like = models.SmallIntegerField(blank=True, null=True)
    fenxiang = models.SmallIntegerField(blank=True, null=True)
    dianji = models.SmallIntegerField(blank=True, null=True)
    no = models.AutoField(db_column='No', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dongqiudi_vidio'
        unique_together = (('no', 'id'),)


class GameMatch(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    url = models.CharField(max_length=15, blank=True, null=True)
    team_a = models.CharField(max_length=40, blank=True, null=True)
    team_a_logo = models.CharField(max_length=90, blank=True, null=True)
    team_b = models.CharField(max_length=40, blank=True, null=True)
    team_b_logo = models.CharField(max_length=90, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_match'


class HomeInformation(models.Model):
    user_count = models.SmallIntegerField(blank=True, null=True)
    day_user = models.SmallIntegerField(blank=True, null=True)
    wechat = models.CharField(max_length=11, blank=True, null=True)
    show = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_information'


class Jieshao(models.Model):
    yingchao = models.CharField(max_length=255, blank=True, null=True)
    xijia = models.CharField(max_length=255, blank=True, null=True)
    yijia = models.CharField(max_length=255, blank=True, null=True)
    dejia = models.CharField(max_length=255, blank=True, null=True)
    fajia = models.CharField(max_length=255, blank=True, null=True)
    id = models.SmallIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'jieshao'


class NewsPriase(models.Model):
    url = models.CharField(max_length=55, blank=True, null=True)
    open_id = models.CharField(max_length=28, blank=True, null=True)
    id = models.SmallIntegerField(primary_key=True)
    avatar = models.CharField(max_length=150, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_priase'


class NurIndex(models.Model):
    uid = models.CharField(primary_key=True, max_length=50)
    title = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)
    count = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nur_index'


class NurNews(models.Model):
    url = models.CharField(primary_key=True, max_length=50)
    p_0 = models.CharField(db_column='P_0', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    p_1 = models.CharField(max_length=1500, blank=True, null=True)
    p_2 = models.TextField(blank=True, null=True)
    p_3 = models.TextField(blank=True, null=True)
    p_4 = models.TextField(blank=True, null=True)
    p_5 = models.TextField(blank=True, null=True)
    p_6 = models.TextField(blank=True, null=True)
    p_7 = models.TextField(blank=True, null=True)
    p_8 = models.TextField(blank=True, null=True)
    p_9 = models.TextField(db_column='P_9', blank=True, null=True)  # Field name made lowercase.
    p_10 = models.TextField(db_column='P_10', blank=True, null=True)  # Field name made lowercase.
    p_11 = models.TextField(db_column='P_11', blank=True, null=True)  # Field name made lowercase.
    p_12 = models.TextField(db_column='P_12', blank=True, null=True)  # Field name made lowercase.
    p_13 = models.TextField(db_column='P_13', blank=True, null=True)  # Field name made lowercase.
    p_14 = models.TextField(db_column='P_14', blank=True, null=True)  # Field name made lowercase.
    p_15 = models.TextField(db_column='P_15', blank=True, null=True)  # Field name made lowercase.
    p_16 = models.TextField(db_column='P_16', blank=True, null=True)  # Field name made lowercase.
    p_17 = models.TextField(db_column='P_17', blank=True, null=True)  # Field name made lowercase.
    p_18 = models.TextField(db_column='P_18', blank=True, null=True)  # Field name made lowercase.
    p_19 = models.TextField(db_column='P_19', blank=True, null=True)  # Field name made lowercase.
    p_20 = models.TextField(db_column='P_20', blank=True, null=True)  # Field name made lowercase.
    p_21 = models.TextField(db_column='P_21', blank=True, null=True)  # Field name made lowercase.
    p_22 = models.TextField(db_column='P_22', blank=True, null=True)  # Field name made lowercase.
    p_23 = models.TextField(db_column='P_23', blank=True, null=True)  # Field name made lowercase.
    p_24 = models.TextField(db_column='P_24', blank=True, null=True)  # Field name made lowercase.
    p_25 = models.TextField(db_column='P_25', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(max_length=255, blank=True, null=True)
    root = models.CharField(max_length=40, blank=True, null=True)
    pub_time = models.DateTimeField(blank=True, null=True)
    a = models.CharField(max_length=100, blank=True, null=True)
    b = models.CharField(max_length=100, blank=True, null=True)
    c = models.CharField(max_length=100, blank=True, null=True)
    d = models.CharField(max_length=100, blank=True, null=True)
    e = models.CharField(max_length=100, blank=True, null=True)
    p = models.CharField(max_length=40, blank=True, null=True)
    span = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nur_news'


class NurSlideShow(models.Model):
    img = models.CharField(max_length=128, blank=True, null=True)
    text = models.CharField(max_length=128, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'nur_slide_show'


class Player(models.Model):
    leage = models.CharField(max_length=50, blank=True, null=True)
    be_from = models.CharField(max_length=50, blank=True, null=True)
    ranking = models.IntegerField(blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    team = models.CharField(max_length=100, blank=True, null=True)
    count = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class Schedule(models.Model):
    start_paly = models.DateTimeField(blank=True, null=True)
    round_name = models.CharField(max_length=30, blank=True, null=True)
    team_a_name = models.CharField(db_column='team_A_name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    team_a_logo = models.CharField(db_column='team_A_logo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    team_b_name = models.CharField(db_column='team_B_name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    team_b_logo = models.CharField(db_column='team_B_logo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    fs_a = models.CharField(db_column='fs_A', max_length=3, blank=True, null=True)  # Field name made lowercase.
    fs_b = models.CharField(db_column='fs_B', max_length=3, blank=True, null=True)  # Field name made lowercase.
    match_title = models.CharField(max_length=60, blank=True, null=True)
    date_utc = models.CharField(max_length=12, blank=True, null=True)
    time_utc = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'schedule'


class Score(models.Model):
    leage = models.CharField(max_length=30, blank=True, null=True)
    ranking = models.SmallIntegerField(blank=True, null=True)
    team_name = models.CharField(max_length=30, blank=True, null=True)
    matches_won = models.CharField(max_length=4, blank=True, null=True)
    matches_drew = models.CharField(max_length=4, blank=True, null=True)
    matches_win = models.CharField(max_length=4, blank=True, null=True)
    matches = models.CharField(max_length=5, blank=True, null=True)
    score = models.CharField(max_length=4, blank=True, null=True)
    logo = models.CharField(max_length=100, blank=True, null=True)
    goal = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'score'


class Shoucang(models.Model):
    open_id = models.CharField(max_length=28)
    url = models.CharField(max_length=155, blank=True, null=True)
    id = models.SmallIntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'shoucang'


class Team(models.Model):
    leage = models.CharField(max_length=30, blank=True, null=True)
    be_from = models.CharField(max_length=30, blank=True, null=True)
    team = models.CharField(max_length=30, blank=True, null=True)
    ranking = models.SmallIntegerField(blank=True, null=True)
    img = models.CharField(max_length=150, blank=True, null=True)
    count = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'team'


class User(models.Model):
    open_id = models.CharField(max_length=28)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    gender = models.SmallIntegerField(blank=True, null=True)
    province = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        unique_together = (('id', 'open_id'),)


class VidioUser(models.Model):
    open_id = models.CharField(max_length=28, blank=True, null=True)
    vidio_url = models.CharField(max_length=100, blank=True, null=True)
    like = models.SmallIntegerField(blank=True, null=True)
    shoucang = models.SmallIntegerField(blank=True, null=True)
    fanxiang = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vidio_user'
