from pathlib import Path

from sirtuin.models.http_headers import ESCAPED_SOURCES, HttpHeadersSirtuinConfig
from sirtuin.utils.constants import DEFAULT_AWS_PROFILE
from sirtuin.utils.decorators import catch_remote_config
from sirtuin.utils.loaders import read_toml_file


def _get_sirtuin_config(filepath: Path) -> HttpHeadersSirtuinConfig:
    return HttpHeadersSirtuinConfig(**read_toml_file(filepath))


def _merge_csp_sources(config: HttpHeadersSirtuinConfig) -> dict[str, list[str]]:
    csp_sources: dict[str, set[str]] = {}

    for _, rules in config.csp.items():
        for source_type, sources in rules.items():
            if source_type in csp_sources:
                csp_sources[source_type] = csp_sources[source_type].union(set(sources))
            else:
                csp_sources[source_type] = set(sources)

    return {key: sorted(list(value)) for key, value in csp_sources.items()}


def _catch_csp_exceptions(sources: list[str]) -> list[str]:
    return [
        f"'{source}'" if source in ESCAPED_SOURCES else source for source in sources
    ]


def _generate_content_security_policy(config: HttpHeadersSirtuinConfig) -> str:
    csp_sources = _merge_csp_sources(config)

    return "; ".join(
        [
            f"{source_type} {' '.join(_catch_csp_exceptions(sources))}"
            for source_type, sources in csp_sources.items()
        ]
    )


@catch_remote_config
def print_content_security_policy(
    filepath: Path, profile: str = DEFAULT_AWS_PROFILE, verbose: bool = False
) -> None:
    print(_generate_content_security_policy(_get_sirtuin_config(filepath)))
