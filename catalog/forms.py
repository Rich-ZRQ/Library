from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        date = self.cleaned_data['renewal_date']    # post过来的数据都是得先清洗为python格式然后放入cleaned_data字典里

        #Check date is not in past.
        if date < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return date