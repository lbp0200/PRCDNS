from PRCDNS import chinaz_client


def main():
    """Entry point for the application script"""
    print("Call your main application code here")
    client = chinaz_client.ChinazClient()
    client.query_domain()


if __name__ == "__main__":
    main()
