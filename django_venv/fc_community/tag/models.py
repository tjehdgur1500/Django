from django.db import models

# Create your models here.


class Tag(models.Model):
    tagname = models.CharField(max_length=32, verbose_name="태그명")
    registered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name='등록시간')

    def __str__(self):
        return self.tagname

    class Meta:
        db_table = 'Fastcampus_tag'
        verbose_name = "패스트캠퍼스 태그"
        verbose_name_plural = '패스트캠퍼스 태그'
