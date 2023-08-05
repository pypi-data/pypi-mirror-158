# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spaceone/api/monitoring/v1/event.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from spaceone.api.core.v1 import query_pb2 as spaceone_dot_api_dot_core_dot_v1_dot_query__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&spaceone/api/monitoring/v1/event.proto\x12\x1aspaceone.api.monitoring.v1\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto\x1a spaceone/api/core/v1/query.proto\"I\n\rEventResource\x12\x13\n\x0bresource_id\x18\x01 \x01(\t\x12\x15\n\rresource_type\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\"c\n\x12\x43reateEventRequest\x12\x12\n\nwebhook_id\x18\x01 \x01(\t\x12\x12\n\naccess_key\x18\x02 \x01(\t\x12%\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x17.google.protobuf.Struct\"D\n\x0fGetEventRequest\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t\x12\x11\n\tdomain_id\x18\x02 \x01(\t\x12\x0c\n\x04only\x18\x03 \x03(\t\"\x88\x02\n\nEventQuery\x12*\n\x05query\x18\x01 \x01(\x0b\x32\x1b.spaceone.api.core.v1.Query\x12\x10\n\x08\x65vent_id\x18\x02 \x01(\t\x12\x11\n\tevent_key\x18\x03 \x01(\t\x12\x12\n\nevent_type\x18\x04 \x01(\t\x12\x10\n\x08severity\x18\x05 \x01(\t\x12\x13\n\x0bresource_id\x18\x06 \x01(\t\x12\x10\n\x08provider\x18\x07 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x08 \x01(\t\x12\x10\n\x08\x61lert_id\x18\x0b \x01(\t\x12\x12\n\nwebhook_id\x18\x0c \x01(\t\x12\x12\n\nproject_id\x18\r \x01(\t\x12\x11\n\tdomain_id\x18\x0e \x01(\t\"\xce\x03\n\tEventInfo\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t\x12\x11\n\tevent_key\x18\x02 \x01(\t\x12\x12\n\nevent_type\x18\x03 \x01(\t\x12\r\n\x05title\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x10\n\x08severity\x18\x06 \x01(\t\x12\x0c\n\x04rule\x18\x07 \x01(\t\x12;\n\x08resource\x18\x08 \x01(\x0b\x32).spaceone.api.monitoring.v1.EventResource\x12\x10\n\x08provider\x18\t \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\n \x01(\t\x12\x11\n\timage_url\x18\x0b \x01(\t\x12)\n\x08raw_data\x18\x15 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x30\n\x0f\x61\x64\x64itional_info\x18\x16 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x10\n\x08\x61lert_id\x18\x1f \x01(\t\x12\x12\n\nwebhook_id\x18  \x01(\t\x12\x12\n\nproject_id\x18! \x01(\t\x12\x11\n\tdomain_id\x18\" \x01(\t\x12\x12\n\ncreated_at\x18) \x01(\t\x12\x13\n\x0boccurred_at\x18* \x01(\t\"Y\n\nEventsInfo\x12\x36\n\x07results\x18\x01 \x03(\x0b\x32%.spaceone.api.monitoring.v1.EventInfo\x12\x13\n\x0btotal_count\x18\x02 \x01(\x05\"Y\n\x0e\x45ventStatQuery\x12\x34\n\x05query\x18\x01 \x01(\x0b\x32%.spaceone.api.core.v1.StatisticsQuery\x12\x11\n\tdomain_id\x18\x02 \x01(\t2\xa9\x04\n\x05\x45vent\x12\x91\x01\n\x06\x63reate\x12..spaceone.api.monitoring.v1.CreateEventRequest\x1a\x16.google.protobuf.Empty\"?\x82\xd3\xe4\x93\x02\x39\"7/monitoring/v1/webhook/{webhook_id}/{access_key}/events\x12\x82\x01\n\x03get\x12+.spaceone.api.monitoring.v1.GetEventRequest\x1a%.spaceone.api.monitoring.v1.EventInfo\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/monitoring/v1/event/{event_id}\x12\x95\x01\n\x04list\x12&.spaceone.api.monitoring.v1.EventQuery\x1a&.spaceone.api.monitoring.v1.EventsInfo\"=\x82\xd3\xe4\x93\x02\x37\x12\x15/monitoring/v1/eventsZ\x1e\"\x1c/monitoring/v1/events/search\x12o\n\x04stat\x12*.spaceone.api.monitoring.v1.EventStatQuery\x1a\x17.google.protobuf.Struct\"\"\x82\xd3\xe4\x93\x02\x1c\"\x1a/monitoring/v1/events/statb\x06proto3')



_EVENTRESOURCE = DESCRIPTOR.message_types_by_name['EventResource']
_CREATEEVENTREQUEST = DESCRIPTOR.message_types_by_name['CreateEventRequest']
_GETEVENTREQUEST = DESCRIPTOR.message_types_by_name['GetEventRequest']
_EVENTQUERY = DESCRIPTOR.message_types_by_name['EventQuery']
_EVENTINFO = DESCRIPTOR.message_types_by_name['EventInfo']
_EVENTSINFO = DESCRIPTOR.message_types_by_name['EventsInfo']
_EVENTSTATQUERY = DESCRIPTOR.message_types_by_name['EventStatQuery']
EventResource = _reflection.GeneratedProtocolMessageType('EventResource', (_message.Message,), {
  'DESCRIPTOR' : _EVENTRESOURCE,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventResource)
  })
_sym_db.RegisterMessage(EventResource)

CreateEventRequest = _reflection.GeneratedProtocolMessageType('CreateEventRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEEVENTREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.CreateEventRequest)
  })
_sym_db.RegisterMessage(CreateEventRequest)

GetEventRequest = _reflection.GeneratedProtocolMessageType('GetEventRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETEVENTREQUEST,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.GetEventRequest)
  })
_sym_db.RegisterMessage(GetEventRequest)

EventQuery = _reflection.GeneratedProtocolMessageType('EventQuery', (_message.Message,), {
  'DESCRIPTOR' : _EVENTQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventQuery)
  })
_sym_db.RegisterMessage(EventQuery)

EventInfo = _reflection.GeneratedProtocolMessageType('EventInfo', (_message.Message,), {
  'DESCRIPTOR' : _EVENTINFO,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventInfo)
  })
_sym_db.RegisterMessage(EventInfo)

EventsInfo = _reflection.GeneratedProtocolMessageType('EventsInfo', (_message.Message,), {
  'DESCRIPTOR' : _EVENTSINFO,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventsInfo)
  })
_sym_db.RegisterMessage(EventsInfo)

EventStatQuery = _reflection.GeneratedProtocolMessageType('EventStatQuery', (_message.Message,), {
  'DESCRIPTOR' : _EVENTSTATQUERY,
  '__module__' : 'spaceone.api.monitoring.v1.event_pb2'
  # @@protoc_insertion_point(class_scope:spaceone.api.monitoring.v1.EventStatQuery)
  })
_sym_db.RegisterMessage(EventStatQuery)

_EVENT = DESCRIPTOR.services_by_name['Event']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _EVENT.methods_by_name['create']._options = None
  _EVENT.methods_by_name['create']._serialized_options = b'\202\323\344\223\0029\"7/monitoring/v1/webhook/{webhook_id}/{access_key}/events'
  _EVENT.methods_by_name['get']._options = None
  _EVENT.methods_by_name['get']._serialized_options = b'\202\323\344\223\002!\022\037/monitoring/v1/event/{event_id}'
  _EVENT.methods_by_name['list']._options = None
  _EVENT.methods_by_name['list']._serialized_options = b'\202\323\344\223\0027\022\025/monitoring/v1/eventsZ\036\"\034/monitoring/v1/events/search'
  _EVENT.methods_by_name['stat']._options = None
  _EVENT.methods_by_name['stat']._serialized_options = b'\202\323\344\223\002\034\"\032/monitoring/v1/events/stat'
  _EVENTRESOURCE._serialized_start=193
  _EVENTRESOURCE._serialized_end=266
  _CREATEEVENTREQUEST._serialized_start=268
  _CREATEEVENTREQUEST._serialized_end=367
  _GETEVENTREQUEST._serialized_start=369
  _GETEVENTREQUEST._serialized_end=437
  _EVENTQUERY._serialized_start=440
  _EVENTQUERY._serialized_end=704
  _EVENTINFO._serialized_start=707
  _EVENTINFO._serialized_end=1169
  _EVENTSINFO._serialized_start=1171
  _EVENTSINFO._serialized_end=1260
  _EVENTSTATQUERY._serialized_start=1262
  _EVENTSTATQUERY._serialized_end=1351
  _EVENT._serialized_start=1354
  _EVENT._serialized_end=1907
# @@protoc_insertion_point(module_scope)
