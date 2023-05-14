from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class Variable:
    """
    A way to express an attribute that we'll load from an environment variable,
    with a given default.

    Environment variables are all strings, so the values will be run through the
    `data_type` constructor to make sure they're the correct type.
    """

    attr_name: str
    env_name: str
    default: Any
    data_type: type = str


DEFAULTS = [
    Variable("claude_key", "CLAUDE_KEY", "", str),
    Variable("cohere_key", "COHERE_KEY", "", str),
]


@dataclass
class Environment:
    """
    This class loads in the required environment variables
    """

    claude_key: str
    cohere_key: str

    @classmethod
    def from_environment_variables(cls) -> Environment:
        """
        Load environment variables into an Environment instance.

        Get defaults from the DEFAULTS list, and log when the defaults are used.
        """
        params = {}
        print("Loading environment variables")
        for var in DEFAULTS:
            print("Loading environment variables: " + var.env_name)
            if var.env_name in os.environ:
                print(f"Environment variable {var.env_name} set")
                constructor = var.data_type
                params[var.attr_name] = constructor(os.environ[var.env_name])
            else:
                logger.info(
                    f"Environment variable {var.env_name} not set. Using default {var.default!r}"
                )
                params[var.attr_name] = var.default
        return cls(**params)


ENVIRONMENT = Environment.from_environment_variables()
