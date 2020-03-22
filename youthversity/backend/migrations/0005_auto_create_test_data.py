# Generated by Django 3.0.4 on 2020-03-22 10:59

from django.db import migrations


def create_test_data(apps, _schema_editor):
    AuthUser = apps.get_model('auth', 'User')
    User = apps.get_model('backend', 'User')
    Feed = apps.get_model('backend', 'Feed')
    SchoolClass = apps.get_model('backend', 'SchoolClass')
    Post = apps.get_model('backend', 'Post')
    Comment = apps.get_model('backend', 'Comment')
    Subject = apps.get_model('backend', 'Subject')

    # first, we create a superuser
    # admin, admin
    superuser = AuthUser(
        username="admin",
        password="pbkdf2_sha256$180000$eKigTTXPAJxl$xVyeOjKHcfO2q9xD/ItpZ1G7lk+l2MLoNvJerKlat4M="
    )
    superuser.save()

    # then we need some other users

    # first a student
    # teststudent01, test123!
    f = Feed(interested_in_subjects="5")
    f.save()

    au = AuthUser(
        username="teststudent01",
        password="pbkdf2_sha256$180000$ML93s0s1r9pp$rHibqr0KGwlsX/1uFK7ljmW4dfzaPqIl/pm2fkzrFC8="
    )
    au.save()

    teststudent01 = User(auth_user=au, name="teststudent01", type="student", language="DE", feed=f)
    teststudent01.save()

    # then a teacher
    # testteacher01, test123!
    f = Feed(interested_in_subjects="1")
    f.save()

    # another a student
    # teststudent02, test123!
    f = Feed(interested_in_subjects="21")
    f.save()

    au = AuthUser(
        username="teststudent02",
        password="pbkdf2_sha256$180000$ML93s0s1r9pp$rHibqr0KGwlsX/1uFK7ljmW4dfzaPqIl/pm2fkzrFC8="
    )
    au.save()

    teststudent02 = User(auth_user=au, name="teststudent02", type="student", language="DE", feed=f)
    teststudent02.save()

    # then a teacher
    # testteacher01, test123!
    f = Feed(interested_in_subjects="1")
    f.save()

    au = AuthUser(
        username="testteacher01",
        password="pbkdf2_sha256$180000$ML93s0s1r9pp$rHibqr0KGwlsX/1uFK7ljmW4dfzaPqIl/pm2fkzrFC8="
    )
    au.save()

    teacher = User(auth_user=au, name="testteacher01", type="teacher", language="DE", feed=f)
    teacher.save()

    # now we create a class with all those
    sc = SchoolClass(
        name="9a",
        school_name="Test School",
    )
    sc.save()
    sc.teachers.add(teacher)
    sc.students.add(teststudent01, teststudent02)

    # and now some posts
    p = Post(
        content="""
        
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam rhoncus quam gravida lacus dictum, non auctor tortor fringilla. Fusce sed pretium sapien. Donec quis aliquet diam. Ut id tortor dignissim, viverra diam eu, consequat urna. Morbi euismod purus et enim molestie accumsan. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Suspendisse potenti.

Nunc laoreet turpis magna, vel tempor tellus egestas et. Phasellus laoreet ipsum et dignissim dapibus. Nulla vel eros vel metus posuere gravida a at risus. Phasellus eget elit facilisis, euismod sapien sed, congue turpis. Pellentesque pellentesque tellus sed nibh ultrices volutpat. Suspendisse eget imperdiet nisi. In id efficitur risus, non dignissim augue. Donec purus dolor, porta at nunc eget, varius elementum tellus. Nullam lacinia feugiat fermentum. Nulla sit amet orci ante. Nam placerat placerat erat, sit amet aliquet justo gravida non. Sed feugiat risus at lectus tincidunt, non congue lacus viverra. Integer sit amet elit sem. Sed cursus in velit eget aliquet.

Sed mi quam, porttitor et lacinia in, mattis ac metus. Morbi lacinia justo quis sem pharetra, at tempor mi pharetra. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Cras faucibus porttitor ante, sed cursus sem porttitor vitae. Nullam neque dui, vehicula sed efficitur nec, volutpat non enim. Ut cursus erat vitae mauris dignissim dapibus. Morbi ut elit rutrum, ullamcorper nulla quis, hendrerit justo. Ut sit amet elit laoreet, pellentesque dolor a, aliquet lorem. In fringilla lorem eu porta feugiat. Nam vitae nisl eget neque ornare pellentesque nec non metus. Mauris tempor orci tortor, vitae egestas turpis lacinia vel. In leo lectus, sagittis nec hendrerit at, tincidunt in sem. Mauris sit amet dictum ante. Donec velit magna, volutpat ut sapien vitae, vestibulum egestas risus. Vivamus vel justo venenatis, sollicitudin ipsum sit amet, lobortis urna.

Nullam luctus diam vitae augue interdum, nec pellentesque turpis rhoncus. Vestibulum finibus magna a est vulputate dapibus. Suspendisse potenti. Nullam tempus erat a imperdiet tristique. Maecenas vulputate, enim nec interdum cursus, nibh nulla pharetra elit, id eleifend metus elit vitae massa. Donec eu erat eget leo vulputate malesuada nec sed nulla. Aliquam ut sollicitudin ligula. Fusce et turpis ullamcorper, vulputate est vel, congue erat. Proin gravida velit at malesuada pharetra.

Nunc finibus mi a nunc efficitur, a pulvinar metus suscipit. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc et est ac purus pretium facilisis. Phasellus id urna tristique, aliquam felis eu, vulputate justo. Nulla facilisi. Vestibulum turpis massa, eleifend scelerisque sollicitudin at, ornare sed risus. Donec vel ullamcorper magna. Praesent scelerisque neque vel ultricies ornare. Curabitur augue mauris, convallis non ex quis, dictum suscipit augue. Aenean ullamcorper sem a aliquet sollicitudin. Etiam et arcu in lectus lacinia laoreet quis ac urna. Donec id mi quis velit mattis molestie sed et libero. Nulla et aliquam enim. 
        """,
        author=teststudent01,
        type="essay",
        title="Lorem Ipsum at its finest",
        subject=Subject.objects.all()[13],
        visibility="all",
        edited=True,
    )
    p.save()
    p.upvotes.add(teststudent01, teststudent02, teacher)

    p = Post(
        content="e = mc²",
        author=teststudent02,
        type="calculation",
        title="Einstein",
        subject=Subject.objects.all()[9],
        visibility="all",
        edited=False,
    )
    p.save()
    p.upvotes.add(teacher)

    c = Comment(
        author=teacher,
        type="comment",
        content="Your are genius!!!!",
        parent=p, edited=False
    )
    c.save()
    c.upvotes.add(teststudent02)


class Migration(migrations.Migration):
    dependencies = [
        ('backend', '0004_auto_20200321_2236'),
    ]

    operations = [
        migrations.RunPython(create_test_data)
    ]
