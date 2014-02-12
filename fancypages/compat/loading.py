from importlib import import_module


try:
    from django.utils.module_loading import import_string
except ImportError:
    try:
        from django.utils.module_loading import import_by_path as import_string
    except ImportError:

        def fallback_import_string(dotted_path):
            """
            Import a dotted module path and return the attribute/class
            designated by the last name in the path. Raise ImportError if the
            import failed.
            """
            try:
                module_path, class_name = dotted_path.rsplit('.', 1)
            except ValueError:
                msg = "%s doesn't look like a module path" % dotted_path
                raise ImportError(msg)

            module = import_module(module_path)

            try:
                return getattr(module, class_name)
            except AttributeError:
                msg = 'Module "%s" does not define a "%s" attribute/class' % (
                    dotted_path, class_name)
                raise ImportError(msg)

        import_string = fallback_import_string  # noqa
