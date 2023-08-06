# pandas_gdc_agent

This project explores the Hasura Graphql Data Connectors (GDC) using pandas
Dataframe as backend.

To quickly get started, please go through a sample app in `app.py`.

## GDCAgent

The `GDCAgent` constructor takes a list of tuples, where the first element
is the table name and the second element is the `DataFrame` which corresponds
to the table name. To setup a `GDCAgent`, run the following:

``` python
# setting up GDC Agent
agent = GDCAgent([("table1",df1),("table2", df2)])
```

Please note that the dataframe must have the primary key as index.

After setting up the `GDCAgent`, start the GDCAgent server by running the
following:

``` python
# starting the GDC Agent
agent.run_agent()
```

When you run the `GDCAgent`, it starts a flask server and exposes the required
endpoints explained [here](https://github.com/hasura/graphql-engine-mono/tree/main/dc-agents#implementing-data-connector-agents).
