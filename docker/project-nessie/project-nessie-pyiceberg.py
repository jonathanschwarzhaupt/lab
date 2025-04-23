

import marimo

__generated_with = "0.13.0"
app = marimo.App(app_title="project-nessie-pyiceberg")


@app.cell
def _():
    from pyiceberg.catalog import load_catalog
    from pyiceberg.schema import Schema
    from pyiceberg.types import NestedField, IntegerType, StringType
    import pyarrow as pa
    return IntegerType, NestedField, Schema, StringType, load_catalog, pa


@app.cell
def _(load_catalog):
    # Set up the connection to Nessie's REST Catalog
    catalog = load_catalog(
        "nessie",
        **{
            "uri": "http://localhost:19120/iceberg/main",
            "s3.access-key-id": "admin",
            "s3.secret-access-key": "password",
            "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        }
    )

    # Verify connection by listing namespaces
    namespaces = catalog.list_namespaces()
    print("Namespaces:", namespaces)
    return (catalog,)


@app.cell
def _(catalog):
    catalog.create_namespace_if_not_exists("demo")
    return


@app.cell
def _(IntegerType, NestedField, Schema, StringType, catalog):
    # Define the schema for the table
    schema = Schema(
        NestedField(1, "id", IntegerType(), required=True),
        NestedField(2, "name", StringType(), required=False)
    )

    # Create the table in the `demo` namespace
    catalog.create_table_if_not_exists("demo.sample_table", schema)
    return


@app.cell
def _(catalog):
    table = catalog.load_table('demo.sample_table')
    schema_1 = table.schema().as_arrow()
    return schema_1, table


@app.cell
def _(pa, schema_1, table):
    data = pa.Table.from_pylist([{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}, {'id': 3, 'name': 'Charlie'}], schema=schema_1)
    table.overwrite(data)
    return


@app.cell
def _(catalog):
    table_1 = catalog.load_table('demo.sample_table')
    schema_2 = table_1.schema()
    print('Table Schema:', schema_2)
    properties = table_1.properties
    print('Table Properties:', properties)
    return (table_1,)


@app.cell
def _(table_1):
    snapshots = table_1.snapshots()
    print('Table Snapshots:', snapshots)
    return


@app.cell
def _(catalog, pa):
    another_data = pa.Table.from_pylist([{'id': 1, 'name': 'Dave'}, {'id': 2, 'name': 'Eve'}, {'id': 3, 'name': 'Frank'}])
    catalog.create_table_if_not_exists('demo.another_sample_table', schema=another_data.schema)
    table_2 = catalog.load_table('demo.another_sample_table')
    table_2.overwrite(another_data)
    return


@app.cell
def _(catalog):
    table_3 = catalog.load_table('demo.another_sample_table')
    print(table_3.schema())
    return


if __name__ == "__main__":
    app.run()
