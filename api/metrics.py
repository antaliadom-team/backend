from prometheus_client import Counter, Enum

orders_requests_total = Counter(
    name='orders_requests_total',
    documentation='Total number of orders.',
    labelnames=['endpoint', 'method', 'user'],
)
orders_create_last_status = Enum(
    name='orders_create_last_status',
    documentation='Status of last order create endpoint call.',
    labelnames=['user'],
    states=['success', 'error'],
)


def save_metrics(func):
    """Сохранение метрик. Декоратор для функций APIView"""

    def wrapper(request, *args, **kwargs):
        orders_requests_total.labels(
            endpoint=request.get_full_path(),
            method=request.method,
            user=request.user,
        ).inc()
        result = func(request, *args, **kwargs)
        if result:
            orders_create_last_status.labels(user=request.user).state(
                'success'
            )
        else:
            orders_create_last_status.labels(user=request.user).state('error')
        return result

    return wrapper
