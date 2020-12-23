from django import forms

class WriteSolution(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
                            attrs={'id':'MathInput',
                                  }
                                                    ),
                            label='',
                            )
    file    = forms.FileField(label='', required = False)

class WriteComment(forms.Form):
	content = forms.CharField(widget=forms.Textarea(
						attrs={'id':'MathInput',}),
						label='',
						)
