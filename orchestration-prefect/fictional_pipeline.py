from datetime import date

from prefect import task, flow


@task
def get_last_date(table_name: str) -> date:
    """Gets latest date from fictional databse)"""

    print(f"Found date for table: {table_name}")
    return date(2025, 4, 17)


@task
def get_data(resource: str, last_date: date) -> None:
    """Gets data from date"""
    print(
        f"Getting data for resource: {resource} and from date: {last_date.strftime('%Y-%m-%d')}"
    )


@flow(log_prints=True)
def fictional_pipeline() -> None:
    """Starts the flow"""
    last_date = get_last_date(table_name="orders")
    get_data(resource="orders", last_date=last_date)


if __name__ == "__main__":
    fictional_pipeline()
