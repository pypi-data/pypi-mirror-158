# stdlib
from typing import Dict

# third party
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

# first party
from dbtc.client.base import _Client
from dbtc.client.metadata.schema import Query


class _MetadataClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    _header_property = 'service_token'
    _default_domain = 'metadata.cloud.getdbt.com'
    _path = '/graphql'

    @property
    def _endpoint(self) -> HTTPEndpoint:
        return HTTPEndpoint(self.full_url(), self.headers)

    def _make_request(self, obj: str, arguments: Dict = None) -> Dict:
        op = Operation(Query)
        getattr(op, obj)(  # noqa: F841
            **{k: v for k, v in arguments.items() if v is not None}  # type: ignore
        ).__fields__()
        data = self._endpoint(op)
        return data

    def get_exposure(self, job_id: int, name: str, *, run_id: int = None) -> Dict:
        """
        The exposure object allows you to query information about a particular
            exposure. You can learn more about exposures [here](
            https://docs.getdbt.com/docs/building-a-dbt-project/exposures).

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "exposure",
            {"job_id": job_id, "name": name, "run_id": run_id},
        )

    def get_exposures(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The exposures object allows you to query information about all exposures in a
            given job. You can learn more about exposures [here](
            https://docs.getdbt.com/docs/building-a-dbt-project/exposures).

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "exposures",
            {"job_id": job_id, "run_id": run_id},
        )

    def get_macro(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The macro object allows you to query information about a particular macro in a
        given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "macro",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_macros(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The macros object allows you to query information about all macros in a
            given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request("macros", {"job_id": job_id, "run_id": run_id})

    def get_metric(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The metric object allows you to query information about [metrics](
            https://docs.getdbt.com/docs/building-a-dbt-project/metrics).

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "metric",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_metrics(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The metrics object allows you to query information about [metrics](
            https://docs.getdbt.com/docs/building-a-dbt-project/metrics).

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request("metrics", {"job_id": job_id, "run_id": run_id})

    def get_model(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The model object allows you to query information about a particular model in a
        given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "model",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_models(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
    ) -> Dict:
        """
        The models object allows you to query information about all models in a given
            job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
            database (str, optional): The database where this table/view lives
            schema (str, optional): The schema where this table/view lives
            identifier (str, optional): The identifier of this table/view
        """
        return self._make_request(
            "models",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
        )

    def get_seed(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The seed object allows you to query information about a particular seed in a
            given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "seed",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_seeds(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The seeds object allows you to query information about a all seeds in a given
            job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "seeds",
            {"job_id": job_id, "run_id": run_id},
        )

    def get_snapshot(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The snapshot object allows you to query information about a particular
            snapshot.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "snapshot",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_snapshots(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The snapshots object allows you to query information about all snapshots in a
            given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "snapshots",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
        )

    def get_source(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The source object allows you to query information about a particular source in
            a given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "source",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_sources(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
    ) -> Dict:
        """
        The snapshots object allows you to query information about all snapshots in a
            given job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
            database (str, optional): The database where this table/view lives
            schema (str, optional): The schema where this table/view lives
            identifier (str, optional): The identifier of this table/view
        """
        return self._make_request(
            "sources",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
        )

    def get_test(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The test object allows you to query information about a particular test.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "test", {"job_id": job_id, "unique_id": unique_id, "run_id": run_id}
        )

    def get_tests(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        """
        The tests object allows you to query information about all tests in a given
            job.

        Note:
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
        """
        return self._make_request(
            "tests",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
        )
