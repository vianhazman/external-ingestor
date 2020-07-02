# External Ingestor

External Ingestor is an universal batch data ingestion framework. 
The architecture of this tool is separated into three different modules;
Client, Transform and Sink. The three modules were implemented on a template design pattern since it imposes structure from pluggable components. The batch processing job is written on a
'.yaml' configuration file.

## Crafting your desired "Ingestion Burger"
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

