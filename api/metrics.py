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
registered_users_counter = Counter(
    'registered_users_total', 'Total number of registered users'
)
activated_users_counter = Counter(
    'activated_users_total', 'Total number of activated users'
)
real_estate_counter = Counter(
    'real_estate_total', 'Total number of real estate'
)


def save_metrics(metric_name):
    """Сохранение метрик. Декоратор для функций APIView"""

    def decorator(func):
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
                orders_create_last_status.labels(user=request.user).state(
                    'error'
                )
            return result

        return wrapper

    return decorator
