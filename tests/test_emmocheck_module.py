from emmopy.emmocheck import main


main(
    argv=[
        "--url-from-catalog",
        "--check-imported",
        # Test against a specific commit of EMMO 1.0.0-beta5
        "https://raw.githubusercontent.com/emmo-repo/EMMO/3b93e2c9c45ab8d9882d2d6385276ff905095798/emmo.ttl",
    ]
)
