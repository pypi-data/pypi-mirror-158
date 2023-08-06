from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Project(_message.Message):
    __slots__ = ["atlas_problem_id", "id", "labels", "name", "runtime", "visibility"]
    class Visibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ATLAS_PROBLEM_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    LABELS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRIVATE: Project.Visibility
    PUBLIC: Project.Visibility
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    atlas_problem_id: str
    id: str
    labels: _containers.RepeatedScalarFieldContainer[str]
    name: str
    runtime: str
    visibility: Project.Visibility
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., runtime: _Optional[str] = ..., visibility: _Optional[_Union[Project.Visibility, str]] = ..., atlas_problem_id: _Optional[str] = ..., labels: _Optional[_Iterable[str]] = ...) -> None: ...
