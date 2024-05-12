
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
DUMMY_DEPENDENCIES = [
    {
      "type": "library-test",
      "bom-ref": "ahash 0.8.7 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "ahash",
      "version": "0.8.7",
      "description": "A non-cryptographic hash function using AES-NI for high performance",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/ahash@0.8.7",
      "externalReferences": [
        {
          "type": "documentation",
          "url": "https://docs.rs/ahash"
        },
        {
          "type": "vcs",
          "url": "https://github.com/tkaitchuck/ahash"
        }
      ]
    },
    {
      "type": "library-test",
      "bom-ref": "bit-set 0.5.33 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "bit-set",
      "version": "v0.5.33",
      "description": "A set of bits",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/bit-set@0.5.33",
      "externalReferences": [
        {
          "type": "documentation",
          "url": "https://contain-rs.github.io/bit-set/bit_set"
        },
        {
          "type": "website",
          "url": "https://github.com/contain-rs/bit-set"
        },
        {
          "type": "vcs",
          "url": "https://github.com/contain-rs/bit-set"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "async-stream 0.3.5 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "async-stream",
      "version": "0.3.5",
      "description": "Asynchronous streams using async & await notation",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/async-stream@0.3.5",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/tokio-rs/async-stream"
        }
      ]
    },
    {
      "bom-ref": "pkg:golang/github.com/allan-simon/go-singleinstance@v0.0.0-20160830203053-79edcfdc2dfc",
      "type": "library",
      "name": "github.com/allan-simon/go-singleinstance",
      "version": "1.0.0",
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
    {
      "type": "library",
      "bom-ref": "bytes 1.5.0 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "bytes",
      "version": "1.5.0",
      "description": "Types and traits for working with bytes",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/bytes@1.5.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/tokio-rs/bytes"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "config-reader 0.1.0 (path+file:///janus/lib/config-reader)",
      "name": "config-reader",
      "version": "0.1.0",
      "scope": "required",
      "purl": "pkg:cargo/config-reader@0.1.0?download_url=file%3A%2F%2F..%252F..%252F..%252Flib%252Fconfig-reader"
    },
    {
      "type": "library",
      "bom-ref": "fancy-regex 0.11.0 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "fancy-regex",
      "version": "0.11.0",
      "description": "An implementation of regexes, supporting a relatively rich set of features, including backreferences and look-around.",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/fancy-regex@0.11.0",
      "externalReferences": [
        {
          "type": "documentation",
          "url": "https://docs.rs/fancy-regex"
        },
        {
          "type": "vcs",
          "url": "https://github.com/fancy-regex/fancy-regex"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "fastrand 2.0.1 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "fastrand",
      "version": "2.0.1",
      "description": "A simple and fast random number generator",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/fastrand@2.0.1",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/smol-rs/fastrand"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "fnv 1.0.7 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "fnv",
      "version": "1.0.7",
      "description": "Fowler\u2013Noll\u2013Vo hash function",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/fnv@1.0.7",
      "externalReferences": [
        {
          "type": "documentation",
          "url": "https://doc.servo.org/fnv/"
        },
        {
          "type": "vcs",
          "url": "https://github.com/servo/rust-fnv"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "form_urlencoded 1.2.1 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "form_urlencoded",
      "version": "1.2.1",
      "description": "Parser and serializer for the application/x-www-form-urlencoded syntax, as used by HTML forms.",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/form_urlencoded@1.2.1",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/servo/rust-url"
        }
      ]
    },
    {
      "type": "library",
      "bom-ref": "fraction 0.13.1 (registry+https://github.com/rust-lang/crates.io-index)",
      "name": "fraction",
      "version": "0.13.1",
      "description": "Lossless fractions and decimals; drop-in float replacement",
      "scope": "required",
      "licenses": [
        {
          "license": {
            "id": "MIT"
          }
        }
      ],
      "purl": "pkg:cargo/fraction@0.13.1",
      "externalReferences": [
        {
          "type": "documentation",
          "url": "https://docs.rs/fraction/"
        },
        {
          "type": "website",
          "url": "https://github.com/dnsl48/fraction.git"
        },
        {
          "type": "vcs",
          "url": "https://github.com/dnsl48/fraction.git"
        }
      ]
    },
    {
      "bom-ref": "pkg:golang/github.com/chzyer/test@v0.0.0-20180213035817-a1ea475d72b1",
      "type": "library",
      "name": "github.com/chzyer/test",
      "version": "v0.0.0-20180213035817-a1ea475d72b1",
      "scope": "required",
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "abbeb7a9ff61b8dd7590341abd6b2865724d5b7c44138249c876b9436e7fb1df"
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
      "purl": "pkg:golang/github.com/chzyer/test@v0.0.0-20180213035817-a1ea475d72b1",
      "externalReferences": [
        {
          "url": "https://github.com/chzyer/test",
          "type": "vcs"
        }
      ]
    },
    {
      "bom-ref": "pkg:golang/github.com/aymerick/raymond@v2.0.3-0.20180322193309-b565731e1464",
      "type": "library",
      "name": "github.com/aymerick/raymond",
      "version": "v2.0.3-0.20180322193309-b565731e1464",
      "scope": "required",
      "hashes": [
        {
          "alg": "SHA-256",
          "content": "901a7783930a0426984323b3db44d35643a9cadacc01a92f2fb43fcf530b35cf"
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
      "purl": "pkg:golang/github.com/aymerick/raymond@v2.0.3-0.20180322193309-b565731e1464",
      "externalReferences": [
        {
          "url": "https://github.com/aymerick/raymond",
          "type": "vcs"
        }
      ]
    }
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
