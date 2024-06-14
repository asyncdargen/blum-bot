def format_time(millis: int) -> str:
    result = []

    if millis // 3_600_000 > 0:
        result.append(f'{int(millis // 3_600_000)} час.')
        millis %= 3_600_000

    if millis // 60_000 > 0:
        result.append(f'{int(millis // 60_000)} мин.')
        millis %= 60_000

    if len(result) == 0 or millis // 1000 > 0:
        result.append(f'{int(millis // 1000)} сек.')

    return ' '.join(result)
