# _converters_to_bytes_map = {
#     bytes: lambda val: val,
#     bytearray: lambda val: val,
#     str: lambda val: val.encode('utf-8'),
#     int: lambda val: str(val).encode('utf-8'),
#     float: lambda val: str(val).encode('utf-8'),
#     }
#
#
# _converters_to_str_map = {
#     str: lambda val: val,
#     bytearray: lambda val: bytes(val).decode('utf-8'),
#     bytes: lambda val: val.decode('utf-8'),
#     int: lambda val: str(val),
#     float: lambda val: str(val),
#     }
#
#
# def _convert_to_bytes(value):
#     if type(value) in _converters_to_bytes_map:
#         converted_value = _converters_to_bytes_map[type(value)](value)
#     else:
#         raise TypeError("Argument {!r} expected to be of bytes,"
#                         " str, int or float type".format(value))
#     return converted_value
#
#
# def _convert_to_str(value):
#     if type(value) in _converters_to_str_map:
#         converted_value = _converters_to_str_map[type(value)](value)
#     else:
#         raise TypeError("Argument {!r} expected to be of bytes,"
#                         " str, int or float type".format(value))
#     return converted_value
