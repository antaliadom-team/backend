from django.conf import settings
from django.core.management import BaseCommand

from catalog.models import Image


class Command(BaseCommand):
    help = 'Regenerate previews for all real estate pictures.'

    def handle(self, *args, **kwargs):
        """Regenerate previews for all real estate pictures."""

        all_images = Image.objects.all()
        self.stdout.write('Deleting existing previews...')
        for image in all_images:
            try:
                image.delete_thumbnails()
            except FileNotFoundError:
                all_images.pop(image)
                continue
        self.stdout.write('Generating new previews...')
        for image in all_images:
            for size in settings.PREVIEW_SIZES:
                try:
                    Image.thumbnail_generator(
                        infile=image.image.path,
                        outfile=image.filename_generator(
                            image.image.path, size
                        ),
                        image_size=size,
                    )
                except FileNotFoundError:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Photo of the object #id:{image.real_estate.id} '
                            'found in the DB but file '
                            f'...{image.image.path[-30:]} not found... '
                            'skipping'
                        )
                    )
                except Exception as error:
                    self.stdout.write(self.style.ERROR(error))
        self.stdout.write(
            self.style.SUCCESS('Previews regenerated successfully.')
        )
