from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from PIL import Image
# Create your models here.
class Tags(TagBase):

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    # ... methods (if any) here


class Category(TagBase):

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # ... methods (if any) here

class SubCategory(TagBase):

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategory"

    # ... methods (if any) here

class TagsAll(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )


class CategorysAll(GenericTaggedItemBase):
    tag = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class SubCategorysAll(GenericTaggedItemBase):
    tag = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class Schemes(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    # openDate = models.DateTimeField(default=timezone.now,null = True)
    openDate = models.DateField(blank = True,null = True)
    closeDate = models.DateField(blank = True,null = True)
    nodalMinistry = models.CharField(max_length=100,blank=True,null = True)
    nodalDepartment = models.CharField(max_length=100,blank=True,null = True)
    brief = models.TextField()
    details = models.TextField()
    eligibility = models.TextField()
    tags = TaggableManager(through=TagsAll,verbose_name="Tags",blank = True)
    category = TaggableManager(through=CategorysAll,verbose_name="Category",blank = True)
    subcategory = TaggableManager(through=SubCategorysAll,verbose_name="Subcategory",blank = True)
    references = models.TextField()
    uploadDate = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=False, unique=True)
    image = models.ImageField(default='default.jpg',upload_to='schemes')
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("schemedetail", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        super(Schemes, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)