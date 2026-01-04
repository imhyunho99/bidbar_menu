import csv
from django.core.management.base import BaseCommand
from menu.models import Category, MenuItem
import os

class Command(BaseCommand):
    help = 'Imports menu items from a CSV file'

    def handle(self, *args, **options):
        # The CSV file is in the root directory of the project
        csv_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 'region.csv')

        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter='\t')
            
            for row in reader:
                parent_category_name = row['부모 카테고리']
                category_name = row['카테고리']
                item_name_en = row['영문명']
                item_name_ko = row['한글명']
                item_price = row['가격(1oz)']

                # Get or create parent category
                parent_category, created = Category.objects.get_or_create(
                    name=parent_category_name,
                    parent=None,
                    defaults={'name_en': ''} # Add default for name_en or handle it as needed
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created parent category: "{parent_category_name}"'))

                # Get or create child category
                child_category, created = Category.objects.get_or_create(
                    name=category_name,
                    parent=parent_category,
                    defaults={'name_en': ''} # Add default for name_en or handle it as needed
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created child category: "{category_name}" under "{parent_category_name}"'))

                # Create or update menu item
                menu_item, created = MenuItem.objects.update_or_create(
                    name=item_name_ko,
                    category=child_category,
                    defaults={
                        'name_en': item_name_en,
                        'price': item_price,
                        'description': '', # No description in CSV
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created menu item "{item_name_ko}"'))
                else:
                    self.stdout.write(self.style.WARNING(f'Updated menu item "{item_name_ko}"'))

        self.stdout.write(self.style.SUCCESS('Successfully imported all menu items.'))
