from django import forms
from questions.models import QuestionPrice, QuestionTitle


class QuestionForm(forms.Form):

    def __init__(self, *args, **kwargs):
        try:
            question_setting = QuestionPrice.objects.last()
            question_titles = QuestionTitle.objects.all()
            q_count = question_setting.q_count
        except:
            q_count = 1
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['count'] = forms.ChoiceField(
            choices=[(f"{item + 1}", f"{item + 1}") for item in range(q_count)],
            widget=forms.Select(attrs={"class": "form-select"})
        )
        self.fields['title'] = forms.ChoiceField(
            choices=[(f"{item.name}", f"{item.name}") for item in question_titles],
            widget=forms.Select(attrs={"class": "form-select"})
        )

    name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام و نام خانوادگی را وارد کنید"}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "example@mail.com"}))

    count = forms.ChoiceField()
    title = forms.ChoiceField()
    image = forms.ImageField(widget=forms.FileInput(attrs={"class": "form-control"}), allow_empty_file=False)
