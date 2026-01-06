# load_data.py  (place this in the project root, next to manage.py)

import os
import csv

if __name__ == '__main__':
    # Set up Django environment FIRST
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wineapi.settings')
    import django
    django.setup()

    # NOW it's safe to import models
    from api.models import Wine

    print("Deleting old data...")
    Wine.objects.all().delete()

    files = ['data/winequality-red.csv', 'data/winequality-white.csv']
    types = ['red', 'white']

    total_loaded = 0
    for file_path, wine_type in zip(files, types):
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            print("Please make sure the CSV files are in the 'data/' folder.")
            continue

        print(f"Loading {wine_type} wines from {file_path}...")
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')  # IMPORTANT: delimiter is ';'
            wines_to_create = []
            for row in reader:
                wines_to_create.append(Wine(
                    type=wine_type,
                    fixed_acidity=float(row['fixed acidity']),
                    volatile_acidity=float(row['volatile acidity']),
                    citric_acid=float(row['citric acid']),
                    residual_sugar=float(row['residual sugar']),
                    chlorides=float(row['chlorides']),
                    free_sulfur_dioxide=float(row['free sulfur dioxide']),
                    total_sulfur_dioxide=float(row['total sulfur dioxide']),
                    density=float(row['density']),
                    pH=float(row['pH']),
                    sulphates=float(row['sulphates']),
                    alcohol=float(row['alcohol']),
                    quality=int(row['quality'])
                ))
            Wine.objects.bulk_create(wines_to_create)
            count = len(wines_to_create)
            total_loaded += count
            print(f"Successfully loaded {count} {wine_type} wines.")

    print(f"\nAll done! Total wines loaded: {total_loaded}")
    print("You can now run: python manage.py runserver")