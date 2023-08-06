from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagRequestModel")


@attr.s(auto_attribs=True)
class TagRequestModel:
    """
    Attributes:
        name (Union[Unset, str]): Name for the tag.
        description (Union[Unset, str]): Description for the tag.
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        tag_request_model = cls(
            name=name,
            description=description,
        )

        return tag_request_model
