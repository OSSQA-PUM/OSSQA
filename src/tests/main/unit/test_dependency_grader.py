import pytest
from main.data_types.sbom_types.sbom import Sbom

base_sbom_dict = {
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
        ]
}

base_sbom: Sbom = Sbom(base_sbom_dict)


