# Command Line Interface

The CLI is a way to interact with the Microsoft Fabric REST API. It includes commands for workspaces, lakehouses, and notebooks creation, deletion and updating.

For complete documentation, run `msfu --help`.

## Examples

### Workspace

```bash
msfu workspace create --name "My Workspace" --description "My workspace description"
```

### Lakehouse

```bash
msfu lakehouse create --name "My Lakehouse" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef" --enable-schemas
```

### Notebook

```bash
msfu notebook create --path "path/to/notebook.Notebook" --workspace-id "beefbeef-beef-beef-beef-beefbeefbeef"
```

