# coding: utf-8
# author: gabriel couture
from typing import Dict

from pyorthanc import Orthanc


class RemoteModality:
    """Wrapper around Orthanc API when dealing with a (remote) modality.
    """

    def __init__(self, orthanc: Orthanc, modality: str) -> None:
        """Constructor

        Parameters
        ----------
        orthanc
            Orthanc object.
        modality
            Remote modality.
        """
        self.orthanc: Orthanc = orthanc
        self.modality: str = modality

    def echo(self) -> bool:
        """C-Echo to remote modality

        Returns
        -------
        bool
            True if C-Echo succeeded.
        """
        return self.orthanc.echo_to_modality(self.modality)

    def query(self, data: Dict) -> Dict:
        """C-Find (Querying with data)

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        requests.Response

        Examples
        -------
        >>> data = {'Level': 'Study',
        ...         'Query': {
        ...             'PatientID':'03HD*',
        ...             'StudyDescription':'*Chest*',
        ...             'PatientName':''
        ...         }
        ... }

        >>> remote_modality = RemoteModality(
        ...     orthanc=Orthanc('http://localhost:8042'),
        ...     modality='sample'
        ... )

        >>> remote_modality.query(data)
        """
        return self.orthanc.query_on_modality(self.modality, data=data)

    def retrieve(self, data: Dict) -> bool:
        """Retrieve (C-Move) to local modality

        Parameters
        ----------
        data
            Dictionary to send in the body of request.

        Returns
        -------
        bool
            True if the C-Move operation was sent without problem, else False.
        """
        return self.orthanc.move_from_modality(self.modality, data=data)

    def move(self, query_identifier: str, cmove_data: Dict) -> bool:
        """C-Move query results to another modality

        C-Move SCU: Send all the results to another modality whose AET is in the body

        Parameters
        ----------
        query_identifier
            Query identifier.
        cmove_data
            Ex. {'TargetAET': 'modality_name', "Synchronous": False}

        Returns
        -------
        bool
            True if the C-Move operation was sent without problem, else False.

        Examples
        --------
        >>> remote_modality = RemoteModality(Orthanc('http://localhost:8042'), 'modality')
        >>> query_id = remote_modality.query(
        ...     data={'Level': 'Study',
        ...           'Query': {'QueryRetrieveLevel': 'Study',
        ...                     'Modality':'SR'}}).json()

        >>> remote_modality.move(
        ...     query_identifier=query_id['ID'],
        ...     cmove_data={'TargetAET': 'modality'}
        ... )

        """
        return self.orthanc.move_query_results_to_given_modality(
            query_identifier,
            data=cmove_data
        )

    def get_query_answer_number_of_results(self, query_identifier: str,
            params: Dict = None,
            **kwargs) -> list:
        """Get all content of specified answer of C-Find

            Parameters
            ----------
            query_identifier
                Query identifier.
            params
                GET HTTP request's params.

            Returns
            -------
            list
                A list of dictionaries corresponding to each answer of the C-find. Empty if no answer found.
        """
        return self.orthanc.get_query_answer_number_of_results(query_identifier, params)

    def get_content_of_specified_query_answer(
            self, query_identifier: str,
            index: str,
            params: Dict = None,
            **kwargs):
        """Get content of specified answer of C-Find

        Parameters
        ----------
        query_identifier
            Query identifier.
        index
            Index of wanted answer.
        params
            GET HTTP request's params.

        Returns
        -------
        Any
            Specified answer of C-Find SCU operation.
        """
        return self.orthanc.get_content_of_specified_query_answer(query_identifier, index, params)
