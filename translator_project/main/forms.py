from django import forms


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control prettyprint",
            'rows': 15,
            "placeholder": "Введите ваш код на Pascal..."}),
        label='',


        max_length=5000)


