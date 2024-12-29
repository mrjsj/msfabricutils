# Command Line Interface

The CLI is a way to interact with the Microsoft Fabric REST API. It includes commands for workspaces, lakehouses, and notebooks creation, deletion and updating.

For complete documentation, run `msfu --help`.

!!! warning
    The functions are not fully tested yet.
    Use with caution.
    Please report any issues to the [GitHub repository](https://github.com/mrjsj/msfabricutils/issues).


## Examples

![msfu CLI help](/assets/images/cli-help.png)

![msfu CLI lakehouse create](/assets/images/cli-lakehouse-create.png)

## Available commands
For a quick overview of the commands available, run `msfu tree`.

To see specific subset of commands, run `msfu tree <commands>`. For example, `msfu tree lakehouse` will show all the subcommands related to lakehouses.

```bash
➜  msfabricutils git:(main) ✗ msfu tree lakehouse
Commands
└── lakehouse
    ├── background-jobs
    │   └── run-on-demand-table-maintenance
    ├── create
    ├── delete
    ├── get
    ├── list
    ├── update
    └── tables
        ├── list
        └── load
```

To see subset of subset of commands, run `msfu tree <commands> <subcommand>`. For example, `msfu tree lakehouse tables` will show all the subcommands related to tables in lakehouses.

```bash
➜  msfabricutils git:(main) ✗ msfu tree lakehouse tables
Commands
└── tables
    ├── list
    └── load
```

## Full command structure


```bash
➜  msfabricutils git:(main) ✗ msfu tree
Commands
├── admin
│   ├── domains
│   │   ├── assign-workspaces-by-capacities
│   │   ├── assign-workspaces-by-ids
│   │   ├── assign-workspaces-by-principals
│   │   ├── create
│   │   ├── delete
│   │   ├── get
│   │   ├── list-workspaces
│   │   ├── list
│   │   ├── bulk-assign-role-assignments
│   │   ├── bulk-unassign-role-assignments
│   │   ├── unassign-all-workspaces
│   │   ├── unassign-workspaces-by-ids
│   │   └── update
│   ├── external-data-shares
│   │   ├── list
│   │   └── revoke
│   ├── items
│   │   ├── get
│   │   ├── list-access-details
│   │   └── list
│   ├── labels
│   │   ├── bulk-remove
│   │   └── bulk-set
│   ├── tenants
│   │   ├── list-capacities-tenant-settings-overrides
│   │   └── list-tenant-settings
│   ├── users
│   │   └── list-access-entities
│   └── workspaces
│       ├── get
│       ├── list-git-connections
│       ├── list-workspace-access-details
│       ├── list
│       └── restore
├── capacities
│   └── list
├── connections
│   ├── add-role-assignment
│   ├── create
│   ├── delete
│   ├── delete-role-assignment
│   ├── get
│   ├── get-role-assignment
│   ├── list-role-assignments
│   ├── list
│   ├── list-supported-connection-types
│   ├── update
│   └── update-role-assignment
├── deployment-pipelines
│   ├── deploy-stage-content
│   ├── get
│   ├── list-stage-items
│   ├── list-stages
│   └── list-deployment-pipelines
├── external-data-shares
│   ├── create
│   ├── get
│   ├── list-in-item
│   └── revoke
├── gateways
│   ├── add-role-assignment
│   ├── create
│   ├── delete
│   ├── delete-member
│   ├── delete-role-assignment
│   ├── get
│   ├── get-role-assignment
│   ├── list-members
│   ├── list-role-assignments
│   ├── list
│   ├── update
│   ├── update-member
│   └── update-role-assignment
├── git
│   ├── commit
│   ├── connect
│   ├── disconnect
│   ├── get-connection
│   ├── get-my-git-credentials
│   ├── get-status
│   ├── initialize-connection
│   ├── update-from-git
│   └── update-my-git-credentials
├── items
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list-connections
│   ├── list
│   ├── update
│   └── update-definition
├── job-scheduler
│   ├── cancel-item-job-instance
│   ├── create-item-schedule
│   ├── get-item-job-instance
│   ├── get-item-schedule
│   ├── list-item-job-instances
│   ├── list-item-schedules
│   ├── run-on-demand-item-job
│   └── update-item-schedule
├── long-running-operations
│   ├── get-result
│   └── get-state
├── managed-private-endpoints
│   ├── create
│   ├── delete
│   ├── get
│   └── list
├── one-lake-data-access-security
│   ├── create-or-update-data-access-roles
│   └── list-data-access-roles
├── one-lake-shortcuts
│   ├── create
│   ├── delete
│   ├── get
│   └── list
├── workspaces
│   ├── add-role-assignment
│   ├── assign-to-capacity
│   ├── create
│   ├── delete
│   ├── delete-role-assignment
│   ├── deprovision-identity
│   ├── get
│   ├── get-role-assignment
│   ├── list-role-assignments
│   ├── list
│   ├── provision-identity
│   ├── unassign-from-capacity
│   ├── update
│   └── update-role-assignment
├── dashboard
│   └── list
├── datamart
│   └── list
├── data-pipeline
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   └── update
├── environment
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   ├── update
│   ├── spark-compute
│   │   ├── get-published-settings
│   │   ├── get-staging-settings
│   │   └── update-staging-settings
│   └── spark-libraries
│       ├── cancel-publish
│       ├── delete-staging-library
│       ├── get-published-libraries
│       ├── get-staging-libraries
│       ├── publish-environment
│       └── upload-staging-library
├── eventhouse
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── eventstream
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── kql-dashboard
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── kql-database
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── kql-queryset
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── lakehouse
│   ├── background-jobs
│   │   └── run-on-demand-table-maintenance
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   ├── update
│   └── tables
│       ├── list
│       └── load
├── mirrored-database
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   ├── update-definition
│   └── mirroring
│       ├── get-status
│       ├── get-tables-status
│       ├── start
│       └── stop
├── mirrored-warehouse
│   └── list
├── ml-experiment
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   └── update
├── ml-model
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   └── update
├── notebook
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── paginated-report
│   ├── list
│   └── update
├── report
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   └── update-definition
├── semantic-model
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── spark
│   ├── custom-pools
│   │   ├── create
│   │   ├── delete
│   │   ├── get
│   │   ├── list
│   │   └── update
│   └── spark-settings
│       ├── get
│       └── update
├── spark-job-definition
│   ├── background-jobs
│   │   └── run-on-demand
│   ├── create
│   ├── delete
│   ├── get
│   ├── get-definition
│   ├── list
│   ├── update
│   └── update-definition
├── sql-endpoint
│   └── list
├── warehouse
│   ├── create
│   ├── delete
│   ├── get
│   ├── list
│   └── update
└── tree
```