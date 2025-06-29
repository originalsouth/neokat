from nibbles.disallowed_csp_hostnames.disallowed_csp_hostnames import nibble

from octopoes.models import Reference
from octopoes.models.ooi.config import Config
from octopoes.models.ooi.findings import Finding, KATFindingType
from octopoes.models.ooi.web import HTTPHeaderHostname


def test_disallowed_csp_headers_no_findings():
    http_header_hostname = HTTPHeaderHostname(
        hostname=Reference.from_str("Hostname|internet|example.com"),
        header=Reference.from_str(
            "HTTPHeader|internet|1.1.1.1|tcp|443|https|internet|example.com|https|internet|example.com|443||Content-Security-Policy"
        ),
    )

    results = list(
        nibble(
            http_header_hostname,
            Config(ooi=http_header_hostname.reference, bit_id="disallowed-csp-hostnames", config={}),
        )
    )

    assert results == []


def test_disallowed_csp_headers_simple_finding():
    http_header_hostname = HTTPHeaderHostname(
        hostname=Reference.from_str("Hostname|internet|bit.ly"),
        header=Reference.from_str(
            "HTTPHeader|internet|1.1.1.1|tcp|443|https|internet|example.com|https|internet|example.com|443||Content-Security-Policy"
        ),
    )

    results = list(
        nibble(
            http_header_hostname,
            Config(ooi=http_header_hostname.reference, bit_id="disallowed-csp-hostnames", config={}),
        )
    )

    assert results == [
        KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP"),
        Finding(
            ooi=http_header_hostname.reference, finding_type=KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP").reference
        ),
    ]


def test_disallowed_csp_headers_allow_url_shortener():
    http_header_hostname = HTTPHeaderHostname(
        hostname=Reference.from_str("Hostname|internet|bit.ly"),
        header=Reference.from_str(
            "HTTPHeader|internet|1.1.1.1|tcp|443|https|internet|example.com|https|internet|example.com|443||Content-Security-Policy"
        ),
    )

    results = list(
        nibble(
            http_header_hostname,
            Config(
                ooi=http_header_hostname.reference,
                bit_id="disallowed-csp-hostnames",
                config={"disallow_url_shorteners": False},
            ),
        )
    )

    assert results == []


def test_disallowed_csp_headers_disallow_custom_hostname():
    http_header_hostname = HTTPHeaderHostname(
        hostname=Reference.from_str("Hostname|internet|example.com"),
        header=Reference.from_str(
            "HTTPHeader|internet|1.1.1.1|tcp|443|https|internet|example.com|https|internet|example.com|443||Content-Security-Policy"
        ),
    )

    results = list(
        nibble(
            http_header_hostname,
            Config(
                ooi=http_header_hostname.reference,
                bit_id="disallowed-csp-hostnames",
                config={"disallowed_hostnames": "example.com"},
            ),
        )
    )

    assert results == [
        KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP"),
        Finding(
            ooi=http_header_hostname.reference, finding_type=KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP").reference
        ),
    ]


def test_disallowed_csp_headers_disallow_custom_hostname_subdomain():
    http_header_hostname = HTTPHeaderHostname(
        hostname=Reference.from_str("Hostname|internet|sub.example.com"),
        header=Reference.from_str(
            "HTTPHeader|internet|1.1.1.1|tcp|443|https|internet|example.com|https|internet|example.com|443||Content-Security-Policy"
        ),
    )

    results = list(
        nibble(
            http_header_hostname,
            Config(
                ooi=http_header_hostname.reference,
                bit_id="disallowed-csp-hostnames",
                config={"disallowed_hostnames": "example.com"},
            ),
        )
    )

    assert results == [
        KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP"),
        Finding(
            ooi=http_header_hostname.reference, finding_type=KATFindingType(id="KAT-DISALLOWED-DOMAIN-IN-CSP").reference
        ),
    ]
