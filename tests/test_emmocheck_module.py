from emmopy.emmocheck import main


status = main(
    argv=[
        "--url-from-catalog",
        "--check-imported",
        # Test against a specific commit of EMMO 1.0.0-beta5
        "https://raw.githubusercontent.com/emmo-repo/EMMO/f282769978af9fda7e1c55d1adeeb0ef9e24fc48/emmo.ttl",
    ]
)

assert status == 0
