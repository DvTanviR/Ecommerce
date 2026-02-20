from django.db import migrations, models
from django.utils.text import slugify

def generate_unique_slug(apps, title, product_id=None):
    Product = apps.get_model('main', 'Product')
    slug = slugify(title)
    unique_slug = slug
    counter = 1
    while Product.objects.filter(slug=unique_slug).exclude(id=product_id).exists():
        unique_slug = f"{slug}-{counter}"
        counter += 1
    return unique_slug

def populate_slugs(apps, schema_editor):
    Product = apps.get_model('main', 'Product')
    for product in Product.objects.all():
        if not product.slug:
            product.slug = generate_unique_slug(apps, product.taitle, product.id)
            product.save()

def reverse_populate_slugs(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_populate_product_slugs'),
    ]

    operations = [
        # First populate the slugs
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
        
        # Then make the field unique and non-nullable
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=200, unique=True),
        ),
    ]