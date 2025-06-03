# === Known Fields Directly Used in SPL Queries ===

COLUMN_LIST = [
    "eventDatetime",
    "eventType",
    "index",
    "step",
    "comments",
    "uniqueId",
    "interfaceId",
    "correlationId",
    "source",
    "target",
    "originalClientId",
    "originalClientName",
    "businessObject",
    "appName",
    "environment",
    "sourceBusinessServiceId",
    "targetBusinessServiceId",
    "businessIntegrationNumber",
    "businessUnit",
    "Resource",
    "WorkOrderNumber",
    "IdType",
    "ValidationErrors",
    "OrderNumber",
    "FilePattern",
    "CPQ_Oracle_Integration__c",
    "Type",
    "AssemblyPartNumber",
    "PartNumber",
    "Quantity",
    "billSequenceId",
    "ReportPath",
    "LastUpdateTo",
    "LastUpdateDate",
    "schedulerName",
    "p_start_date",
    "p_end_date",
    "ScheduleId",
    "ItemNumber",
    "PartType",
    "metadata.source",
    "metadata.target"
]

# === User Input to SPL Field Mappings ===
# Helps map conversational words to log schema fields

FIELD_MAPPINGS = {
    "source": "metadata.source",
    "target": "metadata.target",
    "from system": "metadata.source",
    "to system": "metadata.target",
    "origin": "metadata.source",
    "destination": "metadata.target",
    "id": "uniqueId",
    "interface": "interfaceId",
    "correlation": "correlationId",
    "order": "OrderNumber",
    "order number": "OrderNumber",
    "voucher": "OrderNumber",
    "business unit": "businessUnit"
}

# Optional: List of known system names (used in entity extraction)
SYSTEM_NAMES = [
    "SAP",
    "OTM",
    "WMS",
    "TRAX",
    # Add more known systems from your environment
]