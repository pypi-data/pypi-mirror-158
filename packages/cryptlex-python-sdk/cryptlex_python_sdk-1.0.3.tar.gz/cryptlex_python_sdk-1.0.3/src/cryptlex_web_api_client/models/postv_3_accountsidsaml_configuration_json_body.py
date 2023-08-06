from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.saml_role_mapping_request_model import SamlRoleMappingRequestModel
from ..types import UNSET, Unset

T = TypeVar("T", bound="Postv3AccountsidsamlConfigurationJsonBody")


@attr.s(auto_attribs=True)
class Postv3AccountsidsamlConfigurationJsonBody:
    """
    Attributes:
        metadata_url (Union[Unset, str]): SAML metadata xml url.
        assertion_consumer_service_url (Union[Unset, str]): SAML assertion consumer service url.
        return_url (Union[Unset, str]): Redirect url after successful authentication.
        entity_id (Union[Unset, str]): Entity Id of SAML service provider.
        auto_provision_users (Union[Unset, bool]): Auto provision users.
        enabled (Union[Unset, bool]): Enable or disable the SAML SSO.
        saml_role_mappings (Union[Unset, None, List[SamlRoleMappingRequestModel]]): Role mapping.
    """

    metadata_url: Union[Unset, str] = UNSET
    assertion_consumer_service_url: Union[Unset, str] = UNSET
    return_url: Union[Unset, str] = UNSET
    entity_id: Union[Unset, str] = UNSET
    auto_provision_users: Union[Unset, bool] = UNSET
    enabled: Union[Unset, bool] = UNSET
    saml_role_mappings: Union[Unset, None, List[SamlRoleMappingRequestModel]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        metadata_url = self.metadata_url
        assertion_consumer_service_url = self.assertion_consumer_service_url
        return_url = self.return_url
        entity_id = self.entity_id
        auto_provision_users = self.auto_provision_users
        enabled = self.enabled
        saml_role_mappings: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.saml_role_mappings, Unset):
            if self.saml_role_mappings is None:
                saml_role_mappings = None
            else:
                saml_role_mappings = []
                for saml_role_mappings_item_data in self.saml_role_mappings:
                    saml_role_mappings_item = saml_role_mappings_item_data.to_dict()

                    saml_role_mappings.append(saml_role_mappings_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if metadata_url is not UNSET:
            field_dict["metadataUrl"] = metadata_url
        if assertion_consumer_service_url is not UNSET:
            field_dict["assertionConsumerServiceUrl"] = assertion_consumer_service_url
        if return_url is not UNSET:
            field_dict["returnUrl"] = return_url
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if auto_provision_users is not UNSET:
            field_dict["autoProvisionUsers"] = auto_provision_users
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if saml_role_mappings is not UNSET:
            field_dict["samlRoleMappings"] = saml_role_mappings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        metadata_url = d.pop("metadataUrl", UNSET)

        assertion_consumer_service_url = d.pop("assertionConsumerServiceUrl", UNSET)

        return_url = d.pop("returnUrl", UNSET)

        entity_id = d.pop("entityId", UNSET)

        auto_provision_users = d.pop("autoProvisionUsers", UNSET)

        enabled = d.pop("enabled", UNSET)

        saml_role_mappings = []
        _saml_role_mappings = d.pop("samlRoleMappings", UNSET)
        for saml_role_mappings_item_data in _saml_role_mappings or []:
            saml_role_mappings_item = SamlRoleMappingRequestModel.from_dict(saml_role_mappings_item_data)

            saml_role_mappings.append(saml_role_mappings_item)

        postv_3_accountsidsaml_configuration_json_body = cls(
            metadata_url=metadata_url,
            assertion_consumer_service_url=assertion_consumer_service_url,
            return_url=return_url,
            entity_id=entity_id,
            auto_provision_users=auto_provision_users,
            enabled=enabled,
            saml_role_mappings=saml_role_mappings,
        )

        postv_3_accountsidsaml_configuration_json_body.additional_properties = d
        return postv_3_accountsidsaml_configuration_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
