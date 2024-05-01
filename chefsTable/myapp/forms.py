from .models import Booking
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['comments'].required = False

        self.fields['guest_count'].help_text = '1～10人までの予約ができます'

        self.fields['comments'].label = 'コメント'
