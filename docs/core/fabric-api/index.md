# Fabric API

A collection of functions to interact with the Fabric API. I tried to mimic the API as closely as possible, however there are some differences, especially in relation to item defintions.

While the APIs with item definitions takes multiple item parts as base64 encoded strings, these wrapper functions take a path to the folder containing the item parts, e.g.

- `path/to/myReport.Report`
- `path/to/mySemanticModel.SemanticModel`
- `path/to/myNotebook.Notebook`.

!!! warning
    The functions are not fully tested yet.
    Use with caution.
    Please report any issues to the [GitHub repository](https://github.com/mrjsj/msfabricutils/issues).