import uuid
import djclick as click
from django.contrib.auth import get_user_model
from django_middleware_global_request_example.models import Book
from django_middleware_global_request import GlobalRequest


@click.command()
@click.option("-n", "--number", type=int, default=10)
def create(number):
    User = get_user_model()
    admin = User()
    admin.username = "admin" + uuid.uuid4().hex
    admin.set_password(uuid.uuid4().hex)
    admin.is_active = True
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()

    with GlobalRequest(user=admin):
        for i in range(number):
            book = Book(name="book{idx}".format(idx=i+1))
            book.save()
            print(i, book.name, book.author.username)
            assert book.author.pk == admin.pk
