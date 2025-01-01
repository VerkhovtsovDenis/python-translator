from django import forms


class TextForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': "form-control",
            'rows': 10,
            "placeholder": "Введите ваш код на Pascal..."}),
        label='',
        initial='''pascal aaa;
var a: read;
begin
a := 2;
end.''',
        max_length=5000)
