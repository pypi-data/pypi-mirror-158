from typing import overload
import typing

import System
import System.Runtime.InteropServices.Marshalling

System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T = typing.TypeVar("System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T")
System_Runtime_InteropServices_Marshalling_PointerArrayMarshaller_T = typing.TypeVar("System_Runtime_InteropServices_Marshalling_PointerArrayMarshaller_T")


class ArrayMarshaller(typing.Generic[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T]):
    """Marshaller for arrays"""

    @overload
    def __init__(self, sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the ArrayMarshaller{T}.
        
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    @overload
    def __init__(self, array: typing.List[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T], sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the ArrayMarshaller{T}.
        
        :param array: Array to be marshalled.
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    @overload
    def __init__(self, array: typing.List[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T], buffer: System.Span[int], sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the ArrayMarshaller{T}.
        
        :param array: Array to be marshalled.
        :param buffer: Buffer that may be used for marshalling.
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    def FreeNative(self) -> None:
        """Frees native resources."""
        ...

    def FromNativeValue(self, value: typing.Any) -> None:
        """
        Sets the native value representing the array.
        
        :param value: The native value.
        """
        ...

    def GetManagedValuesDestination(self, length: int) -> System.Span[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T]:
        """
        Gets a span that points to the memory where the unmarshalled managed values of the array should be stored.
        
        :param length: Length of the array.
        :returns: Span where managed values of the array should be stored.
        """
        ...

    def GetManagedValuesSource(self) -> System.ReadOnlySpan[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T]:
        """
        Gets a span that points to the memory where the managed values of the array are stored.
        
        :returns: Span over managed values of the array.
        """
        ...

    def GetNativeValuesDestination(self) -> System.Span[int]:
        """
        Returns a span that points to the memory where the native values of the array should be stored.
        
        :returns: Span where native values of the array should be stored.
        """
        ...

    def GetNativeValuesSource(self, length: int) -> System.ReadOnlySpan[int]:
        """
        Returns a span that points to the memory where the native values of the array are stored after the native call.
        
        :param length: Length of the array.
        :returns: Span over the native values of the array.
        """
        ...

    def GetPinnableReference(self) -> typing.Any:
        """Returns a reference to the marshalled array."""
        ...

    def ToManaged(self) -> typing.List[System_Runtime_InteropServices_Marshalling_ArrayMarshaller_T]:
        """Returns the managed array."""
        ...

    def ToNativeValue(self) -> typing.Any:
        """Returns the native value representing the array."""
        ...


class Utf16StringMarshaller(System.Object):
    """Marshaller for UTF-16 strings"""

    @staticmethod
    def ConvertToManaged(unmanaged: typing.Any) -> str:
        """
        Convert an unmanaged string to a managed version.
        
        :param unmanaged: An unmanaged string
        :returns: A managed string.
        """
        ...

    @staticmethod
    def ConvertToUnmanaged(managed: str) -> typing.Any:
        """
        Convert a string to an unmanaged version.
        
        :param managed: A managed string
        :returns: An unmanaged string.
        """
        ...

    @staticmethod
    def Free(unmanaged: typing.Any) -> None:
        """
        Free the memory for the unmanaged string.
        
        :param unmanaged: Memory allocated for the unmanaged string.
        """
        ...

    @staticmethod
    def GetPinnableReference(str: str) -> typing.Any:
        """
        Get a pinnable reference for the string.
        
        :param str: The string.
        :returns: A pinnable reference.
        """
        ...


class AnsiStringMarshaller(System.Object):
    """Marshaller for ANSI strings"""

    class ManagedToUnmanagedIn:
        """Custom marshaller to marshal a managed string as a ANSI unmanaged string."""

        BufferSize: int
        """Requested buffer size for optimized marshalling."""

        def Free(self) -> None:
            """Free any allocated unmanaged string."""
            ...

        def FromManaged(self, managed: str, buffer: System.Span[int]) -> None:
            """
            Initialize the marshaller with a managed string and requested buffer.
            
            :param managed: The managed string
            :param buffer: A request buffer of at least size, BufferSize.
            """
            ...

        def ToUnmanaged(self) -> typing.Any:
            """
            Convert the current manage string to an unmanaged string.
            
            :returns: The unmanaged string.
            """
            ...

    @staticmethod
    def ConvertToManaged(unmanaged: typing.Any) -> str:
        """
        Convert an unmanaged string to a managed version.
        
        :param unmanaged: An unmanaged string
        :returns: A managed string.
        """
        ...

    @staticmethod
    def ConvertToUnmanaged(managed: str) -> typing.Any:
        """
        Convert a string to an unmanaged version.
        
        :param managed: A managed string
        :returns: An unmanaged string.
        """
        ...

    @staticmethod
    def Free(unmanaged: typing.Any) -> None:
        """
        Free the memory for the unmanaged string.
        
        :param unmanaged: Memory allocated for the unmanaged string.
        """
        ...


class MarshalMode(System.Enum):
    """An enumeration representing the different marshalling modes in our marshalling model."""

    Default = 0
    """
    All modes. A marshaller specified with this mode will be used if there is not a specific
    marshaller specified for a given usage mode.
    """

    ManagedToUnmanagedIn = 1
    """By-value and in parameters in managed-to-unmanaged scenarios, like P/Invoke."""

    ManagedToUnmanagedRef = 2
    """ref parameters in managed-to-unmanaged scenarios, like P/Invoke."""

    ManagedToUnmanagedOut = 3
    """out parameters in managed-to-unmanaged scenarios, like P/Invoke."""

    UnmanagedToManagedIn = 4
    """By-value and in parameters in unmanaged-to-managed scenarios, like Reverse P/Invoke."""

    UnmanagedToManagedRef = 5
    """ref parameters in unmanaged-to-managed scenarios, like Reverse P/Invoke."""

    UnmanagedToManagedOut = 6
    """out parameters in unmanaged-to-managed scenarios, like Reverse P/Invoke."""

    ElementIn = 7
    """Elements of arrays passed with in or by-value in interop scenarios."""

    ElementRef = 8
    """Elements of arrays passed with ref or passed by-value with both InAttribute and OutAttribute in interop scenarios."""

    ElementOut = 9
    """Elements of arrays passed with out or passed by-value with only OutAttribute in interop scenarios."""


class CustomMarshallerAttribute(System.Attribute):
    """Attribute to indicate an entry point type for defining a marshaller."""

    class GenericPlaceholder:
        """Placeholder type for generic parameter"""

    @property
    def ManagedType(self) -> typing.Type:
        """The managed type to marshal."""
        ...

    @property
    def MarshalMode(self) -> int:
        """
        The marshalling mode this attribute applies to.
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.MarshalMode enum.
        """
        ...

    @property
    def MarshallerType(self) -> typing.Type:
        """Type used for marshalling."""
        ...

    def __init__(self, managedType: typing.Type, marshalMode: System.Runtime.InteropServices.Marshalling.MarshalMode, marshallerType: typing.Type) -> None:
        """
        Create a CustomMarshallerAttribute instance.
        
        :param managedType: Managed type to marshal.
        :param marshalMode: The marshalling mode this attribute applies to.
        :param marshallerType: Type used for marshalling.
        """
        ...


class MarshalUsingAttribute(System.Attribute):
    """Attribute used to provide a custom marshaller type or size information for marshalling."""

    @property
    def NativeType(self) -> typing.Type:
        """The marshaller type used to convert the attributed type from managed to native code. This type must be attributed with CustomTypeMarshallerAttribute"""
        ...

    @property
    def CountElementName(self) -> str:
        """The name of the parameter that will provide the size of the collection when marshalling from unmanaged to managed, or ReturnsCountValue if the return value provides the size."""
        ...

    @CountElementName.setter
    def CountElementName(self, value: str):
        """The name of the parameter that will provide the size of the collection when marshalling from unmanaged to managed, or ReturnsCountValue if the return value provides the size."""
        ...

    @property
    def ConstantElementCount(self) -> int:
        """If a collection is constant size, the size of the collection when marshalling from unmanaged to managed."""
        ...

    @ConstantElementCount.setter
    def ConstantElementCount(self, value: int):
        """If a collection is constant size, the size of the collection when marshalling from unmanaged to managed."""
        ...

    @property
    def ElementIndirectionDepth(self) -> int:
        """What indirection depth this marshalling info is provided for."""
        ...

    @ElementIndirectionDepth.setter
    def ElementIndirectionDepth(self, value: int):
        """What indirection depth this marshalling info is provided for."""
        ...

    ReturnsCountValue: str = "return-value"
    """A constant string that represents the name of the return value for CountElementName."""

    @overload
    def __init__(self) -> None:
        """Create a MarshalUsingAttribute that provides only size information."""
        ...

    @overload
    def __init__(self, nativeType: typing.Type) -> None:
        """
        Create a MarshalUsingAttribute that provides a native marshalling type and optionally size information.
        
        :param nativeType: The marshaller type used to convert the attributed type from managed to native code. This type must be attributed with CustomTypeMarshallerAttribute
        """
        ...


class CustomTypeMarshallerDirection(System.Enum):
    """A direction of marshalling data into or out of the managed environment"""

    # Cannot convert to Python: None = 0
    """No marshalling direction"""

    In = ...
    """Marshalling from a managed environment to an unmanaged environment"""

    Out = ...
    """Marshalling from an unmanaged environment to a managed environment"""

    Ref = ...
    """Marshalling to and from managed and unmanaged environments"""


class BStrStringMarshaller(System.Object):
    """Marshaller for BSTR strings"""

    class ManagedToUnmanagedIn:
        """Custom marshaller to marshal a managed string as a ANSI unmanaged string."""

        BufferSize: int
        """Requested buffer size for optimized marshalling."""

        def Free(self) -> None:
            """Free any allocated unmanaged string."""
            ...

        def FromManaged(self, managed: str, buffer: System.Span[int]) -> None:
            """
            Initialize the marshaller with a managed string and requested buffer.
            
            :param managed: The managed string
            :param buffer: A request buffer of at least size, BufferSize.
            """
            ...

        def ToUnmanaged(self) -> typing.Any:
            """
            Convert the current manage string to an unmanaged string.
            
            :returns: The unmanaged string.
            """
            ...

    @staticmethod
    def ConvertToManaged(unmanaged: typing.Any) -> str:
        """
        Convert an unmanaged string to a managed version.
        
        :param unmanaged: An unmanaged string
        :returns: A managed string.
        """
        ...

    @staticmethod
    def ConvertToUnmanaged(managed: str) -> typing.Any:
        """
        Convert a string to an unmanaged version.
        
        :param managed: A managed string
        :returns: An unmanaged string.
        """
        ...

    @staticmethod
    def Free(unmanaged: typing.Any) -> None:
        """
        Free the memory for the unmanaged string.
        
        :param unmanaged: Memory allocated for the unmanaged string.
        """
        ...


class Utf8StringMarshaller(System.Object):
    """Marshaller for UTF-8 strings"""

    class ManagedToUnmanagedIn:
        """Custom marshaller to marshal a managed string as a UTF-8 unmanaged string."""

        BufferSize: int
        """Requested buffer size for optimized marshalling."""

        def Free(self) -> None:
            """Free any allocated unmanaged string."""
            ...

        def FromManaged(self, managed: str, buffer: System.Span[int]) -> None:
            """
            Initialize the marshaller with a managed string and requested buffer.
            
            :param managed: The managed string
            :param buffer: A request buffer of at least size, BufferSize.
            """
            ...

        def ToUnmanaged(self) -> typing.Any:
            """
            Convert the current manage string to an unmanaged string.
            
            :returns: The unmanaged string.
            """
            ...

    @staticmethod
    def ConvertToManaged(unmanaged: typing.Any) -> str:
        """
        Convert an unmanaged string to a managed version.
        
        :param unmanaged: An unmanaged string
        :returns: A managed string.
        """
        ...

    @staticmethod
    def ConvertToUnmanaged(managed: str) -> typing.Any:
        """
        Convert a string to an unmanaged version.
        
        :param managed: A managed string
        :returns: An unmanaged string.
        """
        ...

    @staticmethod
    def Free(unmanaged: typing.Any) -> None:
        """
        Free the memory for the unmanaged string.
        
        :param unmanaged: Memory allocated for the unmanaged string.
        """
        ...


class PointerArrayMarshaller(typing.Generic[System_Runtime_InteropServices_Marshalling_PointerArrayMarshaller_T]):
    """Marshaller for arrays of pointers"""

    @overload
    def __init__(self, sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the PointerArrayMarshaller{T}.
        
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    @overload
    def __init__(self, array: typing.List[typing.Any], sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the PointerArrayMarshaller{T}.
        
        :param array: Array to be marshalled.
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    @overload
    def __init__(self, array: typing.List[typing.Any], buffer: System.Span[int], sizeOfNativeElement: int) -> None:
        """
        Initializes a new instance of the PointerArrayMarshaller{T}.
        
        :param array: Array to be marshalled.
        :param buffer: Buffer that may be used for marshalling.
        :param sizeOfNativeElement: Size of the native element in bytes.
        """
        ...

    def FreeNative(self) -> None:
        """Frees native resources."""
        ...

    def FromNativeValue(self, value: typing.Any) -> None:
        """
        Sets the native value representing the array.
        
        :param value: The native value.
        """
        ...

    def GetManagedValuesDestination(self, length: int) -> System.Span[System.IntPtr]:
        """
        Gets a span that points to the memory where the unmarshalled managed values of the array should be stored.
        
        :param length: Length of the array.
        :returns: Span where managed values of the array should be stored.
        """
        ...

    def GetManagedValuesSource(self) -> System.ReadOnlySpan[System.IntPtr]:
        """
        Gets a span that points to the memory where the managed values of the array are stored.
        
        :returns: Span over managed values of the array.
        """
        ...

    def GetNativeValuesDestination(self) -> System.Span[int]:
        """
        Returns a span that points to the memory where the native values of the array should be stored.
        
        :returns: Span where native values of the array should be stored.
        """
        ...

    def GetNativeValuesSource(self, length: int) -> System.ReadOnlySpan[int]:
        """
        Returns a span that points to the memory where the native values of the array are stored after the native call.
        
        :param length: Length of the array.
        :returns: Span over the native values of the array.
        """
        ...

    def GetPinnableReference(self) -> typing.Any:
        """Returns a reference to the marshalled array."""
        ...

    def ToManaged(self) -> typing.List[typing.Any]:
        """Returns the managed array."""
        ...

    def ToNativeValue(self) -> typing.Any:
        """Returns the native value representing the array."""
        ...


class CustomTypeMarshallerKind(System.Enum):
    """The shape of a custom type marshaller for usage in source-generated interop scenarios."""

    Value = 0
    """This custom type marshaller represents a single value."""

    LinearCollection = 1
    """This custom type marshaller represents a container of values that are placed sequentially in memory."""


class CustomTypeMarshallerAttribute(System.Attribute):
    """Attribute used to indicate that the type can be used to convert a value of the provided ManagedType to a native representation."""

    class GenericPlaceholder:
        """
        This type is used as a placeholder for the first generic parameter when generic parameters cannot be used
        to identify the managed type (i.e. when the marshaller type is generic over T and the managed type is T[])
        """

    @property
    def ManagedType(self) -> typing.Type:
        """The managed type for which the attributed type is a marshaller"""
        ...

    @property
    def MarshallerKind(self) -> int:
        """
        The required shape of the attributed type
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerKind enum.
        """
        ...

    @property
    def BufferSize(self) -> int:
        """When the CustomTypeMarshallerFeatures.CallerAllocatedBuffer flag is set on Features the size of the caller-allocated buffer in number of elements."""
        ...

    @BufferSize.setter
    def BufferSize(self, value: int):
        """When the CustomTypeMarshallerFeatures.CallerAllocatedBuffer flag is set on Features the size of the caller-allocated buffer in number of elements."""
        ...

    @property
    def Direction(self) -> int:
        """
        The marshalling directions this custom type marshaller supports.
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerDirection enum.
        """
        ...

    @Direction.setter
    def Direction(self, value: int):
        """
        The marshalling directions this custom type marshaller supports.
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerDirection enum.
        """
        ...

    @property
    def Features(self) -> int:
        """
        The optional features for the MarshallerKind that the marshaller supports.
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerFeatures enum.
        """
        ...

    @Features.setter
    def Features(self, value: int):
        """
        The optional features for the MarshallerKind that the marshaller supports.
        
        This property contains the int value of a member of the System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerFeatures enum.
        """
        ...

    def __init__(self, managedType: typing.Type, marshallerKind: System.Runtime.InteropServices.Marshalling.CustomTypeMarshallerKind = ...) -> None:
        ...


class CustomTypeMarshallerFeatures(System.Enum):
    """Optional features supported by custom type marshallers."""

    # Cannot convert to Python: None = 0
    """No optional features supported"""

    UnmanagedResources = ...
    """The marshaller owns unmanaged resources that must be freed"""

    CallerAllocatedBuffer = ...
    """The marshaller can use a caller-allocated buffer instead of allocating in some scenarios"""

    TwoStageMarshalling = ...
    """The marshaller uses the two-stage marshalling design for its CustomTypeMarshallerKind instead of the one-stage design."""


class NativeMarshallingAttribute(System.Attribute):
    """Attribute used to provide a default custom marshaller type for a given managed type."""

    @property
    def NativeType(self) -> typing.Type:
        """The marshaller type used to convert the attributed type from managed to native code. This type must be attributed with CustomTypeMarshallerAttribute"""
        ...

    def __init__(self, nativeType: typing.Type) -> None:
        """
        Create a NativeMarshallingAttribute that provides a native marshalling type.
        
        :param nativeType: The marshaller type used to convert the attributed type from managed to native code. This type must be attributed with CustomTypeMarshallerAttribute
        """
        ...


