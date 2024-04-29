
from pathlib import Path

DIRECTORY = Path(__file__).parent

PATHS = [
    DIRECTORY / "example-SBOM.json",
]

SBOM_COMPONENT_URLS = [
    "github.com/ProtonMail/proton-bridge",
    "github.com/allan-simon/go-singleinstance",
    "github.com/andybalholm/cascadia",
    "gitsnub.com/ProtonMail/proton-bridge",
    "",
    "github.com/ProtonMail/",
    "a"
]

DUMMY_SBOM = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.2",
        "serialNumber": "urn:uuid:d7a0ac67-e0f8-4342-86c6-801a02437636",
        "version": 1,
        "metadata": {
            "timestamp": "2021-05-16T17:10:53+02:00",
            "tools": [
                {
                    "vendor": "CycloneDX",
                    "name": "cyclonedx-gomod",
                    "version": "v0.6.1",
                    "hashes": [
                        {
                            "alg": "MD5",
                            "content": "a92d9f6145a94c2c7ad8489d84301eb9"
                        },
                        {
                            "alg": "SHA-1",
                            "content": "a5af6c5ef3f21bf5425c680b64acf57cc6a90c69"
                        },
                        {
                            "alg": "SHA-256",
                            "content": "dc215a651772356eca763d6fe77169379c1cc25c2bb89c7d6df2e2170c3972ab"
                        },
                        {
                            "alg": "SHA-512",
                            "content": "387953ab509c31bf352693de9df617650c87494e607119bc284b91ba9a0a2d284a2e96946c272dc284c4370875412eea855bc30351faedd099dbdbed209e4636"
                        }
                    ]
                }
                ],
                "component": {
                    "bom-ref": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
                    "type": "application",
                    "name": "github.com/ProtonMail/proton-bridge",
                    "version": "v1.8.0",
                    "purl": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
                    "externalReferences": [
                        {
                            "url": "https://github.com/ProtonMail/proton-bridge",
                            "type": "vcs"
                        }
                    ]
                }
            },
        "components": [
            {
        "bom-ref": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "type": "library",
        "name": "github.com/allan-simon/go-singleinstance",
        "version": "v0.0.0-20160830203053-79edcfdc2dfc",
        "scope": "required",
        "hashes": [
            {
            "alg": "SHA-256",
            "content": "99971ad3f1d9fd75973fdb7191f765d861fa994cc1a80972273deee4b83c7ee0"
            }
        ],
        "licenses": [
            {
            "license": {
                "id": "MIT",
                "url": "https://spdx.org/licenses/MIT.html"
            }
            }
        ],
        "purl": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "externalReferences": [
            {
            "url": "https://github.com/allan-simon/go-singleinstance",
            "type": "vcs"
            }
        ]
        }
            ]
    }

BAD_SBOMS = [
    {
    "bomFormat": "CycloneDX",
    "specVersion": "1.2",
    "serialNumber": "urn:uuid:d7a0ac67-e0f8-4342-86c6-801a02437636",
    "metadata": {
        "timestamp": "2021-05-16T17:10:53+02:00",
        "tools": [
        {
            "vendor": "CycloneDX",
            "name": "cyclonedx-gomod",
            "version": "v0.6.1",
            "hashes": [
            {
                "alg": "MD5",
                "content": "a92d9f6145a94c2c7ad8489d84301eb9"
            },
            {
                "alg": "SHA-1",
                "content": "a5af6c5ef3f21bf5425c680b64acf57cc6a90c69"
            },
            {
                "alg": "SHA-256",
                "content": "dc215a651772356eca763d6fe77169379c1cc25c2bb89c7d6df2e2170c3972ab"
            },
            {
                "alg": "SHA-512",
                "content": "387953ab509c31bf352693de9df617650c87494e607119bc284b91ba9a0a2d284a2e96946c272dc284c4370875412eea855bc30351faedd099dbdbed209e4636"
            }
            ]
        }
        ],
        "component": {
        "bom-ref": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
        "type": "application",
        "name": "github.com/ProtonMail/proton-bridge",
        "version": "v1.8.0",
        "purl": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
        "externalReferences": [
            {
            "url": "https://github.com/ProtonMail/proton-bridge",
            "type": "vcs"
            }
        ]
        }
    },
    "components": [
        {
        "bom-ref": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "type": "library",
        "name": "github.com/allan-simon/go-singleinstance",
        "version": "v0.0.0-20160830203053-79edcfdc2dfc",
        "scope": "required",
        "hashes": [
            {
            "alg": "SHA-256",
            "content": "99971ad3f1d9fd75973fdb7191f765d861fa994cc1a80972273deee4b83c7ee0"
            }
        ],
        "licenses": [
            {
            "license": {
                "id": "MIT",
                "url": "https://spdx.org/licenses/MIT.html"
            }
            }
        ],
        "purl": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "externalReferences": [
            {
            "url": "https://github.com/allan-simon/go-singleinstance",
            "type": "vcs"
            }
        ]
        },
        {
        "bom-ref": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
        "type": "library",
        "name": "github.com/andybalholm/cascadia",
        "version": "v1.1.0",
        "scope": "required",
        "hashes": [
            {
            "alg": "SHA-256",
            "content": "06eb8eeac49f40d151bb52e9a606c3db91ebdaf2d85b6e49bf11ece73cec2d3a"
            }
        ],
        "licenses": [
            {
            "license": {
                "id": "BSD-2-Clause",
                "url": "https://spdx.org/licenses/BSD-2-Clause.html"
            }
            }
        ],
        "purl": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
        "externalReferences": [
            {
            "url": "https://github.com/andybalholm/cascadia",
            "type": "vcs"
            }
        ]
        },
        ]
    },
    {
    "bomFormat": "CycloneDX",
    "specVersion": "1.2",
    "serialNumber": "urn:uuidd7a0ac67-e0f8-4342-86c6-801a02437636",
    "version": 1,
    "metadata": {
        "timestamp": "2021-05-16T17:10:53+02:00",
        "tools": [
        {
            "vendor": "CycloneDX",
            "name": "cyclonedx-gomod",
            "version": "v0.6.1",
            "hashes": [
            {
                "alg": "MD5",
                "content": "a92d9f6145a94c2c7ad8489d84301eb9"
            },
            {
                "alg": "SHA-1",
                "content": "a5af6c5ef3f21bf5425c680b64acf57cc6a90c69"
            },
            {
                "alg": "SHA-256",
                "content": "dc215a651772356eca763d6fe77169379c1cc25c2bb89c7d6df2e2170c3972ab"
            },
            {
                "alg": "SHA-512",
                "content": "387953ab509c31bf352693de9df617650c87494e607119bc284b91ba9a0a2d284a2e96946c272dc284c4370875412eea855bc30351faedd099dbdbed209e4636"
            }
            ]
        }
        ],
        "component": {
        "bom-ref": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
        "type": "application",
        "name": "github.com/ProtonMail/proton-bridge",
        "version": "v1.8.0",
        "purl": "pkg:golang/github.com/ProtonMail/proton-bridge@v1.8.0",
        "externalReferences": [
            {
            "url": "https://github.com/ProtonMail/proton-bridge",
            "type": "vcs"
            }
        ]
        }
    },
    "components": [
        {
        "bom-ref": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "type": "library",
        "name": "github.com/allan-simon/go-singleinstance",
        "version": "v0.0.0-20160830203053-79edcfdc2dfc",
        "scope": "required",
        "hashes": [
            {
            "alg": "SHA-256",
            "content": "99971ad3f1d9fd75973fdb7191f765d861fa994cc1a80972273deee4b83c7ee0"
            }
        ],
        "licenses": [
            {
            "license": {
                "id": "MIT",
                "url": "https://spdx.org/licenses/MIT.html"
            }
            }
        ],
        "purl": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
        "externalReferences": [
            {
            "url": "https://github.com/allan-simon/go-singleinstance",
            "type": "vcs"
            }
        ]
        },
        {
        "bom-ref": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
        "type": "library",
        "name": "github.com/andybalholm/cascadia",
        "version": "v1.1.0",
        "scope": "required",
        "hashes": [
            {
            "alg": "SHA-256",
            "content": "06eb8eeac49f40d151bb52e9a606c3db91ebdaf2d85b6e49bf11ece73cec2d3a"
            }
        ],
        "licenses": [
            {
            "license": {
                "id": "BSD-2-Clause",
                "url": "https://spdx.org/licenses/BSD-2-Clause.html"
            }
            }
        ],
        "purl": "pkg:golang/github.com/andybalholm/cascadia@v1.1.0",
        "externalReferences": [
            {
            "url": "https://github.com/andybalholm/cascadia",
            "type": "vcs"
            }
        ]
        },
        ]
    }
]
