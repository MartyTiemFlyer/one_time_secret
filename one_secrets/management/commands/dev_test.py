from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '-- hello world -- '

    def handle(self, *args, **options):
        from one_secrets.models import Secret
        from django.utils import timezone
        from datetime import timedelta

        self.stdout.write("-- 1 --")

        s1 = Secret(secret="секрет_первый", expires_at=timezone.now() + timedelta(minutes=5))
        s1.save()
        test1 = s1.read_once()
        self.stdout.write(str(s1))
        self.stdout.write(test1)

        self.stdout.write("-- 2 --")
        test2 = s1.read_once()
        self.stdout.write(str(s1))
        result = s1.read_once()
        if result is None:
            self.stdout.write("секрет уничтожен")
        else:
            self.stdout.write(result)

