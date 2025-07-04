
from django import forms
from .models import Expense, Category

class ExpenseCreateModelForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'] = forms.ChoiceField(
			choices = [
				(cat.id, cat.name) for cat in Category.objects.all()
    	])
        self.fields['date'] = forms.DateField(
			# widget=forms.DateInput(attrs={'type': 'date'})
			widget=forms.SelectDateWidget(years=range(1950, 2100))
		)
        for field in self.fields.values():
            if field.__class__.__name__ != 'DateField':
                field.widget.attrs.update({
					'class': 'form-control form-control-sm'
				})
		
    class Meta:
        model = Expense
        fields = '__all__'

# class ExpenseCreateForm(forms.Form):
#     amount = forms.FloatField(blank=False)
#     date = forms.DateField(label="Expense date", input_formats=["%d/%m/%Y"], required=True, default=now)
#     description = forms.CharField(name="Descrição", required=False, max_length=600)
#     owner = forms.ChoiceField(choices=User.objects.all.username)
#     category = forms.ModelChoiceField(blank=False)
    