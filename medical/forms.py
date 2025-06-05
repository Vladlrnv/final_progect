from django import forms

from medical.models import Appointment, Feedback

SPAMS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар', ]


# Запись на приём
class AppointmentForm(forms.ModelForm):
    """ Форма для записи на приём """

    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "services"]
        exclude = ["user",]
        widgets = {
            "appointment_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Дата и время приёма",
                    "type": "datetime-local"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields["services"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Услуга:"}
        )
        self.fields["doctor"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Доктор:"}
        )
        self.fields["appointment_date"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Дата приёма:"}
        )


# Обратная связь
class FeedbackForm(forms.ModelForm):
    """ Форма для обратной связи """

    class Meta:
        model = Feedback
        fields = ["subject", "feedback",]
        exclude = ["user", "created_at",]

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Возникла проблема?"}
        )
        self.fields["feedback"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Расскажите о проблеме с которой вы столкнулись."}
        )
