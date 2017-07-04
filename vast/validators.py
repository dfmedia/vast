"""
Validators for class instance

A validator function always takes in an instance and returns:
 None if there are no errors
 An str error message if one found
"""

from vast.errors import IllegalModelStateError


def validate(instance, validators=None):
    """
    :param instance: to be validated
    :param validators: iterable of validator functions
    :return: None if no errors, raises a validation errors if there are
    """
    validators = validators or getattr(instance, "VALIDATORS", [])

    errors = (v(instance) for v in validators)
    errors = ",".join((e for e in errors if e))
    if errors:
        msg = "validation error(s) found for instance from {cls_name}. Errors = [{errors}]"
        cls_name = instance.__class__.__name__
        raise IllegalModelStateError(msg.format(cls_name=cls_name, errors=errors))



def make_greater_then_validator(attr_name, value, allow_none=True):
    """
    :param attr_name: attribute name
    :param value: to be greater than
    :param allow_none: no error if attribute value is None
    :return: msg if found an error None otherwise
    """
    msg = "attribute {attr_name} value was {attr_value} but must be greater than {value}"

    def _validate(instance):
        attr_value = getattr(instance, attr_name, None)

        if attr_value is None:
            error = not allow_none
        else:
            error = attr_value < value

        if error:
            return msg.format(attr_name=attr_name, attr_value=attr_value, value=value)

    return _validate
