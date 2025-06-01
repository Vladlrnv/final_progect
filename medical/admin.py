from .models import Doctors, Services, Information, CompanyValues, Appointment, \
    DiagnosticResults, TestResult, Feedback

from django.contrib import admin
from .models import AddressHospital
from .utils import get_coordinates


# Доктора
@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "patronymic",
                    "avatar", "specialization", "experience", "user", )
    list_filter = ("last_name", "specialization", "reviews",)
    search_fields = ("experience", "id",)


# Услуги
@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "price", "user",)
    list_filter = ("name", "description",)
    search_fields = ("name", "description",)


# Информация
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ("id", "text_from_the_main_page", "image_the_main_page", "company_history",
                    "mission", "purposes", "image_from_the_company", "phone", "email", "address", "user",)
    list_filter = ("address",)
    search_fields = ("address",)


# Запись на приём
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "address", "doctor", "appointment_date", "services", "is_active", "user",)
    list_filter = ("appointment_date", "user", "services")
    search_fields = ("appointment_date", "user", "services")


# Результаты диагностики
@admin.register(DiagnosticResults)
class DiagnosticResultsAdmin(admin.ModelAdmin):
    list_display = ("id", "appointment", "recommendations", "user", "general_comments",)
    list_filter = ("appointment",)
    search_fields = ("appointment",)


# Медицинские тесты. Результаты
@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("id", "diagnostic_result", "name", "value", "norm", "comment",)
    list_filter = ("name",)
    search_fields = ("name",)


# Обратная связь
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("subject", "feedback", "user", "created_at",)
