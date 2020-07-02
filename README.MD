# External Ingestor

External Ingestor is an universal batch data ingestion framework. 
The architecture of this tool is separated into three different modules;
Client, Transform and Sink. The three modules were implemented on a template design pattern since it imposes structure from pluggable components. The batch processing job is written on a
'.yaml' configuration file.

The philosophy behind the framework is:
> Democratizing external data ingestion by enabling self-serve while maintaining robustness and consistency of the system

## Crafting your desired "Ingestion Burger"
![alt text](readme/header.png "Treating data ingestion like a self served burger!")
#### Client
Class responsible as a "client" for external data sources.
- Directory: `external_ingestor/clients/` 
- Output: dict
#### Transformers
Class responsible for client data transformation into a sink-ready format
- Directory: `external_ingestor/transformers/`
- Input: dict
- Output: dataframe
#### Sink
Class responsible for batch sinking the final data format into storage. As a default, we provide a PostgreSQL sink.
- Directory: `external_ingestor/sink/`
- Input: dataframe

## Job Configuration Structure
This job only need a configuration file in '.yaml' extension in **external_ingestor/configs** folder. The config file should be the same as your job name.
We support environment variables to prevent exposed credentials with this syntax `!ENV ${VARIABLE_NAME}` (credits to : https://medium.com/swlh/python-yaml-configuration-with-environment-variables-parsing-77930f4273ac).
### Example Job Configuration: Pulling tickets data from Zendesk
```
method: "get_ticket_incremental"
client: "ZendeskClient"
transformer: "ZendeskTransformer"
sink: "PostgresSink"
domain: "https://vianhazman.zendesk.com/"
path: "/api/v2/incremental/tickets.json"
client_settings: {
  "email": !ENV '${ZD_EMAIL}',
  "password": !ENV '${ZD_TOKEN}'
}
sink_settings: {
  "user": "postgres",
  "pass": !ENV '${PG_PASS}',
  "port": 5432,
  "db": "postgres",
  "host": "localhost",
  "table_name": "zendesk_tickets_test_1"
}
```
#### Configuration Dictionary
- `method`: load method used in sink class
- `transformer`: transformer class used
- `sink`: sink class used
- `domain`: REST domain target
- `path`: REST domain path target
- `client_settings`: settings to configure in used client class
- `sink_settings`: settings to configure in used sink class

## Running the ingestion job
Follow the current command format to run the job of your choice
```
python main.py --jobname [JOB/YAML NAME] --start_time [START TIME IN EPOCH] --end_time [END TIME IN EPOCH - OPTIONAL]
```
For example this is for the Zendesk job
```
python main.py --jobname zendesk_ticket --start_time 1591013586
```