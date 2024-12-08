# MSFabricUtils

A collection of **Spark-free** and **local-first** Python utilities for working with Microsoft Fabric Lakehouses locally or in the Fabric Python Notebook experience.

## Features

- **ETL Utilities** - Extract, Transform, Load data from and to Microsoft Fabric Lakehouses. While the utilities can be configured to fit different needs, its defaults are highly opinionated for what we believe are sensible defaults for many use cases
- **Fabric API** - Access Fabric APIs from Python, such as workspaces and lakehouses
- **Local development first** - Aim to provide a local development for Microsoft Fabric solutions
- **DuckDB Connection** 
    - Seamless integration between DuckDB and Microsoft Fabric Lakehouses
    - Cross-lakehouse and cross-workspace querying
    - Delta Lake writing features

## Core dependencies

MSFabricUtils is built on top of modern, high-performance Python libraries:

- **[delta-rs](https://delta-io.github.io/delta-rs)** - A native Rust implementation of Delta Lake, providing fast and reliable Delta Lake operations without the need for a Spark cluster
- **[Polars](https://pola.rs)** - A lightning-fast DataFrame library written in Rust, offering superior performance for data manipulation tasks
- **[DuckDB](https://duckdb.org)** - An embedded analytical database engine, enabling SQL queries with at blazing speed

These dependencies were chosen specifically to:

- Provide Spark-like functionality without the overhead of a Spark cluster
- Enable high-performance data processing on a single machine
- Support both local development and cloud deployment scenarios
- Maintain compatibility with Delta Lake format used in Microsoft Fabric


## Ideas for improvements
Got an idea? Add an issue on [github](https://www.github.com/mrjsj/msfabricutils/issues)!

