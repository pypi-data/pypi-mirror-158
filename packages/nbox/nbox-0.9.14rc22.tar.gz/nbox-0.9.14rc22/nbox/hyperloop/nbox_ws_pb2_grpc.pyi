"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import google.protobuf.empty_pb2
import google.protobuf.wrappers_pb2
import grpc
import job_pb2
import nbox_ws_pb2
import typing

class WSJobServiceStub:
    """
    WSJobService is used by nbox to interface with Web Server. WSJobService manages
    DB and NBX Platform Information. All compute resource related actions are fowarded
    to WSJobsService running on AWS.

    // Generated according to https://cloud.google.com/apis/design/standard_methods
    """
    def __init__(self, channel: grpc.Channel) -> None: ...
    GetJob: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.JobInfo,
        job_pb2.Job]
    """GetJob returns the job with the given info"""

    ListJobs: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.ListJobsRequest,
        nbox_ws_pb2.ListJobsResponse]
    """ListJobs returns a list of jobs for the given workspace/user"""

    UploadJobCode: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.UploadCodeRequest,
        job_pb2.Job]
    """To upload Job Code to S3"""

    CreateJob: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.CreateJobRequest,
        job_pb2.Job]
    """CreateJob creates a new job"""

    UpdateJob: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.UpdateJobRequest,
        job_pb2.Job]
    """UpdateJob updates the given job"""

    DeleteJob: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.JobInfo,
        google.protobuf.empty_pb2.Empty]
    """DeleteJob deletes the given job"""

    GetJobLogs: grpc.UnaryStreamMultiCallable[
        nbox_ws_pb2.JobLogsRequest,
        nbox_ws_pb2.JobLog]
    """GetJobLogs returns logs from given job"""

    TriggerJob: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.JobInfo,
        google.protobuf.wrappers_pb2.BoolValue]
    """TriggerJob triggers the given job"""

    UpdateRun: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.UpdateRunRequest,
        google.protobuf.empty_pb2.Empty]
    """UpdateRun update the run for given job"""

    GetRunToken: grpc.UnaryUnaryMultiCallable[
        nbox_ws_pb2.JobInfo,
        google.protobuf.wrappers_pb2.StringValue]
    """GetRunToken returns a tokn to be used for `/UpdateRun`"""


class WSJobServiceServicer(metaclass=abc.ABCMeta):
    """
    WSJobService is used by nbox to interface with Web Server. WSJobService manages
    DB and NBX Platform Information. All compute resource related actions are fowarded
    to WSJobsService running on AWS.

    // Generated according to https://cloud.google.com/apis/design/standard_methods
    """
    @abc.abstractmethod
    def GetJob(self,
        request: nbox_ws_pb2.JobInfo,
        context: grpc.ServicerContext,
    ) -> job_pb2.Job:
        """GetJob returns the job with the given info"""
        pass

    @abc.abstractmethod
    def ListJobs(self,
        request: nbox_ws_pb2.ListJobsRequest,
        context: grpc.ServicerContext,
    ) -> nbox_ws_pb2.ListJobsResponse:
        """ListJobs returns a list of jobs for the given workspace/user"""
        pass

    @abc.abstractmethod
    def UploadJobCode(self,
        request: nbox_ws_pb2.UploadCodeRequest,
        context: grpc.ServicerContext,
    ) -> job_pb2.Job:
        """To upload Job Code to S3"""
        pass

    @abc.abstractmethod
    def CreateJob(self,
        request: nbox_ws_pb2.CreateJobRequest,
        context: grpc.ServicerContext,
    ) -> job_pb2.Job:
        """CreateJob creates a new job"""
        pass

    @abc.abstractmethod
    def UpdateJob(self,
        request: nbox_ws_pb2.UpdateJobRequest,
        context: grpc.ServicerContext,
    ) -> job_pb2.Job:
        """UpdateJob updates the given job"""
        pass

    @abc.abstractmethod
    def DeleteJob(self,
        request: nbox_ws_pb2.JobInfo,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty:
        """DeleteJob deletes the given job"""
        pass

    @abc.abstractmethod
    def GetJobLogs(self,
        request: nbox_ws_pb2.JobLogsRequest,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[nbox_ws_pb2.JobLog]:
        """GetJobLogs returns logs from given job"""
        pass

    @abc.abstractmethod
    def TriggerJob(self,
        request: nbox_ws_pb2.JobInfo,
        context: grpc.ServicerContext,
    ) -> google.protobuf.wrappers_pb2.BoolValue:
        """TriggerJob triggers the given job"""
        pass

    @abc.abstractmethod
    def UpdateRun(self,
        request: nbox_ws_pb2.UpdateRunRequest,
        context: grpc.ServicerContext,
    ) -> google.protobuf.empty_pb2.Empty:
        """UpdateRun update the run for given job"""
        pass

    @abc.abstractmethod
    def GetRunToken(self,
        request: nbox_ws_pb2.JobInfo,
        context: grpc.ServicerContext,
    ) -> google.protobuf.wrappers_pb2.StringValue:
        """GetRunToken returns a tokn to be used for `/UpdateRun`"""
        pass


def add_WSJobServiceServicer_to_server(servicer: WSJobServiceServicer, server: grpc.Server) -> None: ...
