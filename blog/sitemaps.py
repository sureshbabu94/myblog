from django.contrib.sitemaps import Sitemap
from .models import Dummy

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Dummy.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_on