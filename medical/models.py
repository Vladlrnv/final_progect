from django.utils import timezone

from django.db import models

from config import settings


# Доктора
class Doctors(models.Model):
    """
    Модель для хранения информации о врачах.

    Attributes:
        first_name (str): Имя врача.
        last_name (str): Фамилия врача.
        specialization (str): Специальность врача.
        experience (str): Стаж работы врача.
    """

    first_name = models.CharField(max_length=255, verbose_name="Имя", blank=True, null=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", null=True, blank=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    avatar = models.ImageField(upload_to="medical/", blank=True, null=True, verbose_name="Фотография")
    specialization = models.CharField(max_length=255, verbose_name="Специальность", null=True, blank=True)
    experience = models.CharField(max_length=255, verbose_name="Стаж работы", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь создавший этот экземпляр модели')

    class Meta:
        verbose_name = 'Доктор'
        verbose_name_plural = 'Доктора'

    def __str__(self):
        if self.patronymic:
            return f"{self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"


# Услуги
class Services(models.Model):
    """
    Модель для хранения информации о медицинских услугах.
    """

    name = models.CharField(max_length=500, verbose_name="Название услуги")
    description = models.CharField(max_length=500, verbose_name="Описание услуги")
    price = models.IntegerField(null=True, blank=True, verbose_name='Цена')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь создавший этот экземпляр модели')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return self.name


# Информация
class Information(models.Model):
    """
    Модель для хранения контактной информации клиники.

    Attributes:
        phone (str): Номер телефона клиники.
        address (str): Адрес клиники.
    """
    text_from_the_main_page = models.TextField(null=True, blank=True,
                                               verbose_name="Информация с главной страницы")
    image_the_main_page = models.ImageField(upload_to="medical/", blank=True, null=True,
                                            verbose_name="Фото с главной страницы")
    company_history = models.TextField(null=True, blank=True,
                                       verbose_name="История компании со страницы \"О компании\"")
    mission = models.CharField(max_length=100, null=True, blank=True, verbose_name="Миссия со страницы \"О компании\"")
    purposes = models.CharField(max_length=100, null=True, blank=True, verbose_name="Цели со страницы \"О компании\"")
    image_from_the_company = models.ImageField(upload_to="medical/", blank=True, null=True,
                                               verbose_name="Фото со страницы \"О компании\"")
    phone = models.CharField(max_length=11, verbose_name="Номер телефона")
    email = models.EmailField(unique=True, verbose_name="Email")
    address = models.CharField(max_length=255, verbose_name="Адрес центральной клиники", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь создавший этот экземпляр модели')

    # добавьте метод для получения или создания единственной записи
    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    class Meta:
        verbose_name = 'Информация'
        verbose_name_plural = 'Информации'


# Запись на приём
class Appointment(models.Model):
    """
    Модель для хранения записей пациентов на прием к врачам.

    Attributes:
        ADDRESS_CLINIC (list[tuple[str, str]]): Список адресов клиник, доступных для записи.
        address (str): Адрес клиники, выбирается из ADDRES_CLINIC.
        doctor (ForeignKey): Связь с моделью Doctors, указывающая на врача, к которому записан пациент.
        user (str): Имя пациента.
        appointment_date (datetime): Дата и время записи на прием.
        services (ForeignKey): Связь с моделью Services, указывающая на услуги, которые будут предоставлены.
    """
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'В ожидании'),
            ('completed', 'Услуга оказана'),
            # другие статусы
        ],
        default='pending', verbose_name="Статус"
    )

    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, verbose_name="Доктор", null=True, blank=True, )
    services = models.ForeignKey(Services, on_delete=models.CASCADE, verbose_name="Услуга", null=True, blank=True, )
    appointment_date = models.DateTimeField(verbose_name="Дата приёма")
    is_active = models.BooleanField(default=True, verbose_name="Статус записи")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пациент')

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        if self.doctor:
            return f"{self.doctor}, пациент: {self.user}, дата приёма: {self.appointment_date}"
        if self.services:
            return f"{self.services}, пациент: {self.user}, дата приёма: {self.appointment_date}"


# Результаты диагностики
class DiagnosticResults(models.Model):
    """
    Модель для хранения результатов диагностики, связанных с записями пациентов.

    Attributes:
        appointment (ForeignKey): Связь с моделью Record, указывающая на запись, к которой относятся результаты.
        results (str): Результаты диагностики, могут быть пустыми.
    """

    appointment = models.ForeignKey(Appointment, max_length=255, verbose_name="Запись",
                                    null=True, blank=True, on_delete=models.CASCADE)
    recommendations = models.TextField(blank=True, null=True, verbose_name="Рекомендации")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь создавший этот экземпляр модели')
    general_comments = models.TextField(blank=True, null=True, verbose_name="Общие комментарии")

    class Meta:
        verbose_name = 'Результат диагностики'
        verbose_name_plural = 'Результаты диагностики'

    def __str__(self):
        return f"{self.appointment}"


# Медицинские тесты. Результаты
class TestResult(models.Model):
    """  """
    diagnostic_result = models.ForeignKey(DiagnosticResults, related_name='tests', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название")
    value = models.CharField(max_length=255, null=True, blank=True, verbose_name="Значение")
    norm = models.CharField(max_length=255, null=True, blank=True, verbose_name="Норма")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")


# Обратная связь
class Feedback(models.Model):
    subject = models.CharField(max_length=100, verbose_name="Тема обращения")
    feedback = models.CharField(max_length=500, verbose_name="Сообщение")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь создавший этот экземпляр модели')
    created_at = models.DateTimeField(default=timezone.now, help_text="Дата и время создания")

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
