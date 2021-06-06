from django import forms

class WriteSolution(forms.Form):
    ltr_dir = forms.BooleanField( 
                                widget=forms.CheckboxInput(
                                    attrs = {'style':'position:inherit;margin-left:4px;',
                                    'onclick':"change_dir('MathInput')"
                                    }
                                ),
                                label='الكتابة من اليسار',
                                required = False,
                                )
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
    ltr_dir = forms.BooleanField( 
                                widget=forms.CheckboxInput(
                                    attrs = {'style':'position:inherit;margin-left:4px;',
                                    'onclick':"change_dir()",
                                    }
                                ),
                                label='الكتابة من اليسار',
                                required = False,
                                )
    content = forms.CharField(widget=forms.Textarea(
                        attrs={'id':'MathInput',}),
                        label='',
    )