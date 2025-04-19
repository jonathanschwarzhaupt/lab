import asyncio
from prefect.client.orchestration import get_client


async def fetch_flows(limit: int = 5):
    """
    Fetch up to `limit` flows from Prefect and return the list.
    """
    client = get_client()
    return await client.read_flows(limit=limit)


async def main():
    try:
        flows = await fetch_flows(limit=5)
    except Exception as e:
        print(f"Failed to fetch flows: {e!r}")
        return

    if not flows:
        print(" No flows returned.")
        return

    for flow in flows:
        print(f"{flow.name!r}  (ID: {flow.id})")


if __name__ == "__main__":
    asyncio.run(main())

