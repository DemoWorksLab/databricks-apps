groups = [
    {
        "views": [
            {
                "label": "Introduction",
                "help": "",
                "page": "views/book_intro.py",
                "icon": ":material/skillet_cooktop:",
            },
        ],
    },
    {
        "title": "Tables",
        "views": [
            {
                "label": "Read a table",
                "help": "Query a Unity Catalog Delta table.",
                "page": "views/tables_read.py",
                "icon": ":material/table_view:",
            },
            {
                "label": "Edit a table",
                "help": "Interactively edit a Delta table in the UI.",
                "page": "views/tables_edit.py",
                "icon": ":material/edit_document:",
            },
        ],
    },
    {
        "title": "Volumes",
        "views": [
            {
                "label": "Upload a file",
                "help": "Upload a file into a Unity Catalog Volume.",
                "page": "views/volumes_upload.py",
                "icon": ":material/publish:",
            },
            {
                "label": "Download a file",
                "help": "Download a Volume file.",
                "page": "views/volumes_download.py",
                "icon": ":material/download:",
            },
        ],
    },
    {
        "title": "AI / ML",
        "views": [
            {
                "label": "Invoke a model",
                "help": "Invoke a model across classical ML and Large Language with UI inputs.",
                "page": "views/ml_serving_invoke.py",
                "icon": ":material/experiment:",
            },
            {
                "label": "Run vector search",
                "help": "Use Mosaic AI to generate embeddings for textual data and perform vector search.",
                "page": "views/ml_vector_search.py",
                "icon": ":material/search:",
            },
        ],
    },
    {
        "title": "Business Intelligence",
        "views": [
            {
                "label": "AI/BI Dashboard",
                "help": "Embed an AI/BI dashboard.",
                "page": "views/embed_dashboard.py",
                "icon": ":material/dashboard:",
            },
            # {
            #     "label": "Genie",
            #     "help": "Embed a Genie space.",
            #     "page": "views/genie_api.py",
            #     "icon": ":material/chat:",
            # },
        ],
    },
    {
        "title": "Workflows",
        "views": [
            {
                "label": "Trigger a job",
                "help": "Trigger a job with job parameters.",
                "page": "views/workflows_run.py",
                "icon": ":material/valve:",
            },
            {
                "label": "Retrieve job results",
                "help": "Retrieve results for a Workflow Job run.",
                "page": "views/workflows_get_results.py",
                "icon": ":material/account_tree:",
            },
        ],
    },
    {
        "title": "Compute",
        "views": [
            {
                "label": "Connect",
                "help": "Transform data at scale with UI inputs.",
                "page": "views/compute_connect.py",
                "icon": ":material/lan:",
            },
        ],
    },
    {
        "title": "Authentication",
        "views": [
            {
                "label": "Get current user",
                "help": "Get current App user information.",
                "page": "views/users_get_current.py",
                "icon": ":material/fingerprint:",
            },
            {
                "label": "Retrieve a secret",
                "help": "Get a sensitive API key without hard-coding it.",
                "page": "views/secrets_retrieve.py",
                "icon": ":material/lock:",
            },
        ],
    },
        {
        "title": "Lakebase",
        "views": [
            {
                "label": "Database Operations",
                "help": "Perform transactional operations on the data lake.",
                "page": "views/database_operations.py",
                "icon": ":material/database:",
            },
        ],
    },
]
