
#
# spyne - Copyright (C) Spyne contributors.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#

from spyne.model import SimpleModel

# adapted from: http://code.activestate.com/recipes/413486/

class EnumBase(SimpleModel):
    __namespace__ = None

    @staticmethod
    def resolve_namespace(cls, default_ns):
        if cls.__namespace__ is None:
            cls.__namespace__ = default_ns

    @staticmethod
    def validate_string(cls, value):
        return (    SimpleModel.validate_string(cls, value)
                and value in cls.__values__
            )

def Enum(*values, **kwargs):
    """The snob enum type. Here's how it's supposed to work:

    >>> from spyne.model.enum import Enum
    >>> SomeEnum = SomeEnum("SomeValue", "SomeOtherValue", type_name="SomeEnum")
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'SomeEnum' is not defined
    >>> SomeEnum = Enum("SomeValue", "SomeOtherValue", type_name="SomeEnum")
    >>> SomeEnum.SomeValue == SomeEnum.SomeOtherValue
    False
    >>> SomeEnum.SomeValue == SomeEnum.SomeValue
    True
    >>> SomeEnum.SomeValue is SomeEnum.SomeValue
    True
    >>> SomeEnum.SomeValue == 0
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/plq/src/github/plq/spyne/spyne/model/enum.py", line 61, in __cmp__
        "Only values from the same enum are comparable"
    >>> SomeEnum2 = Enum("SomeValue", "SomeOtherValue", type_name="SomeEnum")
    >>> SomeEnum2.SomeValue == SomeEnum.SomeValue
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/plq/src/github/plq/spyne/spyne/model/enum.py", line 61, in __cmp__
        In the above example, ``SomeEnum`` can be used as a regular Spyne model.
    AssertionError: Only values from the same enum are comparable

    In the above example, ``SomeEnum`` can be used as a regular Spyne model.
    """

    type_name = kwargs.get('type_name', None)
    docstr = kwargs.get('doc', '')
    if type_name is None:
        raise Exception("Please specify 'type_name' as a keyword argument")

    assert len(values) > 0, "Empty enums are meaningless"

    maximum = len(values) # to make __invert__ work

    class EnumValue(object):
        __slots__ = ('__value')

        def __init__(self, value):
            self.__value = value

        def __hash__(self):
            return hash(self.__value)

        def __cmp__(self, other):
            assert isinstance(self, type(other)), \
                             "Only values from the same enum are comparable"

            return cmp(self.__value, other.__value)

        def __invert__(self):
            return values[maximum - self.__value]

        def __nonzero__(self):
            return bool(self.__value)

        def __bool__(self):
            return bool(self.__value)

        def __repr__(self):
            return str(values[self.__value])

    class EnumType(EnumBase):
        __doc__ = docstr
        __type_name__ = type_name
        __values__ = values

        def __iter__(self):
            return iter(values)

        def __len__(self):
            return len(values)

        def __getitem__(self, i):
            return values[i]

        def __repr__(self):
            return 'Enum' + str(enumerate(values))

        def __str__(self):
            return 'enum ' + str(values)

    for i, v in enumerate(values):
        setattr(EnumType, v, EnumValue(i))

    return EnumType