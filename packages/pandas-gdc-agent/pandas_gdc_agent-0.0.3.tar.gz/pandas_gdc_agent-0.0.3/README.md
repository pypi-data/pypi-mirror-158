# pandas_gdc_agent

This project explores the Hasura Graphql Data Connectors (GDC) using pandas
Dataframe as backend.

To quickly get started, please go through a sample app in `example.py`.

## GDCAgent

Link to pip package: https://pypi.org/project/pandas-gdc-agent/

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
endpoints explained [here](https://github.com/hasura/graphql-engine/tree/master/dc-agents#implementing-data-connector-agents).

## Run example

The `example.py` uses the chinook database. To run the example, first create a
virtual environment:

``` bash
python3 -m venv gdc_env 
```

Now, activate the virtual environment and install the requirements

``` bash
source gdc_env/bin/activate
pip install -r requirements.txt
```

Next, start the GDC agent:
``` bash
python example.py
```

Now start a Hasura Graphql Engine:
``` bash
curl https://raw.githubusercontent.com/hasura/graphql-engine/stable/install-manifests/docker-compose/docker-compose.yaml -o docker-compose.yml

docker-compose up
```

Now apply the following metadata:

```
POST /v1/metadata
```

``` json
{
  "type": "replace_metadata",
  "args": {
    "metadata": {
      "version": 3,
      "backend_configs": {
        "dataconnector": {
          "reference": {
            "uri": "http://localhost:5000/"
          }
        }
      },
      "sources": [
        {
          "name": "chinook",
          "kind": "reference",
          "tables": [
            {
              "table": "Album",
              "object_relationships": [
                {
                  "name": "Artist",
                  "using": {
                    "manual_configuration": {
                      "remote_table": "Artist",
                      "column_mapping": {
                        "ArtistId": "ArtistId"
                      }
                    }
                  }
                }
              ]
            },
            {
              "table": "Artist",
              "array_relationships": [
                {
                  "name": "Album",
                  "using": {
                    "manual_configuration": {
                      "remote_table": "Album",
                      "column_mapping": {
                        "ArtistId": "ArtistId"
                      }
                    }
                  }
                }
              ]
            }
          ],
          "configuration": {
            "tables": [ "Artist", "Album" ]
          }
        }
      ]
    }
  }
}
```
