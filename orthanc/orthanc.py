# coding: utf-8
from typing import List, Dict

import requests
from requests.auth import HTTPBasicAuth


class Orthanc:
    """Wrapper around Orthanc REST API

    You need to know if you need credentials before using this
    object. If yes, you need to set credentials with the method
    `setup_credential`.
    """

    def __init__(self, orthanc_url: str):
        """Constructor

        Parameters
        ----------
        orthanc_url : str
            Orthanc server address
        """
        self._orthanc_url: str = orthanc_url

        self._credentials_are_set: bool = False
        self._credentials: HTTPBasicAuth = None

    def setup_credentials(self, username: str, password: str) -> None:
        """Set credentials needed for HTTP requests

        Parameters
        ----------
        username : Username.
        password : Password.
        """
        self._credentials = HTTPBasicAuth(username, password)
        self._credentials_are_set = True

    def get_request(self, route: str, params: Dict = None,
                    **kwargs) -> requests.Response:
        """GET request with specified route

        Parameters
        ----------
        route : HTTP route.
        params : Params with the HTTP GET request.

        Returns
        -------
        requests.Response
            Response of the HTTP GET request.
        """
        if self._credentials_are_set:
            return requests.get(
                route, params=params, auth=self._credentials, **kwargs)

        return requests.get(route, params=params, **kwargs)

    def delete_request(self, route: str, **kwargs) -> requests.Response:
        """DELETE to specified route

        Parameters
        ----------
        route : HTTP route.

        Returns
        -------
        requests.Response
            Response of the HTTP DELETE request.
        """
        if self._credentials_are_set:
            return requests.delete(route, auth=self._credentials, **kwargs)

        return requests.delete(route, **kwargs)

    def post_request(self, route: str, data: Dict = None, json=None,
                     **kwargs) -> requests.Response:
        """POST to specified route

        Parameters
        ----------
        route : HTTP route.
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Response of the HTTP POST request.
        """
        if self._credentials_are_set:
            return requests.post(
                route, auth=self._credentials, data=data, json=json, **kwargs)

        return requests.post(route, data=data, json=json, **kwargs)

    def put_request(self, route: str, data: Dict = None, json=None,
                    **kwargs) -> requests.Response:
        """PUT to specified route

        Parameters
        ----------
        route : str
        data : Dictionary to send in the body of request.
        json : json to send in the body of request.

        Returns
        -------
        requests.Response
            Response of the HTTP PUT requests
        """
        if self._credentials_are_set:
            return requests.put(
                route, auth=self._credentials, data=data, json=json, **kwargs)

        return requests.put(route, data, json=json, **kwargs)

    def get_attachments(
            self, resource_type: str,
            identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get list of files attached to the object identifier

        List the files that are attached to this patient, study, series or instance

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            List of files attached to the object corresponding to the object identifier
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments',
            params=params,
            **kwargs)

    def get_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment file corresponding to object identifier and attachment's name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment file corresponding to object identifier and attachment's name
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            params=params,
            **kwargs)

    def delete_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            **kwargs) -> requests.Response:
        """Delete attachment by name

        Delete the specified attachment file.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            **kwargs)

    def put_attachment_by_name(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put attachment with given name

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : Data to send in the request's body.
        json : json to send in the request's body.

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}',
            data=data,
            json=json,
            **kwargs)

    def post_compress_attachment(
            self, resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Compress attachment file

        This method should compress the DICOM instance(s).

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        data : Data to send in the request's body.
        json : json to send in the request's body.

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compress',
            data=data,
            json=json,
            **kwargs)

    def get_attachment_compressed_data(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment compressed data

        Return the (possibly compressed) data, as stored on the disk.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            The (possibly compressed) data, as stored on the disk.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_data',
            params=params,
            **kwargs)

    def get_attachment_compressed_data_md5(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment by name as compressed data in md5

        Return the (possibly compressed) data, with md5 encryption.
        Note that md5 is not a safe encryption and should not be used if
        real encryption is needed.

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            The (possibly compressed) data, with md5 encryption.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_md5',
            params=params,
            **kwargs)

    def get_attachment_compressed_size(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment compressed size

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment compressed size.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/compressed_size',
            params=params,
            **kwargs)

    def get_attachment_data(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get attachment data

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            Attachment data.
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/data',
            params=params,
            **kwargs)

    def get_if_attachment_compressed(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Is this attachment compressed: "0" means uncompressed, "1" compressed

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
            "0" means uncompressed, "1" compressed
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/is_compressed',
            params=params,
            **kwargs)

    def get_attachments_name_md5(
            self, resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        HERE

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).
        name : Attachment name.
        params : GET HTTP request's params.

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/md5',
            params=params,
            **kwargs)

    def get_resource_type_identifier_attachments_name_size(
            self,
            resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/size',
            params=params,
            **kwargs)

    def post_resource_type_identifier_attachments_name_uncompress(
            self,
            resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/uncompress',
            data=data,
            json=json,
            **kwargs)

    def post_resource_type_identifier_attachments_name_verify_md5(
            self,
            resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method

        Check that there is no corruption on the disk (HTTP status == 200 iff. no error)

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/attachments/{name}/verify_md5',
            data=data,
            json=json,
            **kwargs)

    def get_resource_type_identifier_metadata(
            self,
            resource_type: str,
            identifier: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        "?expand" argument

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata',
            params=params,
            **kwargs)

    def get_resource_type_identifier_metadata_name(
            self,
            resource_type: str,
            identifier: str,
            name: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            params=params,
            **kwargs)

    def delete_resource_type_identifier_metadata_name(
            self, resource_type: str, identifier: str, name: str,
            **kwargs) -> requests.Response:
        """Delete method

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            **kwargs)

    def put_resource_type_identifier_metadata_name(
            self,
            resource_type: str,
            identifier: str,
            name: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Put method

        Parameters
        ----------
        resource_type : Resource type ('Patient', 'Study', 'Series' or 'Instance').
        identifier : Object identifier (patient, study, series, instance).

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/{resource_type}/{identifier}/metadata/{name}',
            data=data,
            json=json,
            **kwargs)

    def get_changes(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        "last", "limit" and "since" arguments
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/changes', params=params, **kwargs)

    def delete_changes(self, **kwargs) -> requests.Response:
        """Delete method
        "last", "limit" and "since" arguments
        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/changes', **kwargs)

    def get_exports(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        "last", "limit" and "since" arguments
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/exports', params=params, **kwargs)

    def delete_exports(self, **kwargs) -> requests.Response:
        """Delete method
        "last", "limit" and "since" arguments
        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/exports', **kwargs)

    def get_instances(self, params: Dict = None,
                      **kwargs) -> requests.Response:
        """Get method
        GET: "last" and "limit" arguments; POST = Add the new DICOM file given in the POST body
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances', params=params, **kwargs)

    def post_instances(self, data: Dict = None, json=None,
                       **kwargs) -> requests.Response:
        """Post method
        GET: "last" and "limit" arguments; POST = Add the new DICOM file given in the POST body
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances', data=data, json=json, **kwargs)

    def get_instances_identifier(self,
                                 identifier: str,
                                 params: Dict = None,
                                 **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}',
            params=params,
            **kwargs)

    def delete_instances_identifier(self, identifier: str,
                                    **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/instances/{identifier}', **kwargs)

    def post_instances_identifier_anonymize(self,
                                            identifier: str,
                                            data: Dict = None,
                                            json=None,
                                            **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_instances_identifier_content(self,
                                         identifier: str,
                                         params: Dict = None,
                                         **kwargs) -> requests.Response:
        """Get method
        List the first-level DICOM tags
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/content/',
            params=params,
            **kwargs)

    def get_instances_identifier_content_group_element(
            self,
            identifier: str,
            group_element: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Raw access to the value of DICOM tags (comprising the padding character)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/content/{group_element}',
            params=params,
            **kwargs)

    def get_instances_identifier_content_group_element_index(
            self,
            identifier: str,
            group_element: str,
            index: str,
            params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Raw access to the content of DICOM sequences
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/content/{group_element}/{index}/...',
            params=params,
            **kwargs)

    def post_instances_identifier_export(self,
                                         identifier: str,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        Write the DICOM file to the filesystem where Orthanc is running
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{identifier}/export',
            data=data,
            json=json,
            **kwargs)

    def get_instances_identifier_file(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/file',
            params=params,
            **kwargs)

    def get_instances_identifier_frames(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_image_int16(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [-32768;32767] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/image_int16',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_image_uint16(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [0;65535] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/image_uint16',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_image_uint8(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [0;255] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/image_uint8',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_matlab(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        a = eval(urlread('http://localhost:8042/instances/.../frames/0/matlab'))
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/matlab',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_preview(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Rescaled image (so that all the range [0;255] is used)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/preview',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_raw(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Access to the raw content of one frame (bypass image decoding)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/raw',
            params=params,
            **kwargs)

    def get_instances_identifier_frames_frameNumber_raw_gz(
            self, identifier: str, frameNumber: str, params: Dict = None,
            **kwargs) -> requests.Response:
        """Get method
        Access to the raw content of one frame, compressed using gzip
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/frames/{frameNumber}/raw.gz',
            params=params,
            **kwargs)

    def get_instances_identifier_header(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Get the meta information (header) of the DICOM file, "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/header',
            params=params,
            **kwargs)

    def get_instances_identifier_image_int16(self,
                                             identifier: str,
                                             params: Dict = None,
                                             **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [-32768;32767] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/image_int16',
            params=params,
            **kwargs)

    def get_instances_identifier_image_uint16(self,
                                              identifier: str,
                                              params: Dict = None,
                                              **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [0;65535] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/image_uint16',
            params=params,
            **kwargs)

    def get_instances_identifier_image_uint8(self,
                                             identifier: str,
                                             params: Dict = None,
                                             **kwargs) -> requests.Response:
        """Get method
        Truncated decoded image to the [0;255] range (Accepts image/png, image/jpg, image/x-portable-arbitrarymap)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/image_uint8',
            params=params,
            **kwargs)

    def get_instances_identifier_matlab(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        a = eval(urlread('http://localhost:8042/instances/.../matlab'))
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/matlab',
            params=params,
            **kwargs)

    def post_instances_identifier_modify(self,
                                         identifier: str,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_instances_identifier_module(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/module',
            params=params,
            **kwargs)

    def get_instances_identifier_patient(self,
                                         identifier: str,
                                         params: Dict = None,
                                         **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent patient of this instance
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/patient',
            params=params,
            **kwargs)

    def get_instances_identifier_pdf(self,
                                     identifier: str,
                                     params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        Return the encapsulated PDF inside the DICOM file, if any
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/pdf',
            params=params,
            **kwargs)

    def get_instances_identifier_preview(self,
                                         identifier: str,
                                         params: Dict = None,
                                         **kwargs) -> requests.Response:
        """Get method
        Rescaled image (so that all the range [0;255] is used)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/preview',
            params=params,
            **kwargs)

    def post_instances_identifier_reconstruct(self,
                                              identifier: str,
                                              data: Dict = None,
                                              json=None,
                                              **kwargs) -> requests.Response:
        """Post method
        Force reconstruction of the main DICOM tags, JSON summary and metadata
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/instances/{identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_instances_identifier_series(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent series of this instance
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/series',
            params=params,
            **kwargs)

    def get_instances_identifier_simplified_tags(self,
                                                 identifier: str,
                                                 params: Dict = None,
                                                 **kwargs
                                                 ) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/simplified_tags',
            params=params,
            **kwargs)

    def get_instances_identifier_statistics(self,
                                            identifier: str,
                                            params: Dict = None,
                                            **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/statistics',
            params=params,
            **kwargs)

    def get_instances_identifier_study(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent study of this instance
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/study',
            params=params,
            **kwargs)

    def get_instances_identifier_tags(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output (same as "simplified-tags"), "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/instances/{identifier}/tags',
            params=params,
            **kwargs)

    def get_jobs(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        List the jobs, "?expand" to get more information
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs', params=params, **kwargs)

    def get_jobs_identifier(self,
                            identifier: str,
                            params: Dict = None,
                            **kwargs) -> requests.Response:
        """Get method
        Get information about one job
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs/{identifier}', params=params, **kwargs)

    def post_jobs_identifier_cancel(self,
                                    identifier: str,
                                    data: Dict = None,
                                    json=None,
                                    **kwargs) -> requests.Response:
        """Post method
        Cancel the job, tag it as failed
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{identifier}/cancel',
            data=data,
            json=json,
            **kwargs)

    def post_jobs_identifier_pause(self,
                                   identifier: str,
                                   data: Dict = None,
                                   json=None,
                                   **kwargs) -> requests.Response:
        """Post method
        Pause the job
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{identifier}/pause',
            data=data,
            json=json,
            **kwargs)

    def post_jobs_identifier_resubmit(self,
                                      identifier: str,
                                      data: Dict = None,
                                      json=None,
                                      **kwargs) -> requests.Response:
        """Post method
        Resumbit a failed job
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{identifier}/resubmit',
            data=data,
            json=json,
            **kwargs)

    def post_jobs_identifier_resume(self,
                                    identifier: str,
                                    data: Dict = None,
                                    json=None,
                                    **kwargs) -> requests.Response:
        """Post method
        Resume a paused job
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/jobs/{identifier}/resume',
            data=data,
            json=json,
            **kwargs)

    def get_jobs_identifier_key(self,
                                identifier: str,
                                key: str,
                                params: Dict = None,
                                **kwargs) -> requests.Response:
        """Get method
        Retrieve outputs generated by the job (only valid after job is successful)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/jobs/{identifier}/{key}',
            params=params,
            **kwargs)

    def get_modalities(self, params: Dict = None,
                       **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/modalities', params=params, **kwargs)

    def get_modalities_dicom(self, dicom: str, params: Dict = None,
                             **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/modalities/{dicom}', params=params, **kwargs)

    def delete_modalities_dicom(self, dicom: str,
                                **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/modalities/{dicom}',
                                   **kwargs)

    def put_modalities_dicom(self,
                             dicom: str,
                             data: Dict = None,
                             json=None,
                             **kwargs) -> requests.Response:
        """Put method

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/modalities/{dicom}',
            data=data,
            json=json,
            **kwargs)

    def post_modalities_dicom_echo(self,
                                   dicom: str,
                                   data: Dict = None,
                                   json=None,
                                   **kwargs) -> requests.Response:
        """Post method
        C-Echo SCU
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{dicom}/echo',
            data=data,
            json=json,
            **kwargs)

    def post_modalities_dicom_move(self,
                                   dicom: str,
                                   data: Dict = None,
                                   json=None,
                                   **kwargs) -> requests.Response:
        """Post method
        DICOM C-Move SCU (Retrieve)
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{dicom}/move',
            data=data,
            json=json,
            **kwargs)

    def post_modalities_dicom_query(self,
                                    dicom: str,
                                    data: Dict = None,
                                    json=None,
                                    **kwargs) -> requests.Response:
        """Post method
        DICOM C-Find SCU (Query), with subsequent possibility for Retrieve
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{dicom}/query',
            data=data,
            json=json,
            **kwargs)

    def post_modalities_dicom_store(self,
                                    dicom: str,
                                    data: Dict = None,
                                    json=None,
                                    **kwargs) -> requests.Response:
        """Post method
        POST body = UUID series, UUID instance, or raw DICOM file
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/modalities/{dicom}/store',
            data=data,
            json=json,
            **kwargs)

    def get_patients(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        "since" and "limit" arguments + "expand" argument to retrieve the content of the patients
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients', params=params, **kwargs)

    def get_patients_identifier(self,
                                identifier: str,
                                params: Dict = None,
                                **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}',
            params=params,
            **kwargs)

    def delete_patients_identifier(self, identifier: str,
                                   **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(
            f'{self._orthanc_url}/patients/{identifier}', **kwargs)

    def post_patients_identifier_anonymize(self,
                                           identifier: str,
                                           data: Dict = None,
                                           json=None,
                                           **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_archive(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Create ZIP
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/archive',
            params=params,
            **kwargs)

    def post_patients_identifier_archive(self,
                                         identifier: str,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        Create ZIP
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_instances(self,
                                          identifier: str,
                                          params: Dict = None,
                                          **kwargs) -> requests.Response:
        """Get method
        Retrieve all the instances of this patient in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/instances',
            params=params,
            **kwargs)

    def get_patients_identifier_instances_tags(self,
                                               identifier: str,
                                               params: Dict = None,
                                               **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_patients_identifier_media(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/media',
            params=params,
            **kwargs)

    def post_patients_identifier_media(self,
                                       identifier: str,
                                       data: Dict = None,
                                       json=None,
                                       **kwargs) -> requests.Response:
        """Post method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_patients_identifier_modify(self,
                                        identifier: str,
                                        data: Dict = None,
                                        json=None,
                                        **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_module(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/module',
            params=params,
            **kwargs)

    def get_patients_identifier_protected(self,
                                          identifier: str,
                                          params: Dict = None,
                                          **kwargs) -> requests.Response:
        """Get method
        Protection against recycling: "0" means unprotected, "1" protected
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/protected',
            params=params,
            **kwargs)

    def put_patients_identifier_protected(self,
                                          identifier: str,
                                          data: Dict = None,
                                          json=None,
                                          **kwargs) -> requests.Response:
        """Put method
        Protection against recycling: "0" means unprotected, "1" protected
        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/patients/{identifier}/protected',
            data=data,
            json=json,
            **kwargs)

    def post_patients_identifier_reconstruct(self,
                                             identifier: str,
                                             data: Dict = None,
                                             json=None,
                                             **kwargs) -> requests.Response:
        """Post method
        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/patients/{identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_patients_identifier_series(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        Retrieve all the series of this patient in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/series',
            params=params,
            **kwargs)

    def get_patients_identifier_shared_tags(self,
                                            identifier: str,
                                            params: Dict = None,
                                            **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/shared_tags',
            params=params,
            **kwargs)

    def get_patients_identifier_statistics(self,
                                           identifier: str,
                                           params: Dict = None,
                                           **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/statistics',
            params=params,
            **kwargs)

    def get_patients_identifier_studies(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Retrieve all the studies of this patient in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/patients/{identifier}/studies',
            params=params,
            **kwargs)

    def get_peers(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/peers', params=params, **kwargs)

    def get_peers_peer(self, peer: str, params: Dict = None,
                       **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/peers/{peer}', params=params, **kwargs)

    def delete_peers_peer(self, peer: str, **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/peers/{peer}',
                                   **kwargs)

    def put_peers_peer(self, peer: str, data: Dict = None, json=None,
                       **kwargs) -> requests.Response:
        """Put method

        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/peers/{peer}',
            data=data,
            json=json,
            **kwargs)

    def post_peers_peer_store(self,
                              peer: str,
                              data: Dict = None,
                              json=None,
                              **kwargs) -> requests.Response:
        """Post method
        POST body = UUID series, UUID instance, or raw DICOM file
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/peers/{peer}/store',
            data=data,
            json=json,
            **kwargs)

    def get_plugins(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        Get the list of all the registered plugins
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins', params=params, **kwargs)

    def get_plugins_identifier(self,
                               identifier: str,
                               params: Dict = None,
                               **kwargs) -> requests.Response:
        """Get method
        Get information about some plugin
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/{identifier}',
            params=params,
            **kwargs)

    def get_plugins_explorer_js(self, params: Dict = None,
                                **kwargs) -> requests.Response:
        """Get method
        Get the JavaScript code that is injected by plugins into Orthanc Explorer
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/plugins/explorer.js',
            params=params,
            **kwargs)

    def get_queries(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries', params=params, **kwargs)

    def get_queries_identifier(self,
                               identifier: str,
                               params: Dict = None,
                               **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}',
            params=params,
            **kwargs)

    def delete_queries_identifier(self, identifier: str,
                                  **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/queries/{identifier}',
                                   **kwargs)

    def get_queries_identifier_answers(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        List all the answers for this C-Find SCU request ("?expand" to show content, "&simplify" to simplify output)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}/answers',
            params=params,
            **kwargs)

    def get_queries_identifier_answers_index_content(self,
                                                     identifier: str,
                                                     index: str,
                                                     params: Dict = None,
                                                     **kwargs
                                                     ) -> requests.Response:
        """Get method
        Access 1 answer of C-Find SCU; "?simplify" argument to simplify output
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}/answers/{index}/content',
            params=params,
            **kwargs)

    def post_queries_identifier_answers_index_retrieve(
            self,
            identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method
        C-Move SCU: Send this resource to another modality whose AET is in the body
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{identifier}/answers/{index}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_instances(
            self,
            identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method
        Launch another C-Find SCU to find the child DICOM instances of the given answer (might not work with all PACS)
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{identifier}/answers/{index}/query_instances',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_series(
            self,
            identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method
        Launch another C-Find SCU to find the child series of the given answer
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{identifier}/answers/{index}/query_series',
            data=data,
            json=json,
            **kwargs)

    def post_queries_identifier_answers_index_query_studies(
            self,
            identifier: str,
            index: str,
            data: Dict = None,
            json=None,
            **kwargs) -> requests.Response:
        """Post method
        Launch another C-Find SCU to find the child patient of the given answer
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{identifier}/answers/{index}/query_studies',
            data=data,
            json=json,
            **kwargs)

    def get_queries_identifier_level(self,
                                     identifier: str,
                                     params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        Get the query retrieve level for this C-Find SCU request
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}/level',
            params=params,
            **kwargs)

    def get_queries_identifier_modality(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Get the modality to which this C-Find SCU request was issued (cf. /modalities)
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}/modality',
            params=params,
            **kwargs)

    def get_queries_identifier_query(self,
                                     identifier: str,
                                     params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        Access the C-Find SCU query; "?simplify" argument to simplify output
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/queries/{identifier}/query',
            params=params,
            **kwargs)

    def post_queries_identifier_retrieve(self,
                                         identifier: str,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        C-Move SCU: Send all the results to another modality whose AET is in the body
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/queries/{identifier}/retrieve',
            data=data,
            json=json,
            **kwargs)

    def get_series(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        "since" and "limit" arguments + "expand" argument to retrieve the content of the series
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series', params=params, **kwargs)

    def get_series_identifier(self,
                              identifier: str,
                              params: Dict = None,
                              **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}',
            params=params,
            **kwargs)

    def delete_series_identifier(self, identifier: str,
                                 **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/series/{identifier}',
                                   **kwargs)

    def post_series_identifier_anonymize(self,
                                         identifier: str,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_archive(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/archive',
            params=params,
            **kwargs)

    def post_series_identifier_archive(self,
                                       identifier: str,
                                       data: Dict = None,
                                       json=None,
                                       **kwargs) -> requests.Response:
        """Post method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_instances(self,
                                        identifier: str,
                                        params: Dict = None,
                                        **kwargs) -> requests.Response:
        """Get method
        Retrieve all the instances of this series in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/instances',
            params=params,
            **kwargs)

    def get_series_identifier_instances_tags(self,
                                             identifier: str,
                                             params: Dict = None,
                                             **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_series_identifier_media(self,
                                    identifier: str,
                                    params: Dict = None,
                                    **kwargs) -> requests.Response:
        """Get method
        Create archives for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/media',
            params=params,
            **kwargs)

    def post_series_identifier_media(self,
                                     identifier: str,
                                     data: Dict = None,
                                     json=None,
                                     **kwargs) -> requests.Response:
        """Post method
        Create archives for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_series_identifier_modify(self,
                                      identifier: str,
                                      data: Dict = None,
                                      json=None,
                                      **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_module(self,
                                     identifier: str,
                                     params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/module',
            params=params,
            **kwargs)

    def get_series_identifier_ordered_slices(self,
                                             identifier: str,
                                             params: Dict = None,
                                             **kwargs) -> requests.Response:
        """Get method
        Order the slices of a 2D+t, 3D or 3D+t image
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/ordered_slices',
            params=params,
            **kwargs)

    def get_series_identifier_patient(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent patient of this series
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/patient',
            params=params,
            **kwargs)

    def post_series_identifier_reconstruct(self,
                                           identifier: str,
                                           data: Dict = None,
                                           json=None,
                                           **kwargs) -> requests.Response:
        """Post method
        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/series/{identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_series_identifier_shared_tags(self,
                                          identifier: str,
                                          params: Dict = None,
                                          **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/shared_tags',
            params=params,
            **kwargs)

    def get_series_identifier_statistics(self,
                                         identifier: str,
                                         params: Dict = None,
                                         **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/statistics',
            params=params,
            **kwargs)

    def get_series_identifier_study(self,
                                    identifier: str,
                                    params: Dict = None,
                                    **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent study of this series
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/series/{identifier}/study',
            params=params,
            **kwargs)

    def get_statistics(self, params: Dict = None,
                       **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/statistics', params=params, **kwargs)

    def get_studies(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method
        "since" and "limit" arguments + "expand" argument to retrieve the content of the studies
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies', params=params, **kwargs)

    def get_studies_identifier(self,
                               identifier: str,
                               params: Dict = None,
                               **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}',
            params=params,
            **kwargs)

    def delete_studies_identifier(self, identifier: str,
                                  **kwargs) -> requests.Response:
        """Delete method

        Returns
        -------
        requests.Response
        """
        return self.delete_request(f'{self._orthanc_url}/studies/{identifier}',
                                   **kwargs)

    def post_studies_identifier_anonymize(self,
                                          identifier: str,
                                          data: Dict = None,
                                          json=None,
                                          **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/anonymize',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_archive(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        Create ZIP
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/archive',
            params=params,
            **kwargs)

    def post_studies_identifier_archive(self,
                                        identifier: str,
                                        data: Dict = None,
                                        json=None,
                                        **kwargs) -> requests.Response:
        """Post method
        Create ZIP
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/archive',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_instances(self,
                                         identifier: str,
                                         params: Dict = None,
                                         **kwargs) -> requests.Response:
        """Get method
        Retrieve all the instances of this patient in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/instances',
            params=params,
            **kwargs)

    def get_studies_identifier_instances_tags(self,
                                              identifier: str,
                                              params: Dict = None,
                                              **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/instances_tags',
            params=params,
            **kwargs)

    def get_studies_identifier_media(self,
                                     identifier: str,
                                     params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/media',
            params=params,
            **kwargs)

    def post_studies_identifier_media(self,
                                      identifier: str,
                                      data: Dict = None,
                                      json=None,
                                      **kwargs) -> requests.Response:
        """Post method
        Create a ZIP archive for media storage with DICOMDIR
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/media',
            data=data,
            json=json,
            **kwargs)

    def post_studies_identifier_merge(self,
                                      identifier: str,
                                      data: Dict = None,
                                      json=None,
                                      **kwargs) -> requests.Response:
        """Post method
        Merge a study, i.e. move series from another study into this study
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/merge',
            data=data,
            json=json,
            **kwargs)

    def post_studies_identifier_modify(self,
                                       identifier: str,
                                       data: Dict = None,
                                       json=None,
                                       **kwargs) -> requests.Response:
        """Post method
        http://book.orthanc-server.com/users/anonymization.html
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/modify',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_module(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/module',
            params=params,
            **kwargs)

    def get_studies_identifier_module_patient(self,
                                              identifier: str,
                                              params: Dict = None,
                                              **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/module_patient',
            params=params,
            **kwargs)

    def get_studies_identifier_patient(self,
                                       identifier: str,
                                       params: Dict = None,
                                       **kwargs) -> requests.Response:
        """Get method
        Retrieve the parent patient of this study
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/patient',
            params=params,
            **kwargs)

    def post_studies_identifier_reconstruct(self,
                                            identifier: str,
                                            data: Dict = None,
                                            json=None,
                                            **kwargs) -> requests.Response:
        """Post method
        Force reconstruction of the main DICOM tags, JSON summary and metadata of child instances
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_series(self,
                                      identifier: str,
                                      params: Dict = None,
                                      **kwargs) -> requests.Response:
        """Get method
        Retrieve all the series of this study in a single REST call
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/series',
            params=params,
            **kwargs)

    def get_studies_identifier_shared_tags(self,
                                           identifier: str,
                                           params: Dict = None,
                                           **kwargs) -> requests.Response:
        """Get method
        "?simplify" argument to simplify output, "?short"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/shared_tags',
            params=params,
            **kwargs)

    def post_studies_identifier_split(self,
                                      identifier: str,
                                      data: Dict = None,
                                      json=None,
                                      **kwargs) -> requests.Response:
        """Post method
        Split a study, i.e. create a new study from a subset of its child series
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/studies/{identifier}/split',
            data=data,
            json=json,
            **kwargs)

    def get_studies_identifier_statistics(self,
                                          identifier: str,
                                          params: Dict = None,
                                          **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/studies/{identifier}/statistics',
            params=params,
            **kwargs)

    def get_system(self, params: Dict = None, **kwargs) -> requests.Response:
        """Get method

        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/system', params=params, **kwargs)

    def post_tools_create_archive(self, data: Dict = None, json=None,
                                  **kwargs) -> requests.Response:
        """Post method
        Create a ZIP from a set of unrelated DICOM resources
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_archive',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_dicom(self, data: Dict = None, json=None,
                                **kwargs) -> requests.Response:
        """Post method
        Create and store a new DICOM instance, possibly with an image or a PDF payload
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_dicom',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_media(self, data: Dict = None, json=None,
                                **kwargs) -> requests.Response:
        """Post method
        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media',
            data=data,
            json=json,
            **kwargs)

    def post_tools_create_media_extended(self,
                                         data: Dict = None,
                                         json=None,
                                         **kwargs) -> requests.Response:
        """Post method
        Create a ZIP-with-DICOMDIR from a set of unrelated DICOM resources, including type-3 tags
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/create_media_extended',
            data=data,
            json=json,
            **kwargs)

    def get_tools_default_encoding(self, params: Dict = None,
                                   **kwargs) -> requests.Response:
        """Get method
        Get the default encoding used by Orthanc, or temporarily change it until the next restart
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/default_encoding',
            params=params,
            **kwargs)

    def put_tools_default_encoding(self,
                                   data: Dict = None,
                                   json=None,
                                   **kwargs) -> requests.Response:
        """Put method
        Get the default encoding used by Orthanc, or temporarily change it until the next restart
        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/default_encoding',
            data=data,
            json=json,
            **kwargs)

    def get_tools_dicom_conformance(self, params: Dict = None,
                                    **kwargs) -> requests.Response:
        """Get method
        DICOM conformance statement of this version of Orthanc
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/dicom_conformance',
            params=params,
            **kwargs)

    def post_tools_execute_script(self, data: Dict = None, json=None,
                                  **kwargs) -> requests.Response:
        """Post method
        Execute the Lua script in the POST body
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/execute_script',
            data=data,
            json=json,
            **kwargs)

    def post_tools_find(self, data: Dict = None, json=None,
                        **kwargs) -> requests.Response:
        """Post method
        Runs a C-Find call from the REST API
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/find', data=data, json=json, **kwargs)

    def get_tools_generate_uid(self, params: Dict = None,
                               **kwargs) -> requests.Response:
        """Get method
        Generate DICOM UID. The "level" GET argument must be "patient", "study", "series" or "instance"
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/generate_uid', params=params, **kwargs)

    def post_tools_invalidate_tags(self,
                                   data: Dict = None,
                                   json=None,
                                   **kwargs) -> requests.Response:
        """Post method
        Invalidate the JSON summary of all the DICOM files (useful if new private tags are registered)
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/invalidate_tags',
            data=data,
            json=json,
            **kwargs)

    def post_tools_lookup(self, data: Dict = None, json=None,
                          **kwargs) -> requests.Response:
        """Post method
        Map DICOM UIDs to Orthanc identifiers
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/lookup',
            data=data,
            json=json,
            **kwargs)

    def get_tools_metrics(self, params: Dict = None,
                          **kwargs) -> requests.Response:
        """Get method
        See whether the collection of metrics is enabled, and enable/disable this collection
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics', params=params, **kwargs)

    def put_tools_metrics(self, data: Dict = None, json=None,
                          **kwargs) -> requests.Response:
        """Put method
        See whether the collection of metrics is enabled, and enable/disable this collection
        Returns
        -------
        requests.Response
        """
        return self.put_request(
            f'{self._orthanc_url}/tools/metrics',
            data=data,
            json=json,
            **kwargs)

    def get_tools_metrics_prometheus(self, params: Dict = None,
                                     **kwargs) -> requests.Response:
        """Get method
        Retrieve the metrics in the Prometheus text-based exposition format
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/metrics_prometheus',
            params=params,
            **kwargs)

    def get_tools_now(self, params: Dict = None,
                      **kwargs) -> requests.Response:
        """Get method
        Returns the current *universal* datetime (UTC) in the ISO 8601 format
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now', params=params, **kwargs)

    def get_tools_now_local(self, params: Dict = None,
                            **kwargs) -> requests.Response:
        """Get method
        Returns the current *local* datetime in the ISO 8601 format
        Returns
        -------
        requests.Response
        """
        return self.get_request(
            f'{self._orthanc_url}/tools/now_local', params=params, **kwargs)

    def post_tools_reconstruct(self, data: Dict = None, json=None,
                               **kwargs) -> requests.Response:
        """Post method
        Reconstructs the main DICOM tags, the JSON summary and metadata of all the instances stored in Orthanc. Slow operation!
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reconstruct',
            data=data,
            json=json,
            **kwargs)

    def post_tools_reset(self, data: Dict = None, json=None,
                         **kwargs) -> requests.Response:
        """Post method
        Hot restart of Orthanc, the configuration file will be read again
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/reset', data=data, json=json, **kwargs)

    def post_tools_shutdown(self, data: Dict = None, json=None,
                            **kwargs) -> requests.Response:
        """Post method
        Stop Orthanc
        Returns
        -------
        requests.Response
        """
        return self.post_request(
            f'{self._orthanc_url}/tools/shutdown',
            data=data,
            json=json,
            **kwargs)
