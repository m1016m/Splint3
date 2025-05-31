# splint_app/forms.py
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from .models import SimulationFeedback # <--- 加入這一行，導入 SimulationFeedback 模型

class CustomUserCreationForm(UserCreationForm):
    # 我們在這裡定義的欄位會覆蓋 User model 的預設表單欄位，
    # 或者添加 UserCreationForm 預設沒有的欄位
    email = forms.EmailField(
        required=True,
        help_text='必填。有效的電子郵件地址。'
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='選填。'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        help_text='選填。'
    )

    class Meta:
        model = User
        # 明確列出你希望在表單中出現的 User model 字段
        # UserCreationForm 會自動處理 password 和 password confirmation
        fields = ("username", "email", "first_name", "last_name")
        # 為了保持 UserCreationForm 對 username 字段的特殊處理（如果有的話）
        field_classes = {'username': UsernameField}

class PreTestForm(forms.Form):
    # 這裡簡化前測，只做一個簡單的提交確認
    # 實際的前測題目可以硬編碼在模板中，或從資料庫讀取
    # 例如：
    # q1 = forms.ChoiceField(label="問題1：副木的主要用途是？", choices=[('A','A'), ('B','B')], widget=forms.RadioSelect)
    # q2 = forms.CharField(label="問題2：請列舉兩種常用的副木材料。")
    confirmation = forms.BooleanField(label="我已了解前測的目的並準備開始學習。", required=True)

class FeedbackForm(forms.ModelForm):
    # 評估項目 (對應 HTML 中的 name 屬性)
    assessment = forms.IntegerField(
        label="1. 評估與測量技能",
        min_value=1, max_value=5,
        widget=forms.HiddenInput() # 前端用 radio buttons，這裡隱藏
    )
    material = forms.IntegerField(
        label="2. 材料準備與處理",
        min_value=1, max_value=5,
        widget=forms.HiddenInput()
    )
    molding = forms.IntegerField(
        label="3. 塑形與成型技巧",
        min_value=1, max_value=5,
        widget=forms.HiddenInput()
    )
    positioning = forms.IntegerField(
        label="4. 關節位置擺位",
        min_value=1, max_value=5,
        widget=forms.HiddenInput()
    )
    trimming = forms.IntegerField(
        label="5. 修剪與邊緣處理",
        min_value=1, max_value=5,
        widget=forms.HiddenInput()
    )
    securing = forms.IntegerField(
        label="6. 固定與調整",
        min_value=1, max_value=5,
        widget=forms.HiddenInput()
    )
    
    # 反思筆記 (對應 HTML 中的 textarea id="reflection")
    # 注意：我們將把這個欄位加到 SimulationFeedback 模型中
    reflection_notes = forms.CharField(
        label="反思與改進筆記",
        widget=forms.Textarea(attrs={'rows': 4, 'style': 'display:none;'}), # 也可隱藏
        required=False # 設為選填
    )

    class Meta:
        model = SimulationFeedback
        # 更新 fields 以包含新欄位 (這些欄位需要在 SimulationFeedback 模型中定義)
        fields = ['assessment', 'material', 'molding', 'positioning', 'trimming', 'securing', 'reflection_notes']
        # 我們不再使用之前 ModelForm 中的 rating_clarity, rating_usefulness, rating_overall
        # 如果想保留，可以加回來，或者從模型和表單中移除它們

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 可以移除 crispy forms 的標籤，因為我們是手動渲染
        # self.helper = FormHelper()
        # self.helper.form_tag = False # 如果不想 crispy forms 渲染 <form> 標籤