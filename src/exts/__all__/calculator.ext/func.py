#!/usr/bin/python3.8

def get_average(*args):
    return sum(args) / len(args)

def get_sum(*args):
    return sum(args)

def get_percent(x, fu):
    return (x / fu * 100)


def get_help(var):
    helps = {
        'abs': "Returns the absolute value of x",
        'acos': "Returns the arccosine of x",
        'asin': "Returns the arcsine of x",
        'atan': "Returns the arctangent of x",
        'ceil': "Returns the value of x rounded up to its nearest integer",
        'cos': "Returns the cosine of x",
        'cosh': "Returns the hyperbolic cosine of x",
        'exp': "Returns the value of Ex",
        'fabs': "Returns the absolute value of a floating x",
        'floor': "Returns the value of x rounded down to its nearest integer",
        'fmod': "Returns the floating point remainder of x/y",
        'hypot': "Returns sqrt(x2 +y2) without intermediate overflow or underflow",
        'pow': "Returns the value of x to the power of y",
        'sin': "Returns the sine of x (x is in radians)",
        'sinh': "Returns the hyperbolic sine of a double value",
        'tan': "Returns the tangent of an angle",
        'tanh': "Returns the hyperbolic tangent of a double value",
        'set': "Define new variables set(x = 10; y = 20; c = 30)",

        '+': "Addition Adds together two values x + y",
        '-': "Subtraction Subtracts one value from another  x - y",
        '*': "Multiplication Multiplies two values  x * y",
        '/': "Division Divides one value by another  x / y",
        '%': "Modulus Returns the division remainder  x % y",
        }

    try:
        return helps[var]
    except KeyError:
        return ""
