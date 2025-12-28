from pathlib import Path

from sirtuin.controllers import http_headers


def test_get_sirtuin_config(headers_sirtuin_config: Path) -> None:
    config = http_headers._get_sirtuin_config(headers_sirtuin_config)

    assert config.static_redirection
    assert "application" in config.csp
    assert config.csp["application"]["default-src"] == ["self"]
    assert "google-analytics" in config.csp
    assert config.x_frame_options.value == "DENY"
    assert config.x_xss_protection.key == "X-XSS-Protection"


def test_merge_csp_sources(headers_sirtuin_config: Path) -> None:
    config = http_headers._get_sirtuin_config(headers_sirtuin_config)

    csp_sources = http_headers._merge_csp_sources(config)

    assert csp_sources["base-uri"] == ["*.domain.com", "self"]
    assert csp_sources["worker-src"] == ["blob:", "www.google.com"]


def test_generate_content_security_policy(headers_sirtuin_config: Path) -> None:
    config = http_headers._get_sirtuin_config(headers_sirtuin_config)

    assert http_headers._generate_content_security_policy(config) == (
        "base-uri *.domain.com 'self'; "
        "connect-src *.domain.com *.doubleclick.net *.facebook.com *.google.com "
        "*.googlesyndication.com *.intercom.io *.sentry.io about: "
        "ampcid.google.com analytics.google.com connect.facebook.net 'self' "
        "stats.g.doubleclick.net uploads.intercomcdn.com "
        "uploads.intercomusercontent.com wss://*.intercom.io "
        "www.google-analytics.com www.googletagmanager.com "
        "www.googletagservices.com; "
        "default-src 'self'; "
        "font-src data: fonts.intercomcdn.com https://cdn.com "
        "js.intercomcdn.com 'self'; "
        "frame-ancestors *.domain.com; "
        "img-src *.domain.com *.doubleclick.net *.facebook.com "
        "*.facebook.net *.fbcdn.net *.google.com *.googlesyndication.com "
        "*.intercom-mail.com *.intercom.io *.intercomcdn.com "
        "*.intercomusercontent.com analytics.google.com blob: data: "
        "https://cdn.com 'self' ssl.google-analytics.com "
        "static.intercomassets.com www.google-analytics.com www.google.com "
        "www.googleadservices.com www.googletagmanager.com; "
        "media-src dai.google.com js.intercomcdn.com 'self'; "
        "object-src *.googlesyndication.com 'self'; "
        "prefetch-src *.googlesyndication.com 'self'; "
        "script-src *.domain.com https://*.doubleclick.net https://*.google.com "
        "https://*.googleadservices.com https://*.googlesyndication.com "
        "https://*.googletagservices.com https://app.intercom.io "
        "https://connect.facebook.net https://google-analytics.com "
        "https://googletagmanager.com https://graph.facebook.com "
        "https://js.facebook.com https://js.intercomcdn.com "
        "https://ssl.google-analytics.com https://tagmanager.google.com "
        "https://widget.intercom.io https://www.google-analytics.com "
        "https://www.googletagmanager.com 'self' 'unsafe-eval' 'unsafe-inline'; "
        "style-src *.google.com 'self' tagmanager.google.com 'unsafe-inline' "
        "www.googletagmanager.com; child-src *.doubleclick.net *.facebook.com "
        "*.google.com *.googlesyndication.com blob: connect.facebook.net "
        "fast.wistia.net intercom-sheets.com player.vimeo.com "
        "www.googletagmanager.com www.intercom-reporting.com www.youtube.com; "
        "form-action *.facebook.com *.google.com api-iam.intercom.io "
        "connect.facebook.net intercom.help; "
        "frame-src *.doubleclick.net *.facebook.com *.google.com "
        "*.googlesyndication.com connect.facebook.net intercom-sheets.com "
        "www.googletagmanager.com www.intercom-reporting.com; "
        "worker-src blob: www.google.com"
    )
