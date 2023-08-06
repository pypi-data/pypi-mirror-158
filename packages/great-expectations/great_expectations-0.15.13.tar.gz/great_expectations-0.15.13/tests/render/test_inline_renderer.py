from typing import List

import pytest

from great_expectations.core.batch import BatchRequest
from great_expectations.core.expectation_configuration import ExpectationConfiguration
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.core.expectation_validation_result import (
    ExpectationValidationResult,
)
from great_expectations.data_context import DataContext
from great_expectations.render.renderer.inline_renderer import InlineRenderer
from great_expectations.render.types import RenderedAtomicContent
from great_expectations.validator.validator import Validator


@pytest.mark.parametrize(
    "expectation_configuration,expected_serialized_expectation_configuration_rendered_atomic_content,expected_serialized_expectation_validation_result_rendered_atomic_content",
    [
        pytest.param(
            ExpectationConfiguration(
                expectation_type="expect_table_row_count_to_equal",
                kwargs={"value": 3},
            ),
            [
                {
                    "value_type": "StringValueType",
                    "name": "atomic.prescriptive.summary",
                    "value": {
                        "header_row": None,
                        "kwargs": None,
                        "graph": None,
                        "header": None,
                        "template": "Must have exactly $value rows.",
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "params": {
                            "value": {"schema": {"type": "number"}, "value": 3},
                            "row_condition": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                            "condition_parser": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                        },
                    },
                }
            ],
            [
                {
                    "name": "atomic.diagnostic.observed_value",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": None,
                        "kwargs": None,
                        "params": {},
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "template": "3",
                    },
                    "value_type": "StringValueType",
                }
            ],
            id="expect_table_row_count_to_equal",
        ),
        pytest.param(
            ExpectationConfiguration(
                expectation_type="expect_column_min_to_be_between",
                kwargs={"column": "event_type", "min_value": 3, "max_value": 20},
            ),
            [
                {
                    "name": "atomic.prescriptive.summary",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": None,
                        "kwargs": None,
                        "params": {
                            "column": {
                                "schema": {"type": "string"},
                                "value": "event_type",
                            },
                            "condition_parser": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                            "max_value": {"schema": {"type": "number"}, "value": 20},
                            "min_value": {"schema": {"type": "number"}, "value": 3},
                            "parse_strings_as_datetimes": {
                                "schema": {"type": "boolean"},
                                "value": None,
                            },
                            "row_condition": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                            "strict_max": {
                                "schema": {"type": "boolean"},
                                "value": None,
                            },
                            "strict_min": {
                                "schema": {"type": "boolean"},
                                "value": None,
                            },
                        },
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "template": "$column minimum value must be greater than or equal "
                        "to $min_value and less than or equal to $max_value.",
                    },
                    "value_type": "StringValueType",
                }
            ],
            [
                {
                    "name": "atomic.diagnostic.observed_value",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": None,
                        "kwargs": None,
                        "params": {},
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "template": "19",
                    },
                    "value_type": "StringValueType",
                }
            ],
            id="expect_column_min_to_be_between",
        ),
        pytest.param(
            ExpectationConfiguration(
                expectation_type="expect_column_quantile_values_to_be_between",
                kwargs={
                    "column": "user_id",
                    "quantile_ranges": {
                        "quantiles": [0.0, 0.5, 1.0],
                        "value_ranges": [
                            [300000, 400000],
                            [2000000, 4000000],
                            [4000000, 10000000],
                        ],
                    },
                },
            ),
            [
                {
                    "name": "atomic.prescriptive.summary",
                    "value": {
                        "graph": None,
                        "header": {
                            "schema": {"type": "StringValueType"},
                            "value": {
                                "params": {
                                    "column": {
                                        "schema": {"type": "string"},
                                        "value": "user_id",
                                    },
                                    "condition_parser": {
                                        "schema": {"type": "string"},
                                        "value": None,
                                    },
                                    "mostly": {
                                        "schema": {"type": "number"},
                                        "value": None,
                                    },
                                    "row_condition": {
                                        "schema": {"type": "string"},
                                        "value": None,
                                    },
                                },
                                "template": "$column quantiles must be within "
                                "the following value ranges.",
                            },
                        },
                        "header_row": [
                            {"schema": {"type": "string"}, "value": "Quantile"},
                            {"schema": {"type": "string"}, "value": "Min Value"},
                            {"schema": {"type": "string"}, "value": "Max Value"},
                        ],
                        "kwargs": None,
                        "params": None,
                        "schema": {"type": "TableType"},
                        "table": [
                            [
                                {"schema": {"type": "string"}, "value": "0.00"},
                                {"schema": {"type": "number"}, "value": 300000},
                                {"schema": {"type": "number"}, "value": 400000},
                            ],
                            [
                                {"schema": {"type": "string"}, "value": "Median"},
                                {"schema": {"type": "number"}, "value": 2000000},
                                {"schema": {"type": "number"}, "value": 4000000},
                            ],
                            [
                                {"schema": {"type": "string"}, "value": "1.00"},
                                {"schema": {"type": "number"}, "value": 4000000},
                                {"schema": {"type": "number"}, "value": 10000000},
                            ],
                        ],
                        "template": None,
                    },
                    "value_type": "TableType",
                }
            ],
            [
                {
                    "name": "atomic.diagnostic.observed_value",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": [
                            {"schema": {"type": "string"}, "value": "Quantile"},
                            {"schema": {"type": "string"}, "value": "Value"},
                        ],
                        "kwargs": None,
                        "params": None,
                        "schema": {"type": "TableType"},
                        "table": [
                            [
                                {"schema": {"type": "string"}, "value": "0.00"},
                                {"schema": {"type": "number"}, "value": 397433},
                            ],
                            [
                                {"schema": {"type": "string"}, "value": "Median"},
                                {"schema": {"type": "number"}, "value": 2388055},
                            ],
                            [
                                {"schema": {"type": "string"}, "value": "1.00"},
                                {"schema": {"type": "number"}, "value": 9488404},
                            ],
                        ],
                        "template": None,
                    },
                    "value_type": "TableType",
                }
            ],
            id="expect_column_quantile_values_to_be_between",
        ),
        pytest.param(
            ExpectationConfiguration(
                expectation_type="expect_column_values_to_be_in_set",
                kwargs={"column": "event_type", "value_set": [19, 22, 73]},
            ),
            [
                {
                    "name": "atomic.prescriptive.summary",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": None,
                        "kwargs": None,
                        "params": {
                            "column": {
                                "schema": {"type": "string"},
                                "value": "event_type",
                            },
                            "condition_parser": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                            "mostly": {"schema": {"type": "number"}, "value": None},
                            "mostly_pct": {"schema": {"type": "string"}, "value": None},
                            "parse_strings_as_datetimes": {
                                "schema": {"type": "boolean"},
                                "value": None,
                            },
                            "row_condition": {
                                "schema": {"type": "string"},
                                "value": None,
                            },
                            "v__0": {"schema": {"type": "string"}, "value": 19},
                            "v__1": {"schema": {"type": "string"}, "value": 22},
                            "v__2": {"schema": {"type": "string"}, "value": 73},
                            "value_set": {
                                "schema": {"type": "array"},
                                "value": [19, 22, 73],
                            },
                        },
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "template": "$column values must belong to this set: $v__0 $v__1 "
                        "$v__2.",
                    },
                    "value_type": "StringValueType",
                }
            ],
            [
                {
                    "name": "atomic.diagnostic.observed_value",
                    "value": {
                        "graph": None,
                        "header": None,
                        "header_row": None,
                        "kwargs": None,
                        "params": {},
                        "schema": {"type": "com.superconductive.rendered.string"},
                        "table": None,
                        "template": "0% unexpected",
                    },
                    "value_type": "StringValueType",
                }
            ],
            id="expect_column_values_to_be_in_set",
        ),
    ],
)
def test_inline_renderer_rendered_content_serialization(
    alice_columnar_table_single_batch_context: DataContext,
    expectation_configuration: ExpectationConfiguration,
    expected_serialized_expectation_configuration_rendered_atomic_content: dict,
    expected_serialized_expectation_validation_result_rendered_atomic_content: dict,
):
    context: DataContext = alice_columnar_table_single_batch_context
    batch_request: BatchRequest = BatchRequest(
        datasource_name="alice_columnar_table_single_batch_datasource",
        data_connector_name="alice_columnar_table_single_batch_data_connector",
        data_asset_name="alice_columnar_table_single_batch_data_asset",
    )
    suite: ExpectationSuite = context.create_expectation_suite("validating_alice_data")

    validator: Validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite=suite,
        include_rendered_content=True,
    )

    expectation_validation_result: ExpectationValidationResult = (
        validator.graph_validate(configurations=[expectation_configuration])
    )[0]

    inline_renderer: InlineRenderer = InlineRenderer(
        render_object=expectation_validation_result
    )
    expectation_configuration_rendered_atomic_content: List[RenderedAtomicContent]
    expectation_validation_result_rendered_atomic_content: List[RenderedAtomicContent]
    (
        expectation_configuration_rendered_atomic_content,
        expectation_validation_result_rendered_atomic_content,
    ) = inline_renderer.render()

    actual_serialized_expectation_configuration_rendered_atomic_content: List[dict] = [
        rendered_atomic_content.to_json_dict()
        for rendered_atomic_content in expectation_configuration_rendered_atomic_content
    ]
    actual_serialized_expectation_validation_result_rendered_atomic_content: List[
        dict
    ] = [
        rendered_atomic_content.to_json_dict()
        for rendered_atomic_content in expectation_validation_result_rendered_atomic_content
    ]

    assert (
        actual_serialized_expectation_configuration_rendered_atomic_content
        == expected_serialized_expectation_configuration_rendered_atomic_content
    )
    assert (
        actual_serialized_expectation_validation_result_rendered_atomic_content
        == expected_serialized_expectation_validation_result_rendered_atomic_content
    )
