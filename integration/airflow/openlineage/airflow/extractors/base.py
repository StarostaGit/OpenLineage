# Copyright 2018-2022 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0

import attr
from abc import ABC, abstractmethod

from openlineage.client.run import Dataset
from typing import List, Dict, Optional
from openlineage.client.facet import BaseFacet
from openlineage.airflow.utils import LoggingMixin


@attr.s
class TaskMetadata:
    name: str = attr.ib()  # deprecated
    inputs: List[Dataset] = attr.ib(factory=list)
    outputs: List[Dataset] = attr.ib(factory=list)
    run_facets: Dict[str, BaseFacet] = attr.ib(factory=dict)
    job_facets: Dict[str, BaseFacet] = attr.ib(factory=dict)


class BaseExtractor(ABC, LoggingMixin):
    def __init__(self, operator):
        super().__init__()
        self.operator = operator
        self.patch()

    def patch(self):
        # Extractor should register extension methods or patches to operator here
        pass

    @classmethod
    def get_operator_classnames(cls) -> List[str]:
        """
        Implement this method returning list of operators that extractor works for.
        Particularly, in Airflow 2 some operators are deprecated and simply subclass the new
        implementation, for example BigQueryOperator:
        https://github.com/apache/airflow/blob/main/airflow/contrib/operators/bigquery_operator.py
        The BigQueryExtractor needs to work with both of them.
        :return:
        """
        raise NotImplementedError()

    def validate(self):
        assert (self.operator.__class__.__name__ in self.get_operator_classnames())

    @abstractmethod
    def extract(self) -> Optional[TaskMetadata]:
        pass

    def extract_on_complete(self, task_instance) -> Optional[TaskMetadata]:
        return self.extract()
