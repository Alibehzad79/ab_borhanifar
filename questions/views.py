from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from questions.forms import QuestionForm
from questions.models import Question, QuestionTitle
from questions.models import QuestionPrice


# Create your views here.

def question_page(request):
    template_name = "question/question.html"
    user = request.user
    try:
        question_setting = QuestionPrice.objects.last()
        question_price = question_setting.price
    except:
        question_price = 0
    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            count = form.cleaned_data.get("count")
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("image")
            question_final_price = question_price * int(count)
            short_id = f"#ID-{timezone.now()}".replace(" ", "-")

            # redirect to bank getaway
            bank = True
            if bank:
                new_question = Question.objects.create(short_id=short_id, user=user, name=name, email=email,
                                                       question_count=count,
                                                       image=image, question_title=title, price=question_final_price,
                                                       date_sent=timezone.now())
                if new_question is not None:
                    new_question.save()
                    messages.add_message(request, message=f"با موفقیت ارسال شد.",
                                         level=messages.SUCCESS)
                    messages.add_message(request, message=f" آیدی سوال: {short_id}",
                                         level=messages.SUCCESS)
                    return redirect("question")
                else:
                    form.add_error('image', 'مقادیر وارد شده صحیح نمی باشد.')
            else:
                messages.add_message(request, message=f"ارسال ناموفق بود.",
                                     level=messages.ERROR)
                return redirect("question")
    else:
        form = QuestionForm()

    context = {
        "form": form,
        "question_price": question_price,
    }

    return render(request, template_name, context)
