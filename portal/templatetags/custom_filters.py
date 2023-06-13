from django import template

register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
# @register.filter(name='currency_rub')  # название можем менять самостоятельно
@register.filter()
def censor(value):  # Будем указывать значение в фильтре, по-умолчанию Рубли
    """
    value: текст, к которому нужно применить фильтр
    """
    text_new = str(value)
    bad_words = ['подписчик', 'инвестицией', 'дополненной']
    lst = value.split()
    for word in lst:
        if word in bad_words:
            censor_word = word[0] + (len(word) - 1) * '*'
            text_new = text_new.replace(word, censor_word)
    return text_new
