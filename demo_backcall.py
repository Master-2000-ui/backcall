from backcall import callback_prototype


@callback_prototype
def on_data(data, status):
    """Prototype: the API always passes (data, status)."""


@on_data.adapt
def only_data(data):
    return f"got data={data!r}"


@on_data.adapt
def with_default(data, status, verbose=False):
    return f"data={data!r} status={status!r} verbose={verbose}"


print(on_data.adapt(lambda data: f"lambda: {data}")(1, 200))
print(only_data(1, 200))
print(with_default(1, 200))
print(with_default(1, 200, verbose=True))
