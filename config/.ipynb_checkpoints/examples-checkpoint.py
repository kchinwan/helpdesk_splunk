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