from django import template
from django.utils.formats import date_format

register = template.Library()


@register.filter
def uk_date(date, format_string='j F Y'):
    """
    Форматує дату з українськими назвами місяців
    """
    if not date:
        return ''

    # Словник з українськими назвами місяців
    uk_months = {
        'January': 'січня',
        'February': 'лютого',
        'March': 'березня',
        'April': 'квітня',
        'May': 'травня',
        'June': 'червня',
        'July': 'липня',
        'August': 'серпня',
        'September': 'вересня',
        'October': 'жовтня',
        'November': 'листопада',
        'December': 'грудня',
    }

    # Отримуємо англійський формат дати
    formatted_date = date_format(date, format_string)

    # Замінюємо англійські назви місяців на українські
    for eng, ukr in uk_months.items():
        formatted_date = formatted_date.replace(eng, ukr)

    return formatted_date