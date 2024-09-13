# from datetime import datetime
#
# current_datetime = ((str(datetime.now()).replace('-', '.'))[0:-10].split())
# current_datetime[0] = str(int(current_datetime[0].split('.')[2]) + 1) + '.' + current_datetime[0].split('.')[1] + '.' + \
#                       current_datetime[0].split('.')[0]
#
# print(current_datetime)
# print(current_datetime)
#
# t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
# r = 3
# os = len(t)%r
# for i in range(0, len(t)- os, r):
#     text = []
#     for _ in range(r):
#         text.append(t[i + _])
#     print(text)
#
# print(t[-os:])
par = 'Ценс'
case_dict = {
    'ФИ': 'fi',
    'Телефон': 'phone',
    'Дата': 'date',
    'Время': 'time',
    'Процедура': 'procedure'
}

par = case_dict.get(par, 'price')
print(par)