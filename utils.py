def gen_message(dict, to_copy = [], **kwargs):
    d = dict.copy()

    for key, value in kwargs.items():
        d[key] = value

    for key in to_copy:
        d[key] = f"`{d[key]}`"

    return f"ФИ: {d['fi']}\nТелефон: {d['phone']}\nВремя: {d['time']}\nПроцедура: {d['procedure']}\nЦена: {d['price']}\nДата: {d['date']}"
