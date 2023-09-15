from random import choice

from django.core.management.base import BaseCommand
from faker import Faker

from apps.models import Category, Product

fake = Faker()


class Command(BaseCommand):
    help = 'Create fake products and categories'

    def add_arguments(self, parser):
        # python manage..py -p 1.. -c 1..
        parser.add_argument('-p', '--products', type=int, help='Number of products to be created')
        parser.add_argument('-c', '--categories', type=int, help='Number of categories to be created')

    def handle(self, *args, **kwargs):
        num_products = kwargs['products']
        num_categories = kwargs['categories']

        categories = []
        for i in range(num_categories):
            category = Category.objects.create(
                name=fake.name())
            categories.append(category)
            self.stdout.write(self.style.SUCCESS(f'Successfully created Category | "{category.name}"'))

        for i in range(num_products):
            category = choice(categories)
            product = Product.objects.create(
                name=fake.name(),
                description=fake.text(),
                price=fake.pydecimal(left_digits=4, right_digits=2, positive=True),
                category=category,
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created Product | "{product.name}"'))
