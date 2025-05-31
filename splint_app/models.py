from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField # 導入 RichTextField
from ckeditor_uploader.fields import RichTextUploadingField # 如果需要圖片上傳功能


class UserProfile(models.Model):
    """擴展 User 模型以儲存額外信息，如是否完成前測"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pre_test_completed = models.BooleanField(default=False)
    pre_test_score = models.FloatField(null=True, blank=True) # 可以儲存前測分數

    def __str__(self):
        return self.user.username

# 在 User 模型創建時自動創建/更新 UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Unit(models.Model):
    """學習單元"""
    UNIT_CHOICES = [
        ('A', '單元 A：副木理論與用途介紹'),
        ('B', '單元 B：材料工具認識'),
        ('C', '單元 C：製作步驟示範'),
        ('D', '單元 D：臨床案例分析'),
    ]
    code = models.CharField(max_length=1, choices=UNIT_CHOICES, unique=True, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0) # 用於排序

    def __str__(self):
        return self.get_code_display()

    def get_absolute_url(self):
        return reverse('unit_detail', args=[str(self.code)])

class LearningResource(models.Model):
    """單元內的學習資源"""
    RESOURCE_TYPES = [
        ('video', '教學影片'),
        ('text_graphic', '圖文教材'),
    ]
    unit = models.ForeignKey(Unit, related_name='resources', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    title = models.CharField(max_length=200)
    # 對於影片，可以是 YouTube embed URL 或其他影片連結
    # 對於圖文，可以是文字內容或圖片路徑 (需要 Media 設定)
    content_url = models.URLField(blank=True, null=True, help_text="教學影片連結 (例如 YouTube)")
    content_text = models.TextField(blank=True, null=True, help_text="圖文教材內容 (HTML 可用)")
    # 如果是圖片，可以考慮 ImageField:
    # image_content = models.ImageField(upload_to='unit_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.unit.title} - {self.title} ({self.get_type_display()})"

class SimulationFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # 評估項目 (1-5 分)
    assessment = models.IntegerField(verbose_name="1. 評估與測量技能", null=True, blank=True)
    material = models.IntegerField(verbose_name="2. 材料準備與處理", null=True, blank=True)
    molding = models.IntegerField(verbose_name="3. 塑形與成型技巧", null=True, blank=True)
    positioning = models.IntegerField(verbose_name="4. 關節位置擺位", null=True, blank=True)
    trimming = models.IntegerField(verbose_name="5. 修剪與邊緣處理", null=True, blank=True)
    securing = models.IntegerField(verbose_name="6. 固定與調整", null=True, blank=True)
    
    # 反思筆記
    reflection_notes = models.TextField(verbose_name="反思與改進筆記", blank=True, null=True)
    
    submitted_at = models.DateTimeField(auto_now_add=True)

    # 移除舊的評分欄位 (如果不再需要)
    # rating_clarity = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="影片清晰度 (1-5)")
    # rating_usefulness = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="內容實用性 (1-5)")
    # rating_overall = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="整體滿意度 (1-5)")
    # comments = models.TextField(blank=True, null=True, verbose_name="其他建議或回饋")


    def __str__(self):
        return f"Feedback from {self.user.username} at {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

class LearningResource(models.Model):
    RESOURCE_TYPES = [
        ('video', '教學影片'),
        ('text_graphic', '圖文教材'),
    ]
    unit = models.ForeignKey(Unit, related_name='resources', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    title = models.CharField(max_length=200)
    content_url = models.URLField(blank=True, null=True, help_text="教學影片連結 (例如 YouTube)")
    
    # 使用 RichTextUploadingField 替代 TextField 以支持圖片上傳
    content_text = RichTextUploadingField(blank=True, null=True, help_text="圖文教材內容 (可包含圖片)") 
    # 或者，如果不需要上傳圖片，只想用富文本編輯器：
    # content_text = RichTextField(blank=True, null=True, help_text="圖文教材內容")

    def __str__(self):
        return f"{self.unit.title} - {self.title} ({self.get_type_display()})"