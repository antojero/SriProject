from django.db import models

class Media(models.Model):
    IMAGE, VIDEO, REEL = "image", "video", "reel"
    TYPE_CHOICES = [
        (IMAGE, "Image"), 
        (VIDEO, "Video"), 
        (REEL, "Instagram Reel")
    ]

    CATEGORY_CHOICES = [
        ("Cakes", "Cakes"),
        ("Celebrations", "Celebrations"),
        ("Videos", "Videos"),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=IMAGE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="Cakes")
    file = models.FileField(upload_to="gallery/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="gallery/thumbnails/", blank=True, null=True)
    instagram_url = models.URLField(blank=True)
    title = models.CharField(max_length=160, blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Media items"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title or f"Media #{self.id}"
