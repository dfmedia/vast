
def make_type_validator(_type):
    """
    Make a validator function to check type 
    
    :param _type: such as int / bool 
    :return: validator function for that type
    """
    msg_format = "'{name}' must be {type!r} (got {value!r} that is a {actual!r})."

    def validate(value, attr_name, msg=None):
        if not isinstance(value, _type):
            msg = msg or msg_format.format(
                name=attr_name, type=_type,
                actual=value.__class__, value=value
            )
            raise TypeError(msg, attr_name, _type, value)

    return validate


def make_greater_than_validator(must_be_greater_than_me):
    """
    Makes greater_than validator function
     
    :param must_be_greater_than_me: value that must be (strictly) smaller 
    :return: validator function for greater than
    """
    msg_format = "'{name}' must be greater than {gt!r} but got {value!r}."

    def validate(value, attr_name, msg=None):
        if must_be_greater_than_me >= value:
            msg = msg or msg_format.format(
                name=attr_name, gt=must_be_greater_than_me, value=value,
            )
            raise ValueError(msg, attr_name, value)

    return validate


def make_in_validator(_collection):
    """
    
    :param _collection: a collection that implements __in__  
    :return: validator function for in_ 
    """

    collection = set(_collection)

    msg_format = "'{name}' with value {value!r} not found in collection {col!r}."

    def validate(value, attr_name, msg=None):
        if value not in collection:
            msg = msg or msg_format.format(
                name=attr_name, value=value, col=_collection,
            )
            raise ValueError(msg, attr_name, value)

    return validate


def make_min_max_validator():
    """
    
    :return: validator that check that min is <= max 
    """
    msg_format = "'{min_val}' >  '{max_val}' for attribute {name!r}."

    def validate(value, attr_name, msg=None):
        min_val, max_val = value
        if min_val > max_val:
            msg = msg or msg_format.format(
                min_val=min_val, max_val=max_val, name=attr_name,
            )
            raise ValueError(msg, attr_name, value)

    return validate


def make_compound_validator(*validators):
    """
    Makes a validator function from other validator functions
    :param validators: iterable of validator functions 
    :return: validator function that applies all validators 
    """
    def validate(value, attr_name, msg=None):
        for validator_fn in validators:
            validator_fn(value, attr_name, msg=msg)

    return validate


# TODO write validators so they return the errors
def make_class_validator(clazz):
    """

    :param clazz:
    :return:
    """
    msg = "'{name}' must be of {type!r} but got {actual!r} instead."

    def validate(instance, attr_name):
        attr = getattr(instance, attr_name)
        if isinstance(attr, clazz):
            return None
        return msg.format(name=attr_name, type=clazz, actual=type(attr))

    return validate


def make_enum_validator(enum):
    """

    :param enum: enum class
    :return:
    """
    allowed_values = set([e.value for e in enum])
    msg = "Value {attr_value} is not in allowed_values set : ({allowed_values})"

    def validate(instance, attr_name):
        attr_value = getattr(instance, attr_name)
        if attr_value in allowed_values:
            return None
        return msg.format(attr_value=attr_value, allowed_values=allowed_values)

    return validate

