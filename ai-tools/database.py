import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    from typing import Optional, List
    from pathlib import Path
    from pydantic import field_validator
    from pydantic_settings import BaseSettings, SettingsConfigDict


    class TursoConfig(BaseSettings):
        db_path: Path
        sync_url: Optional[str] = None
        auth_token: Optional[str] = None

        @field_validator("db_path")
        def validate_db_path(cls, v):
            Path(v).parent.mkdir(parents=True, exist_ok=True)
            Path(v).touch()
            return v

        model_config = SettingsConfigDict(env_prefix="TURSO_")
    return (
        BaseSettings,
        List,
        Optional,
        SettingsConfigDict,
        TursoConfig,
        field_validator,
    )


@app.cell
def _(TursoConfig):
    import libsql
    import logging
    from contextlib import contextmanager

    # from .config import TursoConfig

    logger = logging.getLogger(__name__)


    @contextmanager
    def get_turso_connection(config: TursoConfig):
        """Turso connection optional embedded replica option for remote syncing"""

        conn = None

        try:
            if is_embedded_replica(config):
                conn = libsql.connect(
                    str(config.db_path),
                    sync_url=config.sync_url,
                    auth_token=config.auth_token,
                )
                logger.debug(f"Connected to embedded SQLite database at '{config.db_path}'")

            else:
                conn = libsql.connect(str(config.db_path))
                logger.debug(f"Connected to SQLite database at '{config.db_path}'")

            yield conn

        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

        finally:
            if conn:
                conn.close()


    def is_embedded_replica(config: TursoConfig) -> bool:
        """Returns true if remote connection can be enabled, else false"""
        if config.sync_url and config.auth_token:
            return True

        return False
    return get_turso_connection, is_embedded_replica, logger, logging


@app.cell
def _(
    Optional,
    TursoConfig,
    get_turso_connection,
    is_embedded_replica,
    logging,
):
    # import logging
    # from typing import Optional

    # from .config import TursoConfig
    # from .connection import get_turso_connection, is_embedded_replica


    # logger = logging.getLogger(__name__)


    def get_max_date_string(
        config: TursoConfig,
        table_name: str,
        date_field: str,
        filter_condition: Optional[str],
    ) -> Optional[str]:
        """Gets the max date (string) from table name"""

        result = None
        where_sql = ""

        if filter_condition:
            where_sql = "WHERE " + filter_condition

        with get_turso_connection(config) as conn:
            if is_embedded_replica(config):
                conn.sync()

            table_exists = (
                conn.execute(
                    f"""
                    SELECT COUNT(*) FROM main.sqlite_master
                    WHERE type='table' AND name='{table_name}'
                    """
                ).fetchone()[0]
                > 0
            )

            if not table_exists:
                logging.info("Table does not exist. Returning 'None'")

                return result

            result = conn.execute(
                f"""
                SELECT MAX({date_field})
                FROM main.{table_name}
                {where_sql}
                """
            ).fetchone()[0]
            logging.info(f"Max value for '{date_field}' = '{result}'")

            return result
    return


@app.cell
def _(
    ACCOUNT_BALANCE_FIELD_PATHS,
    ACCOUNT_TRANSACTION_FIELD_PATHS,
    Optional,
    field_validator,
    logger,
):
    from pendulum import Date
    import pendulum
    from pendulum import DateTime
    from typing import Any, Dict
    from pydantic import BaseModel, model_validator, AnyHttpUrl

    def _exctract_from_path(data: dict[str, Any], path: list[str]) -> Any:
        """Walks a path"""

        err_value = None

        for p in path:
            try:
                data = data[p]
            except KeyError:
                logger.debug(
                    f"Could not traverse path due to key error. Did not find '{p}' for '{path}' in data: '{data}'"
                )
                return err_value
            except TypeError:
                logger.debug(
                    f"Could not traverse path due to value error. Found 'None' at '{p}' for '{path}' in data: '{data}'"
                )
                return err_value

        return data

    def _make_flat(
        acct: dict[str, Any], field_paths: dict[str, list[str]]
    ) -> dict[str, Any]:
        """Flattens a dictionary based on field paths to traverse"""

        return {
            field: _exctract_from_path(acct, path) for field, path in field_paths.items()
        }

    class AccountBalance(BaseModel):
        account_id: str
        account_display_id: int
        currency: str
        client_id: str
        account_type__key: str
        account_type__text: str
        iban: str
        bic: str
        credit_limit__value: float
        credit_limit__unit: str
        balance__value: float
        balance__unit: str
        balance_eur__value: float
        balance_eur__unit: str
        available_cash_amount__value: float
        available_cash_amount__unit: str
        available_cash_amount_eur__value: float
        available_cash_amount_eur__unit: str
        # Timestamp fields for database tracking
        _inserted_at_day: Optional[str] = None
        _inserted_at_ts: Optional[str] = None

        @model_validator(mode="before")
        def _flatten(cls, values):
            """This runs before before pydantic maps values to fields"""
            return _make_flat(values, ACCOUNT_BALANCE_FIELD_PATHS)


    class AccountTransaction(BaseModel):
        # required to make Pydantic work with pendulum
        model_config = {"arbitrary_types_allowed": True}

        reference: Optional[str]
        booking_status: str
        booking_date: Optional[Date]
        amount__value: float
        amount__unit: str
        remitter__holder_name: Optional[str]
        deptor: Optional[str]
        creditor__holder_name: Optional[str]
        creditor__iban: Optional[str]
        creditor__bic: Optional[str]
        valuta_date: Optional[Date]
        direct_debit_creditor_id: Optional[str]
        direct_debit_mandate_id: Optional[str]
        end_to_end_reference: Optional[str]
        new_transaction: bool
        remittance_info: str
        transaction_type__key: str
        transaction_type__text: str
        # Timestamp fields for database tracking
        _inserted_at_day: Optional[str] = None
        _inserted_at_ts: Optional[str] = None
        # Additional field for transaction tables
        account_id: Optional[str] = None

        @field_validator("remittance_info", mode="after")
        def strip_whitespace(cls, v: str) -> str:
            """Remove whitespaces from field"""
            return " ".join(v.split())

        @field_validator("reference", mode="after")
        def whitespace_to_none(cls, v: str) -> Optional[str]:
            """Remove whitespaces from field"""
            if v and len(v.strip()) == 0:
                return None
            return v

        @field_validator("booking_date", mode="before")
        def parse_booking_date(cls, v) -> Optional[Date]:
            """Parse booking date string to pendulum Date"""
            if v is None or v == "":
                return None
            if isinstance(v, str):
                return pendulum.parse(v).date()
            return v

        @field_validator("valuta_date", mode="before")
        def parse_valuta_date(cls, v) -> Optional[Date]:
            """Parse valuta date string to pendulum Date"""
            if v is None or v == "":
                return None
            if isinstance(v, str):
                return pendulum.parse(v).date()
            return v

        @model_validator(mode="before")
        def _flatten(cls, values):
            """This runs before before pydantic maps values to fields"""
            return _make_flat(values, ACCOUNT_TRANSACTION_FIELD_PATHS)

    return AccountBalance, AccountTransaction, BaseModel, Dict, pendulum


@app.cell
def _(logger):

    def _ensure_table_exists(
        conn,
        table_name: str,
        ddl: str,
    ) -> None:
        """Ensure table schema exists in Turso database, create if needed"""

        table_exists = (
            conn.execute(
                f"""
                SELECT COUNT(*) FROM main.sqlite_master
                WHERE type='table' AND name='{table_name}'
                """
            ).fetchone()[0]
            > 0
        )

        is_staging_table = table_name.startswith("staging_")

        # For staging tables, drop and recreate; for regular tables, only create if not exists
        if is_staging_table or not table_exists:
            if is_staging_table:
                # Drop staging table if exists, then create new one
                conn.execute(f"DROP TABLE IF EXISTS main.{table_name}")
                create_table_str = f"CREATE TABLE main.{table_name}"
                logger.info(f"Dropped and creating staging table {table_name}")
            else:
                create_table_str = f"CREATE TABLE IF NOT EXISTS main.{table_name}"
                logger.info(f"Creating new table {table_name}")

            logger.debug(
                f"Creating table {table_name} with statement: {create_table_str} and definition: {ddl}"
            )
            conn.execute(
                f"""
                {create_table_str}
                {ddl}
                """
            )
            logger.info(f"Created table {table_name}")
        else:
            logger.info(f"Table {table_name} already exists")
    return


@app.cell
def _(
    AccountBalance,
    AccountTransaction,
    List,
    TursoConfig,
    get_turso_connection,
    is_embedded_replica,
    logger,
):
    def _delete_and_insert(
        conn,
        data: List[AccountBalance] | List[AccountTransaction],
        table_name: str,
        delete_keys: List[str],
        ddl: str,
    ) -> int:
        """Delete existing records matching staging data and insert new data using staging table"""

        len_new_data = len(data)
        if len_new_data < 1:
            logger.info("No new data, returning")
            return 0

        if not delete_keys:
            raise ValueError("'delete_keys' is required.")

        staging_table_name = "staging_" + table_name

        # Create staging table and populate with new data
        # Create staging table schema
        _ensure_table_exists(conn=conn, table_name=staging_table_name, ddl=ddl)

        # Populate staging table with new data
        row_data = data[0].model_dump()
        columns = list(row_data.keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in columns])

        insert_sql = (
            f"INSERT INTO main.{staging_table_name} ({columns_str}) VALUES ({placeholders})"
        )
        logger.debug(f"Populating staging table with SQL: {insert_sql}")

        for row in data:
            row_values = list(row.model_dump(mode="json").values())
            conn.execute(insert_sql, row_values)
        logger.info(f"Populated staging table {staging_table_name} with {len(data)} rows")

        row_count_before = conn.execute(
            f"SELECT COUNT(*) FROM main.{table_name}"
        ).fetchone()[0]

        # Delete existing records that match staging data
        where_condition = " AND ".join(
            [
                f"main.{table_name}.{key} = main.{staging_table_name}.{key}"
                for key in delete_keys
            ]
        )
        delete_sql = f"""
            DELETE FROM main.{table_name}
            WHERE EXISTS (
                SELECT 1 FROM main.{staging_table_name}
                WHERE {where_condition}
            )
        """
        logger.debug(f"Executing DELETE: {delete_sql}")
        conn.execute(delete_sql)
        logger.info(f"Executed DELETE for records matching {len_new_data} staged rows")

        # Insert all records from staging table
        insert_sql = f"""
            INSERT INTO main.{table_name}
            SELECT * FROM main.{staging_table_name}
        """
        logger.debug(f"Executing INSERT: {insert_sql}")
        conn.execute(insert_sql)

        # Clean up staging table
        logger.debug("Dropping staging table")
        conn.execute(f"DROP TABLE IF EXISTS main.{staging_table_name}")

        row_count_after = conn.execute(
            f"SELECT COUNT(*) FROM main.{table_name}"
        ).fetchone()[0]

        conn.commit()
        logger.info("Completed transaction")
        logger.info(
            f"Inserted {len_new_data} new records (net change: {row_count_after - row_count_before})"
        )

        return len_new_data





    def write_account_balances(
        balances: List[AccountBalance],
        config: TursoConfig,
        ddl: str,
        table_name: str = "account_balances",
        delete_keys: List[str] = ["account_id", "_inserted_at_day"],
    ) -> int:
        """Write account balances using transactional delete+insert"""

        if not balances:
            logger.info("No balances passed, returning early")
            return 0

        with get_turso_connection(config) as conn:
            if is_embedded_replica(config):
                conn.sync()

            try:
                # Ensure table schema exists
                _ensure_table_exists(conn=conn, table_name=table_name, ddl=ddl)

                # Always use delete and insert strategy
                inserted_count = _delete_and_insert(
                    conn=conn,
                    data=balances,
                    table_name=table_name,
                    delete_keys=delete_keys,
                    ddl=ddl,
                )

                if is_embedded_replica(config):
                    conn.sync()

                return inserted_count

            except Exception as e:
                conn.rollback()

                if is_embedded_replica(config):
                    conn.sync()

                logger.error(f"Transaction rolled back due to error: {e}")
                raise


    def write_account_transactions_booked(
        transactions: List[AccountTransaction],
        account_id: str,
        config: TursoConfig,
        ddl: str,
        table_name: str = "account_transactions__booked",
        delete_keys: List[str] = ["account_id", "reference"],
    ) -> int:
        """Write account transactions using transactional 'insert if not exists'"""

        if not transactions:
            logger.info("No transactions passed, returning")
            return 0

        # Use model_copy to add account_id without pandas
        enhanced_transactions = [
            transaction.model_copy(update={"account_id": account_id})
            for transaction in transactions
        ]

        with get_turso_connection(config) as conn:
            try:
                if is_embedded_replica(config):
                    conn.sync()

                # Ensure table schema exists
                _ensure_table_exists(conn=conn, table_name=table_name, ddl=ddl)

                # Always use insert if not exists strategy
                inserted_count = _insert_if_not_exists(
                    conn=conn,
                    data=enhanced_transactions,
                    table_name=table_name,
                    ddl=ddl,
                    on_conflict_keys=delete_keys,
                )

                logger.info(f"Transaction commited: {inserted_count} records processesed")
                if is_embedded_replica(config):
                    conn.sync()

                return inserted_count

            except Exception as e:
                conn.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
                raise


    def write_account_transactions_not_booked(
        transactions: List[AccountTransaction],
        account_id: str,
        config: TursoConfig,
        ddl: str,
        table_name: str = "account_transactions__not_booked",
        delete_keys: List[str] = ["account_id"],
    ) -> int:
        """Write not-booked account transactions using transactional 'delete+insert'"""

        if not transactions:
            logger.info("No transactions passed, returning")
            return 0

        # Use model_copy to add account_id without pandas
        enhanced_transactions = [
            transaction.model_copy(update={"account_id": account_id})
            for transaction in transactions
        ]

        with get_turso_connection(config) as conn:
            try:
                if is_embedded_replica(config):
                    conn.sync()

                # Ensure table schema exists
                _ensure_table_exists(conn=conn, table_name=table_name, ddl=ddl)

                # Always use delete and insert strategy
                inserted_count = _delete_and_insert(
                    conn=conn,
                    data=enhanced_transactions,
                    table_name=table_name,
                    delete_keys=delete_keys,
                    ddl=ddl,
                )

                logger.info(f"Transaction commited: {inserted_count} records processesed")
                if is_embedded_replica(config):
                    conn.sync()

                return inserted_count

            except Exception as e:
                conn.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
                raise
    return


@app.cell
def _(AccountBalance, AccountTransaction, List, logger):
    def _insert_if_not_exists(
        conn,
        data: List[AccountBalance] | List[AccountTransaction],
        table_name: str,
        on_conflict_keys: List[str],
        ddl: str,
    ) -> int:
        """Inserts new records if not exists"""

        staging_table_name = "staging_" + table_name

        if not on_conflict_keys:
            raise ValueError("'on_conflict_keys' is required.")

        # Create staging table schema
        _ensure_table_exists(conn=conn, table_name=staging_table_name, ddl=ddl)

        # Populate staging table with new data
        row_data = data[0].model_dump()
        columns = list(row_data.keys())
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in columns])

        insert_sql = (
            f"INSERT INTO main.{staging_table_name} ({columns_str}) VALUES ({placeholders})"
        )
        logger.debug(f"Populating staging table with SQL: {insert_sql}")

        for row in data:
            row_values = list(row.model_dump(mode="json").values())
            conn.execute(insert_sql, row_values)
        logger.info(f"Populated staging table {staging_table_name} with {len(data)} rows")

        row_count_before = conn.execute(
            f"SELECT COUNT(*) FROM main.{table_name}"
        ).fetchone()[0]

        # Filter incoming data to only new data
        where_condition = " AND ".join(
            [
                f"main.{table_name}.{key} = main.{staging_table_name}.{key}"
                for key in on_conflict_keys
            ]
        )

        # 'INSERT INTO SELECT *'
        insert_sql = f"""
            INSERT INTO main.{table_name}
            SELECT * FROM main.{staging_table_name}
            WHERE NOT EXISTS (
                SELECT 1 FROM main.{table_name}
                WHERE {where_condition}
            )
        """
        logger.debug(f"Executing INSERT: {insert_sql}")
        conn.execute(insert_sql)

        logger.debug("Dropping staging table")
        conn.execute(f"DROP TABLE IF EXISTS main.{staging_table_name}")

        row_count_after = conn.execute(
            f"SELECT COUNT(*) FROM main.{table_name}"
        ).fetchone()[0]
        inserted_row_count = row_count_after - row_count_before
        logger.info(f"INSERTED {inserted_row_count} new records")

        conn.commit()
        logger.info("Completed transaction")

        return inserted_row_count
    return


@app.cell
def _(TursoConfig):
    db_config: TursoConfig = TursoConfig(db_path="comdirect_turso.db", _env_file=".env.turso")
    return (db_config,)


@app.cell
def _(db_config: "TursoConfig"):
    db_config
    return


@app.cell
def _(db_config: "TursoConfig", get_turso_connection, is_embedded_replica):
    with get_turso_connection(db_config) as conn:
        try:
            if is_embedded_replica(db_config):
                print("Is embedded. Syncing")
                conn.sync()
                print("Finished syncing")

            table_name = "comdirect_transactions__categorized"
            table_exists = (
            conn.execute(
                f"""
                SELECT COUNT(*) FROM main.sqlite_master
                WHERE type='table' AND name='{table_name}'
                """
            ).fetchone()[0]
            > 0
            )
            print(table_exists)

        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise

    print("done")
    return


@app.cell
def _(
    AccountBalance,
    AccountTransaction,
    BaseModel,
    Dict,
    Optional,
    logger,
    pendulum,
):
    from typing import Type, get_origin, get_args, Union


    def _is_optional_type(field_type) -> bool:
        """Check if a type is Optional (Union with None)"""
        origin = get_origin(field_type)
        if origin is Union:
            args = get_args(field_type)
            return len(args) == 2 and type(None) in args
        return False

    def _map_field_to_sqlite_type(field_type) -> str:
        """Map Pydantic field type to SQLite type"""

        # Handle Optional/Union types - extract the non-None type
        if _is_optional_type(field_type):
            # For Optional[T], get the T part
            args = get_args(field_type)
            if args:
                field_type = args[0] if args[1] is type(None) else args[1]

        # Core type mappings - check against type objects, not instances
        if isinstance(field_type, str):
            return "TEXT"
        elif isinstance(field_type, int):
            return "INTEGER"
        elif isinstance(field_type, float):
            return "REAL"
        elif isinstance(field_type, bool):
            return "INTEGER"  # SQLite stores booleans as 0/1
        elif isinstance(field_type, pendulum.Date):
            return "TEXT"  # Store dates as ISO format strings
        elif isinstance(field_type, pendulum.DateTime):
            return "TEXT"  # Store datetimes as ISO format strings
        else:
            # Default fallback for complex types (store as JSON)
            logger.debug(f"Unknown field type {field_type}, defaulting to TEXT")
            return "TEXT"


    def get_sqlite_ddl_for_model(
        model_class: Type[BaseModel], extra_fields: Optional[Dict[str, str]] = None
    ) -> str:
        """Generate SQLite CREATE TABLE DDL from Pydantic model with optional extra fields"""

        columns = []

        for field_name, field_info in model_class.model_fields.items():
            sqlite_type = _map_field_to_sqlite_type(field_info.annotation)

            # Determine if field is nullable
            is_nullable = not field_info.is_required() or _is_optional_type(
                field_info.annotation
            )

            column_def = f"{field_name} {sqlite_type}"
            if not is_nullable:
                column_def += " NOT NULL"

            columns.append(column_def)

        # Add extra fields if provided
        if extra_fields:
            for field_name, field_type in extra_fields.items():
                columns.append(f"{field_name} {field_type}")

        ddl = "(\n    " + ",\n    ".join(columns) + "\n)"
        logger.debug(f"Generated DDL for {model_class.__name__}: {ddl}")

        return ddl

    # Standard timestamp fields for all Comdirect tables
    TIMESTAMP_FIELDS = {
        "_inserted_at_day": "TEXT DEFAULT (date('now'))",
        "_inserted_at_ts": "TEXT DEFAULT CURRENT_TIMESTAMP",
    }

    # Pre-computed DDL constants for the three main tables with timestamp fields
    ACCOUNT_BALANCES_DDL = get_sqlite_ddl_for_model(
        AccountBalance, extra_fields=TIMESTAMP_FIELDS
    )
    ACCOUNT_TRANSACTIONS_DDL = get_sqlite_ddl_for_model(
        AccountTransaction, extra_fields=TIMESTAMP_FIELDS
    )

    # Schema registry for easy lookup by table name
    COMDIRECT_SCHEMAS: Dict[str, str] = {
        "account_balances": ACCOUNT_BALANCES_DDL,
        "account_transactions__booked": ACCOUNT_TRANSACTIONS_DDL,
        "account_transactions__not_booked": ACCOUNT_TRANSACTIONS_DDL,
    }
    return ACCOUNT_TRANSACTIONS_DDL, TIMESTAMP_FIELDS, get_sqlite_ddl_for_model


@app.cell
def _(ACCOUNT_TRANSACTIONS_DDL):
    print(ACCOUNT_TRANSACTIONS_DDL)
    return


@app.cell
def _(BaseModel, TIMESTAMP_FIELDS, get_sqlite_ddl_for_model):
    from pydantic import Field
    from typing import Literal

    class TransactionCategorization(BaseModel):
        account_id: str = Field(description="The account ID the transaction belongs to")
        reference: str = Field(descriptio="The reference or ID of the transaction")
        improved_description: str = Field(
            description="The improved description of the transaction"
        )
        category: Literal["Groceries", "Travel", "Restaurant"]

    ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL = get_sqlite_ddl_for_model(
        TransactionCategorization, extra_fields=TIMESTAMP_FIELDS
    )
    return (
        ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL,
        Field,
        TransactionCategorization,
    )


@app.cell
def _(ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL):
    print(ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL)
    return


@app.cell
def _(
    AccountTransaction,
    Optional,
    TursoConfig,
    get_turso_connection,
    logging,
):
    def get_transactions_to_categorize(
        config: TursoConfig,
        source_table_name: str,
        categorization_table_name: str,
        filter_condition: Optional[str],
        limit: Optional[int] = 10
    ) -> Optional[list[AccountTransaction]]:
        """Gets the max date (string) from table name"""

        result = None
        where_sql = ""

        if filter_condition:
            where_sql = "WHERE " + filter_condition

        with get_turso_connection(config) as conn:
        
            # Does the source table exist
            source_table_exists = (
                conn.execute(
                    f"""
                    SELECT COUNT(*) FROM main.sqlite_master
                    WHERE type='table' AND name='{source_table_name}'
                    """
                ).fetchone()[0]
                > 0
            )

            # No transactions to categorize - return
            if not source_table_exists:
                logging.info("Source table does not exist. Returning 'None'")
                return result
            print("Source table exists")

            # Transactions do exist, let's find the column names of the table
            columns = conn.execute(
                    """
                    SELECT name
                    FROM PRAGMA_TABLE_INFO('account_transactions__booked')
                    """
                ).fetchall()
            columns = [elem[0] for elem in columns]

            # does the categorization table exist
            categorization_table_exists = (
                conn.execute(
                    f"""
                    SELECT COUNT(*) FROM main.sqlite_master
                    WHERE type='table' AND name='{categorization_table_name}'
                    """
                ).fetchone()[0]
                > 0
            )

            result = None
            # No transactions were categorized yet
            if not categorization_table_exists:
                print(
                    f"Categorization table does not exist. Returning earliest {limit} transactions"
                )
                result = conn.execute(
                    """
                    SELECT *
                    FROM main.account_transactions__booked
                    ORDER BY _inserted_at_ts DESC
                    LIMIT 10
                    """
                ).fetchall()
            # Some transactions were already categorized
            else:
                result = conn.execute(
                    """
                    SELECT *
                    FROM main.account_transactions__booked t1
                    WHERE NOT EXIST (
                        SELECT 1
                        FROM account_transactions__categorized t2
                        WHERE t1.account_id = t1.account_id
                            AND t1.reference = t2.reference
                    )
                    ORDER BY _inserted_at_ts DESC
                    LIMIT 10
                    """
                ).fetchall()

            if not result:
                print("Unexpected error. Raising")
                raise ValueError("Unexpected error obtaining transactions to categorize")

            return [dict(zip(columns, value_list)) for value_list in result]
    return


@app.cell
def _(db_config: "TursoConfig", get_turso_connection):
    # import asyncio

    # In your Marimo cell:
    def run_query():
        with get_turso_connection(db_config) as conn:
            try:
                columns = conn.execute(
                    """
                    SELECT name
                    FROM PRAGMA_TABLE_INFO('account_transactions__booked')
                    """
                ).fetchall()
                columns = [elem[0] for elem in columns]
                print(columns)
                result = conn.execute(
                    """
                    SELECT *
                    FROM main.account_transactions__booked
                    ORDER BY _inserted_at_ts DESC
                    LIMIT 10
                    """
                ).fetchall()
                print(f"Len columns: {len(columns)}")
                print(f"Len data: {len(result[0])}")

                return [dict(zip(columns, value_list)) for value_list in result]


            except Exception as e:
                if "no such table" in str(e):
                    print("NO SUCH TABLE")
                print(f"Error: {e}")
                return None

    # Run it
    result = run_query()
    return (result,)


@app.cell
def _(result):
    keys_to_keep = set(["account_id", "reference", "amount__value", "remitter__holder_name", "remittance_info"])
    result_filtered = [{k: v for k, v in d.items() if k in keys_to_keep} for d in result]
    result_filtered
    return (result_filtered,)


@app.cell
def _(result_filtered):
    result_filtered
    return


@app.cell
def _(BaseSettings, Field, Optional, SettingsConfigDict):
    from pydantic import AliasChoices

    class PydanticAIConfig(BaseSettings):
        api_key: str = Field(
            description="The Anthropic API Key",
            validation_alias=AliasChoices("api_key", "anthropic_api_key")
        )
        logfire_token: Optional[str] = None

        model_config = SettingsConfigDict(env_file=".env")
    return (PydanticAIConfig,)


@app.cell
def _(PydanticAIConfig):
    ai_config = PydanticAIConfig()
    ai_config
    return (ai_config,)


@app.cell
def _():
    import logfire
    import nest_asyncio

    from pydantic_ai import Agent, format_as_xml
    from pydantic_ai.models.anthropic import AnthropicModel
    from pydantic_ai.providers.anthropic import AnthropicProvider

    logfire.configure(
        send_to_logfire="if-token-present",
        service_name="testing-env",
    )  
    logfire.instrument_pydantic_ai()  
    logfire.instrument_httpx(capture_all=True)  
    return (
        Agent,
        AnthropicModel,
        AnthropicProvider,
        format_as_xml,
        nest_asyncio,
    )


@app.cell
def _(
    Agent,
    AnthropicModel,
    AnthropicProvider,
    TransactionCategorization,
    ai_config,
    nest_asyncio,
):
    # To fix 'This event loop is already running' RuntimeError
    nest_asyncio.apply()

    bank_model = AnthropicModel(
        "claude-3-5-sonnet-latest",
        provider=AnthropicProvider(api_key=ai_config.api_key)
    )
    bank_agent = Agent(
        model=bank_model,
        system_prompt="""
        You are a very knowledgeable personal finance assistant.
        Your speciality lies in: 
          * determening the category of a financial transactions
          * providing a consice description of a financial transaction better than the original
        given the details of the transactions.
        """,
        output_type=TransactionCategorization
    )
    return (bank_agent,)


@app.cell
def _(bank_agent, result_filtered):
    transaction_categorizations = list()
    for transaction in result_filtered[:1]:

        categorization_res = bank_agent.run_sync(f"Transaction: '{transaction}'")
        print(categorization_res.output)
        transaction_categorizations.append(categorization_res.output)
    return (transaction_categorizations,)


@app.cell
def _(transaction_categorizations):
    transaction_categorizations[0].model_dump()
    return


@app.cell
def _(result_filtered):
    result_filtered[0]
    return


@app.cell
def _(format_as_xml, result_filtered):
    for transaction_elem in result_filtered[:1]:
        print(format_as_xml(transaction_elem))
    return


@app.cell
def _(
    List,
    TransactionCategorization,
    TursoConfig,
    enhanced_transactions,
    get_turso_connection,
    is_embedded_replica,
    logger,
):
    def write_account_transactions__categorized(
        transactions: List[TransactionCategorization],
        config: TursoConfig,
        ddl: str,
        table_name: str = "account_transactions__categorized",
        delete_keys: List[str] = ["account_id", "reference"],
    ) -> int:
        """Write not-booked account transactions using transactional 'delete+insert'"""

        if not transactions:
            logger.info("No transactions passed, returning")
            return 0

        with get_turso_connection(config) as conn:
            try:
                if is_embedded_replica(config):
                    conn.sync()

                # Ensure table schema exists
                _ensure_table_exists(conn=conn, table_name=table_name, ddl=ddl)

                # Always use delete and insert strategy
                inserted_count = _delete_and_insert(
                    conn=conn,
                    data=enhanced_transactions,
                    table_name=table_name,
                    delete_keys=delete_keys,
                    ddl=ddl,
                )

                logger.info(f"Transaction commited: {inserted_count} records processesed")
                if is_embedded_replica(config):
                    conn.sync()

                return inserted_count

            except Exception as e:
                conn.rollback()
                logger.error(f"Transaction rolled back due to error: {e}")
                raise
    return (write_account_transactions__categorized,)


@app.cell
def _(
    ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL,
    db_config: "TursoConfig",
    transaction_categorizations,
    write_account_transactions__categorized,
):
    write_account_transactions__categorized(
        transactions=transaction_categorizations,
        config=db_config,
        ddl=ACCOUNT_TRANSACTIONS_CATEGORIZATION_DDL
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
