"""Pytest configuration for tests

Primarily for fixtures and mocks used in multiple test files
"""

import logging
import pytest
from unittest import mock

from .. import config
from ..utils import slack, airtable

#########
# SETUP #
#########


# Displays info logs upon test failure
@pytest.fixture(autouse=True)
def _setup_logging(caplog):
    caplog.set_level(logging.INFO)


#########
# MOCKS #
#########


MOCK_CONFIG = config.Config(
    **{
        "airtable": {
            "base_id": "",
            "api_key": "",
            "table_names": {"inbound": "", "volunteer": ""},
        },
        "slack": {
            "api_key": "",
            "test_user_email": "",
            "test_user_id": "",
        },
        "sendgrid": {"api_key": "", "from_email": "", "from_domain": ""},
        "google_cloud": {"project_id": ""},
    }
)


@pytest.fixture
def mock_config():
    with mock.patch(f"{config.__name__}.Config") as mock_config:
        mock_config.load.return_value = MOCK_CONFIG
        yield mock_config


@pytest.fixture
def mock_slack_client():
    with mock.patch(
        f"{slack.__name__}.SlackClient", autospec=True
    ) as mock_client:
        yield mock_client


@pytest.fixture
def mock_airtable_client():
    with mock.patch(
        f"{airtable.__name__}.AirtableClient", autospec=True
    ) as mock_client:
        yield mock_client


@pytest.fixture
def mock_sendgrid_client():
    with mock.patch(
        "sendgrid.SendGridAPIClient", autospec=True
    ) as mock_client, mock.patch("sendgrid.helpers.mail.Mail", autospec=True):
        yield mock_client
