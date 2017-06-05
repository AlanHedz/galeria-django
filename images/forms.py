from models import Images
from models import Comments
from django import forms

class CreateImage(forms.Form):
    title = forms.CharField(max_length=100)
    imageFile = forms.CharField(max_length=200, widget=forms.ClearableFileInput)

    def __init__(self, *args, **kwargs):
        super(CreateImage, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['imageFile'].widget.attrs.update({'id': 'inputFile'})

class CreateComment(forms.Form):
    

class CreateCommentForm(forms.ModelForm):
    text = forms.CharField(max_length=200, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update(
            {'class': 'form-control textarea-form',
             'placeholder': 'Escribe tu comentario...'})

    class Meta:
        model = Comments
        exclude = ('user', 'image')
