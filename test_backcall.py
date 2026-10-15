import pytest

from backcall import callback_prototype


@callback_prototype
def on_data(data, status):
    """Prototype: the API always passes (data, status)."""


def test_callback_with_full_signature_is_returned_unchanged():
    def cb(data, status):
        return data, status

    assert on_data.adapt(cb) is cb


def test_callback_with_fewer_args_receives_only_what_it_accepts():
    @on_data.adapt
    def only_data(data):
        return data

    assert only_data(1, 200) == 1


def test_lambda_with_one_arg_is_adapted():
    cb = on_data.adapt(lambda data: ("lambda", data))
    assert cb(7, 500) == ("lambda", 7)


def test_optional_parameter_gets_default_unless_prototype_supplies_it():
    @on_data.adapt
    def with_default(data, status, verbose=False):
        return data, status, verbose

    assert with_default(1, 200) == (1, 200, False)


def test_extra_required_parameter_is_rejected():
    def needs_three(data, status, extra):
        return None

    with pytest.raises(TypeError, match="unmatched arguments"):
        on_data.adapt(needs_three)


def test_var_args_in_prototype_are_rejected():
    with pytest.raises(TypeError, match=r"\*args/\*\*kwargs not supported"):

        @callback_prototype
        def bad(*args):
            pass


def test_adapt_attribute_is_attached_to_prototype():
    assert callable(on_data.adapt)
