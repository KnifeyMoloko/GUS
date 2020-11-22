"""
Aggregate endpoint for the GUS package.
Author: Maciej Cisowski
"""
from Aggregeates.metadata import metadata
from Aggregeates.aggregates import aggregates
from assertpy import assert_that, soft_assertions


def test_aggregates(gus_client):
    agg = aggregates().json()
    with soft_assertions():
        assert_that(agg).is_not_none()
        assert_that(agg).is_type_of(dict)


def test_metadata(gus_client):
    data = metadata().json()
    expected_keys = ["id", "title", "url",
                     "provider", "dateModified", "description",
                     "keywords", "temporalCoverage", "language",
                     "updatePeriod", "contentType"]
    with soft_assertions():
        assert_that(data).is_not_empty()
        for key in data.keys():
            assert_that(expected_keys).contains(key)
            assert_that(data[key]).is_type_of(str)
