"""JSON Schema snippets for API contract checks."""

PRODUCT_LIST_SCHEMA = {
    "type": "object",
    "required": ["success", "data", "count"],
    "properties": {
        "success": {"type": "boolean"},
        "count": {"type": "integer"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "title", "price"],
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "price": {"type": ["number", "integer"]},
                    "price_unit": {"type": "string"},
                    "is_available": {"type": ["integer", "boolean"]},
                },
            },
        },
    },
}

CATEGORY_LIST_SCHEMA = {
    "type": "object",
    "required": ["success", "data"],
    "properties": {
        "success": {"type": "boolean"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "name", "slug"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "slug": {"type": "string"},
                },
            },
        },
    },
}

CART_SCHEMA = {
    "type": "object",
    "required": ["success", "cart", "total", "count"],
    "properties": {
        "success": {"type": "boolean"},
        "total": {"type": ["number", "integer"]},
        "count": {"type": "integer"},
        "cart": {"type": "array"},
    },
}

STATUS_SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {"type": "string"},
        "timestamp": {"type": "string"},
        "version": {"type": "string"},
    },
}
