from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product

class Command(BaseCommand):

    def handle(self, *args, **options):

        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', ["Category_fixture.json", "Product_fixture.json"])
        self.stdout.write(self.style.SUCCESS("Фикстуры успешно загружены в базу данных"))