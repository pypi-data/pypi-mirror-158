"""
@generated by codestare-proto-plus.  Do not edit manually!
"""
from builtins import (
    str,
)

from proto import (
    Field,
    STRING,
    module,
)

from proto.message import (
    Message,
)


__protobuf__ = module(
    package="ubii.proto.v1.servers",
    marshal="ubii.proto.v1",
    manifest={
        "Server",
    }
)


class Server(Message):
    """
    Attributes:
        id (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        name (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        ip_ethernet (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        ip_wlan (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        port_service_zmq (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        port_service_rest (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        port_topic_data_zmq (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        port_topic_data_ws (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        constants_json (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        external_address_service_zmq (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        external_address_service_http_json (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        external_address_service_http_binary (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        external_address_topic_data_zmq (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
        external_address_topic_data_ws (proto.fields.Field): :obj:`~proto.fields.Field` of type
            :obj:`~proto.primitives.ProtoType.STRING`
    """

    id: str = Field(
        STRING,
        number=1,
    )
    name: str = Field(
        STRING,
        number=2,
    )
    ip_ethernet: str = Field(
        STRING,
        number=3,
    )
    ip_wlan: str = Field(
        STRING,
        number=4,
    )
    port_service_zmq: str = Field(
        STRING,
        number=5,
    )
    port_service_rest: str = Field(
        STRING,
        number=6,
    )
    port_topic_data_zmq: str = Field(
        STRING,
        number=7,
    )
    port_topic_data_ws: str = Field(
        STRING,
        number=8,
    )
    constants_json: str = Field(
        STRING,
        number=9,
    )
    external_address_service_zmq: str = Field(
        STRING,
        number=10,
    )
    external_address_service_http_json: str = Field(
        STRING,
        number=11,
    )
    external_address_service_http_binary: str = Field(
        STRING,
        number=12,
    )
    external_address_topic_data_zmq: str = Field(
        STRING,
        number=13,
    )
    external_address_topic_data_ws: str = Field(
        STRING,
        number=14,
    )

