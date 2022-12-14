from pydantic import BaseModel, Field

ESCAPED_SOURCES: list[str] = ["self", "unsafe-inline", "unsafe-eval"]


class HttpHeaderConfig(BaseModel):
    key: str = Field(alias="Key")
    value: str | None = Field(default=None, alias="Value")


class HttpHeadersSirtuinConfig(BaseModel):
    static_redirection: bool = Field(default=True, alias="StaticRedirection")
    cache_control: HttpHeaderConfig
    content_security_policy: HttpHeaderConfig
    csp: dict[str, dict[str, list[str]]]
    referrer_policy: HttpHeaderConfig
    strict_transport_security: HttpHeaderConfig
    x_content_type_options: HttpHeaderConfig
    x_frame_options: HttpHeaderConfig
    x_permitted_cross_domain_policies: HttpHeaderConfig
    x_xss_protection: HttpHeaderConfig

    class Config:
        @classmethod
        def alias_generator(cls, variable: str) -> str:
            return variable.replace("_", "-")
