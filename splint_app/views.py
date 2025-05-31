from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, PreTestForm, FeedbackForm
from .models import Unit, LearningResource, UserProfile, SimulationFeedback
from .forms import FeedbackForm # 確保 FeedbackForm 被正確導入
from django.contrib import messages # 用於顯示訊息 (可選)

def home_view(request):
    if request.user.is_authenticated:
        # 如果已登入，且需要根據特定邏輯導向，可以在這裡處理
        # 例如：檢查是否完成前測
        try:
            user_profile = request.user.userprofile
            if not user_profile.pre_test_completed:
                return redirect('pre_test')
            return redirect('course_landing') # 或其他登入後頁面
        except UserProfile.DoesNotExist:
            # 處理 UserProfile 不存在的情況，理論上 signal 會創建
            UserProfile.objects.create(user=request.user)
            return redirect('pre_test') # 導向到前測
    return render(request, 'splint_app/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 確保 UserProfile 被創建 (signal 應該會處理，但以防萬一)
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('pre_test') # 註冊成功後導向前測
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def course_landing_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if not user_profile.pre_test_completed:
        return redirect('pre_test')

    units = Unit.objects.all().order_by('order') # <--- 這一行獲取單元
    context = {
        'units': units, # <--- 傳遞給模板
        'page_title': '課程模組選擇'
    }
    return render(request, 'splint_app/course_landing.html', context)

@login_required
def pre_test_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.pre_test_completed:
        return redirect('course_landing') # 如果已完成，直接去課程列表

    if request.method == 'POST':
        form = PreTestForm(request.POST)
        if form.is_valid():
            # 這裡可以加入實際的測驗邏輯和評分
            # 簡化：假設提交即完成
            user_profile.pre_test_completed = True
            # user_profile.pre_test_score = calculate_score(form.cleaned_data) # 計算分數
            user_profile.save()
            return redirect('course_landing')
    else:
        form = PreTestForm()

    context = {
        'form': form,
        'page_title': '前測：副木製作基礎理解評估'
    }
    return render(request, 'splint_app/pre_test.html', context)

# splint_app/views.py
@login_required
def unit_detail_view(request, unit_code):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.pre_test_completed:
        return redirect('pre_test')

    unit = get_object_or_404(Unit, code=unit_code)
    # video_resources = unit.resources.filter(type='video') # 不再需要分開獲取
    # text_graphic_resources = unit.resources.filter(type='text_graphic') # 可以在模板中判斷

    all_units = Unit.objects.all().order_by('order') # 用於左側導航

    context = {
        'unit': unit,
        'all_units': all_units, # 傳遞所有單元給模板
        'page_title': unit.title
    }
    return render(request, 'splint_app/unit_detail.html', context)

@login_required
def simulation_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.pre_test_completed:
        return redirect('pre_test')

    # 原始短連結
    # simulation_video_url_short = "https://youtu.be/xPmq8F2sKJI" 
    
    # 正確的嵌入式 URL
    simulation_video_embed_url = "https://www.youtube.com/embed/xPmq8F2sKJI" 

    existing_feedback = SimulationFeedback.objects.filter(user=request.user).exists()

    context = {
        'simulation_video_url': simulation_video_embed_url, # <--- 使用嵌入式 URL
        'existing_feedback': existing_feedback,
        'page_title': '模擬操作實作任務'
    }
    return render(request, 'splint_app/simulation.html', context)

@login_required
def simulation_feedback_view(request):
    # ... (檢查 user_profile 和 pre_test_completed 的邏輯保持不變) ...
    user_profile = UserProfile.objects.get(user=request.user)
    if not user_profile.pre_test_completed:
        return redirect('pre_test')

    # 檢查是否已提交過回饋
    if SimulationFeedback.objects.filter(user=request.user).exists():
        messages.info(request, "您已經提交過此模擬操作的回饋。")
        return redirect('simulation') # 或導向課程列表

    if request.method == 'POST':
        form = FeedbackForm(request.POST) # 使用更新後的 FeedbackForm
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            
            # 從 cleaned_data 中獲取所有評估項目的值並賦給 feedback 物件
            # 由於我們在 FeedbackForm 中定義了這些字段，它們會出現在 cleaned_data 中
            feedback.assessment = form.cleaned_data.get('assessment')
            feedback.material = form.cleaned_data.get('material')
            feedback.molding = form.cleaned_data.get('molding')
            feedback.positioning = form.cleaned_data.get('positioning')
            feedback.trimming = form.cleaned_data.get('trimming')
            feedback.securing = form.cleaned_data.get('securing')
            feedback.reflection_notes = form.cleaned_data.get('reflection_notes')
            
            feedback.save()
            messages.success(request, "感謝您的回饋，評估結果已儲存！")
            return redirect('course_landing') # 儲存後導向課程列表頁面
        else:
            # 如果表單無效，可以打印錯誤到控制台進行調試
            print("Feedback form errors:", form.errors)
            messages.error(request, "提交回饋時發生錯誤，請檢查您的輸入。")
            # 這裡可以選擇是重定向回模擬頁面，還是嘗試重新渲染帶有錯誤的表單
            # 但由於表單是JS驅動的，直接重定向可能更簡單
            return redirect('simulation') # 或 'simulation_feedback' GET 請求
    else:
        # GET 請求時，我們需要傳遞一個空的 FeedbackForm 實例給模板
        # 雖然它的主要輸入是隱藏的，但 {{ form.as_p }} 或手動渲染 csrf_token 需要它
        form = FeedbackForm() 

    context = {
        'form': form, # 傳遞 form 給模板，即使它主要用於 CSRF 和隱藏欄位
        'page_title': '模擬操作回饋與自我評估'
    }
    return render(request, 'splint_app/feedback_form.html', context)