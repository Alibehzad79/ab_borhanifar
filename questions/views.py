from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from questions.forms import QuestionForm
from questions.models import Question
from questions.models import QuestionPrice


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
            user = request.user
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            count = form.cleaned_data.get("count")
            title = form.cleaned_data.get("title")
            image = form.cleaned_data.get("image")
            question_final_price = question_price * int(count)
            short_id = f"#ID-{timezone.now()}".replace(" ", "-")
            new_question = Question.objects.create(short_id=short_id, user=user, name=name, email=email,
                                                   question_count=count,
                                                   image=image, question_title=title, price=question_final_price,
                                                   date_sent=timezone.now())
            if new_question is not None:
                new_question.save()
                messages.add_message(request, message="با موفقیت در سبد سوال قرار گرفت", level=messages.SUCCESS)
                return redirect("user_questions")
    else:
        form = QuestionForm()

    context = {
        "form": form,
        "question_price": question_price,
    }

    return render(request, template_name, context)
