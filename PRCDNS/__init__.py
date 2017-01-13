from PRCDNS import chinaz_client
from PRCDNS import domain_cache


def main():
    """Entry point for the application script"""
    print("Call your main application code here")
    # client = chinaz_client.ChinazClient()
    # client.query_domain()
    cache = domain_cache.DomainCache()
    cache.read()

if __name__ == "__main__":
    main()
