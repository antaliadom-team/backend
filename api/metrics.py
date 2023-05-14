from prometheus_client import Counter

orders_requests_total = Counter(
    name='orders_requests_total',
    documentation='Total number of orders.',
    labelnames=['endpoint', 'method', 'user'],
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
            metric = globals().get(metric_name)
            if metric is None:
                raise ValueError(f"Metric '{metric_name}' does not exist.")
            result = func(request, *args, **kwargs)
            if result:
                metric.labels(
                    endpoint=request.get_full_path(),
                    method=request.method,
                    user=request.user,
                ).inc()
            return result

        return wrapper

    return decorator
