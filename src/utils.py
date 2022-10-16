def second_hand_smoke_count(value):
    if value == '1-2 раза в неделю':
        return 1.5
    if value == '2-3 раза в день':
        return 17.5
    if value == '3-6 раз в неделю':
        return 4.5
    if value == '4 и более раз в день':
        return 28.0
    if value == 'не менее 1 раза в день':
        return 7.0
    return 0.0

def round_time(hour, min):
    if min <= 15:
        return hour, 0
    if 15 < min < 45:
        return hour, 30
    return hour + 1, 0

def sleep_time(value):
    hour, min, sec = map(int, value.split(':'))
    hour, min = round_time(hour, min)

    if hour >= 23:
        return (hour - 23) + min / 60
    if hour < 12:
        return hour + 1 + min / 60
    return (hour + min / 60) - 23

def wakeup_time(value):
    hour, min, sec = map(int, value.split(':'))
    hour, min = round_time(hour, min)

    if hour >= 7:
        return (hour - 7) + min / 60
    return (hour + min / 60) - 7
