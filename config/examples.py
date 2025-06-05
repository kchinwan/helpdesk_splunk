EXAMPLES = [
    {
        "user": "Find all failed transactions for OrderNumber 123456",
        "spl": "index=ei_prod_mule_apps OrderNumber=123456 eventType=\"ERROR\""
    },
    {
        "user": "Show logs for correlation ID abc-xyz from last 7 days",
        "spl": "index=ei_prod_mule_apps correlationId=\"abc-xyz\" earliest=-7d"
    },
    {
        "user": "Get logs for uniqueId 987654 with eventType INFO",
        "spl": "index=ei_prod_mule_apps uniqueId=987654 eventType=\"INFO\""
    }
]

REFINEMENT_EXAMPLES = [
    {
        "user": "Add a time range for the last 24 hours",
        "spl": 'index=ei_prod_mule_apps eventDatetime>="2025-06-02" eventDatetime<="2025-06-03"'
    },
    {
        "user": "Filter logs from last 7 days",
        "spl": 'index=ei_prod_mule_apps earliest=-7d'
    },
    {
        "user": "Add a filter for OrderNumber 123456",
        "spl": 'index=ei_prod_mule_apps OrderNumber=123456'
    },
    {
        "user": "Include only logs with uniqueId 987654",
        "spl": 'index=ei_prod_mule_apps uniqueId=987654'
    },
    {
        "user": "Add interfaceId SA00057 to the query",
        "spl": 'index=ei_prod_mule_apps interfaceId=SA00057'
    },
    {
        "user": "Add a filter for eventType ERROR",
        "spl": 'index=ei_prod_mule_apps eventType="ERROR"'
    },
    {
        "user": "Add a date range from 2025-05-01 to 2025-05-31",
        "spl": 'index=ei_prod_mule_apps eventDatetime>="2025-05-01" eventDatetime<="2025-05-31"'
    },
    {
        "user": "Filter logs for correlationId abc-xyz",
        "spl": 'index=ei_prod_mule_apps correlationId="abc-xyz"'
    }
]