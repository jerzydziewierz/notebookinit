
class Obsolete(Exception):
    """notifies the user that something is obsolete

    usage: raise Obsolete("new_function")

    """
    def __init__(self, use_instead=None):
        import inspect
        caller = inspect.stack()[1]
        caller_fn_name = caller.function
        caller_file = caller.filename
        # print(caller)
        if use_instead is not None:
            message = f"function >>{caller_fn_name}<< from {caller_file} is obsolete. Use {use_instead} instead."
        else:
            message = f">{caller_fn_name}< from {caller_file} is obsolete."
        super().__init__(message)

    pass
