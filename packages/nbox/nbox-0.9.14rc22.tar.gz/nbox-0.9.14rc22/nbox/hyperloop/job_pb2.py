# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: job.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import dag_pb2 as dag__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tjob.proto\x12\x04jobs\x1a\tdag.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x98\x07\n\x03Job\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1c\n\x04\x63ode\x18\x05 \x01(\x0b\x32\x0e.jobs.Job.Code\x12 \n\x08resource\x18\x06 \x01(\x0b\x32\x0e.jobs.Resource\x12\x32\n\rfeature_gates\x18\x07 \x03(\x0b\x32\x1b.jobs.Job.FeatureGatesEntry\x12$\n\tauth_info\x18\x0b \x01(\x0b\x32\x11.jobs.NBXAuthInfo\x12$\n\x08schedule\x18\x0c \x01(\x0b\x32\x12.jobs.Job.Schedule\x12\x1a\n\x03\x64\x61g\x18\r \x01(\x0b\x32\r.jobs.dag.DAG\x12\x0e\n\x06paused\x18\x0e \x01(\x08\x12 \n\x06status\x18\x0f \x01(\x0e\x32\x10.jobs.Job.Status\x12\x1e\n\x07k8sInfo\x18\x10 \x01(\x0b\x32\r.jobs.K8sInfo\x1a\xd7\x01\n\x04\x43ode\x12\x0e\n\x06s3_url\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x05\x12!\n\x04type\x18\x03 \x01(\x0e\x32\x13.jobs.Job.Code.Type\x12+\n\x07s3_meta\x18\x04 \x03(\x0b\x32\x1a.jobs.Job.Code.S3MetaEntry\x1a-\n\x0bS3MetaEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"2\n\x04Type\x12\x0b\n\x07NOT_SET\x10\x00\x12\x08\n\x04NBOX\x10\x01\x12\x07\n\x03ZIP\x10\x02\x12\n\n\x06\x42INARY\x10\x03\x1a\x33\n\x11\x46\x65\x61tureGatesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1al\n\x08Schedule\x12)\n\x05start\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\'\n\x03\x65nd\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04\x63ron\x18\x03 \x01(\t\"\x9b\x01\n\x06Status\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07NOT_SET\x10\x01\x12\r\n\tPREPARING\x10\x02\x12\n\n\x06PAUSED\x10\x03\x12\r\n\tSCHEDULED\x10\x04\x12\n\n\x06\x41\x43TIVE\x10\x05\x12\t\n\x05\x45RROR\x10\x06\x12\r\n\tCOMPLETED\x10\x07\x12\x0c\n\x08\x41RCHIVED\x10\x08\x12\r\n\tCANCELLED\x10\t\x12\n\n\x06KILLED\x10\n\"v\n\x0bNBXAuthInfo\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x14\n\x0cworkspace_id\x18\x02 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x03 \x01(\t\x12\x15\n\rrefresh_token\x18\x04 \x01(\t\x12\x12\n\naccess_key\x18\x05 \x01(\t\")\n\x07K8sInfo\x12\x10\n\x08\x63ron_job\x18\x01 \x01(\t\x12\x0c\n\x04pods\x18\x02 \x03(\t\"\x80\x01\n\x08Resource\x12\x0b\n\x03\x63pu\x18\x01 \x01(\t\x12\x0e\n\x06memory\x18\x02 \x01(\t\x12\x0b\n\x03gpu\x18\x03 \x01(\t\x12\x11\n\tgpu_count\x18\x04 \x01(\t\x12\x11\n\tdisk_size\x18\x05 \x01(\t\x12\x0f\n\x07timeout\x18\x06 \x01(\x03\x12\x13\n\x0bmax_retries\x18\x07 \x01(\x05\x42\x32Z0github.com/NimbleBoxAI/jobs-architecture/jobs_pbb\x06proto3')



_JOB = DESCRIPTOR.message_types_by_name['Job']
_JOB_CODE = _JOB.nested_types_by_name['Code']
_JOB_CODE_S3METAENTRY = _JOB_CODE.nested_types_by_name['S3MetaEntry']
_JOB_FEATUREGATESENTRY = _JOB.nested_types_by_name['FeatureGatesEntry']
_JOB_SCHEDULE = _JOB.nested_types_by_name['Schedule']
_NBXAUTHINFO = DESCRIPTOR.message_types_by_name['NBXAuthInfo']
_K8SINFO = DESCRIPTOR.message_types_by_name['K8sInfo']
_RESOURCE = DESCRIPTOR.message_types_by_name['Resource']
_JOB_CODE_TYPE = _JOB_CODE.enum_types_by_name['Type']
_JOB_STATUS = _JOB.enum_types_by_name['Status']
Job = _reflection.GeneratedProtocolMessageType('Job', (_message.Message,), {

  'Code' : _reflection.GeneratedProtocolMessageType('Code', (_message.Message,), {

    'S3MetaEntry' : _reflection.GeneratedProtocolMessageType('S3MetaEntry', (_message.Message,), {
      'DESCRIPTOR' : _JOB_CODE_S3METAENTRY,
      '__module__' : 'job_pb2'
      # @@protoc_insertion_point(class_scope:jobs.Job.Code.S3MetaEntry)
      })
    ,
    'DESCRIPTOR' : _JOB_CODE,
    '__module__' : 'job_pb2'
    # @@protoc_insertion_point(class_scope:jobs.Job.Code)
    })
  ,

  'FeatureGatesEntry' : _reflection.GeneratedProtocolMessageType('FeatureGatesEntry', (_message.Message,), {
    'DESCRIPTOR' : _JOB_FEATUREGATESENTRY,
    '__module__' : 'job_pb2'
    # @@protoc_insertion_point(class_scope:jobs.Job.FeatureGatesEntry)
    })
  ,

  'Schedule' : _reflection.GeneratedProtocolMessageType('Schedule', (_message.Message,), {
    'DESCRIPTOR' : _JOB_SCHEDULE,
    '__module__' : 'job_pb2'
    # @@protoc_insertion_point(class_scope:jobs.Job.Schedule)
    })
  ,
  'DESCRIPTOR' : _JOB,
  '__module__' : 'job_pb2'
  # @@protoc_insertion_point(class_scope:jobs.Job)
  })
_sym_db.RegisterMessage(Job)
_sym_db.RegisterMessage(Job.Code)
_sym_db.RegisterMessage(Job.Code.S3MetaEntry)
_sym_db.RegisterMessage(Job.FeatureGatesEntry)
_sym_db.RegisterMessage(Job.Schedule)

NBXAuthInfo = _reflection.GeneratedProtocolMessageType('NBXAuthInfo', (_message.Message,), {
  'DESCRIPTOR' : _NBXAUTHINFO,
  '__module__' : 'job_pb2'
  # @@protoc_insertion_point(class_scope:jobs.NBXAuthInfo)
  })
_sym_db.RegisterMessage(NBXAuthInfo)

K8sInfo = _reflection.GeneratedProtocolMessageType('K8sInfo', (_message.Message,), {
  'DESCRIPTOR' : _K8SINFO,
  '__module__' : 'job_pb2'
  # @@protoc_insertion_point(class_scope:jobs.K8sInfo)
  })
_sym_db.RegisterMessage(K8sInfo)

Resource = _reflection.GeneratedProtocolMessageType('Resource', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCE,
  '__module__' : 'job_pb2'
  # @@protoc_insertion_point(class_scope:jobs.Resource)
  })
_sym_db.RegisterMessage(Resource)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z0github.com/NimbleBoxAI/jobs-architecture/jobs_pb'
  _JOB_CODE_S3METAENTRY._options = None
  _JOB_CODE_S3METAENTRY._serialized_options = b'8\001'
  _JOB_FEATUREGATESENTRY._options = None
  _JOB_FEATUREGATESENTRY._serialized_options = b'8\001'
  _JOB._serialized_start=64
  _JOB._serialized_end=984
  _JOB_CODE._serialized_start=448
  _JOB_CODE._serialized_end=663
  _JOB_CODE_S3METAENTRY._serialized_start=566
  _JOB_CODE_S3METAENTRY._serialized_end=611
  _JOB_CODE_TYPE._serialized_start=613
  _JOB_CODE_TYPE._serialized_end=663
  _JOB_FEATUREGATESENTRY._serialized_start=665
  _JOB_FEATUREGATESENTRY._serialized_end=716
  _JOB_SCHEDULE._serialized_start=718
  _JOB_SCHEDULE._serialized_end=826
  _JOB_STATUS._serialized_start=829
  _JOB_STATUS._serialized_end=984
  _NBXAUTHINFO._serialized_start=986
  _NBXAUTHINFO._serialized_end=1104
  _K8SINFO._serialized_start=1106
  _K8SINFO._serialized_end=1147
  _RESOURCE._serialized_start=1150
  _RESOURCE._serialized_end=1278
# @@protoc_insertion_point(module_scope)
