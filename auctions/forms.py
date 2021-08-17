from django import forms

class CommentForm(forms.Form): 
    text = forms.CharField(max_length=200, 
        widget=forms.TextInput( 
            attrs={'class' : 'form-control', 'placeholder' : 'add a comment', 'name' : 'description'}))
      