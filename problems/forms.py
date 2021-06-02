from django import forms

class WriteSolution(forms.Form):
    content = forms.CharField(widget=forms.Textarea(
                            attrs={'id':'MathInput',

                                  }
                                                    ),
                            label='',
                            )
    file    = forms.FileField(label='', required = False)

    def __init__(self, *args, dir_attrs = {}, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs |= dir_attrs


class WriteComment(forms.Form):
	content = forms.CharField(widget=forms.Textarea(
						attrs={'id':'MathInput',}),
						label='',
						)
