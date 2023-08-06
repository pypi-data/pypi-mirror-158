# Welcome to ts-ids-core's documentation!

`ts-ids-core` provides a programmatic way of defining TetraScience Intermediate Data Schema (IDS). An IDS defined using the `ts-ids-core` framework can be exported to IDS JSON (`jsonschema` v7) and is thus compatible with the Tetra Data Platform (TDP).

## Install

```shell
pip install ts-ids-core
```

## Quickstart

To define your own Programmatic IDS (PIDS), inherit from classes in `ts_ids_core.schema`; `ts_ids_core.schema.IdsSchema` contains the IDS metadata fields, e.g. IDS version, and should be the parent class to your top-level IDS class.

In addition to defining IDS metadata fields, in the example below we add a field named "samples" that conforms to the predefined component, `Schema`.

```python
from typing import List

from ts_ids_core.schema import IdsSchema, Sample
from ts_ids_core.base.ids_field import IdsField
from ts_ids_core.base.ids_element import SchemaExtraMetadataType


class DemoIdsSchema(IdsSchema):
    #: The type hint `SchemaExtraMetadataType` is required.
    schema_extra_metadata: SchemaExtraMetadataType = {
        "$id": "https://ids.tetrascience.com/my_namespace/demo_ids/v1.0.0/schema.json",
        "$schema": "http://json-schema.org/draft-07/schema#",
    }

    ids_namespace: str = IdsField('my_namespace', const=True)
    ids_type: str = IdsField('my_unique_ids_name', const=True)
    ids_version: str = IdsField('v1.0.0', const=True)

    samples: List[Sample] = IdsField()
```

That's it! You just defined an IDS class. To export the IDS to JSON Schema used by the TDP, run the following code:

```python
ids_json_schema = DemoIdsSchema.schema_json(indent=2)
```

When printed, output will look like this:
<details><summary><a>Expand to show output</a></summary>

```json
{
  "$id": "https://ids.tetrascience.com/my_namespace/my_unique_ids_name/v1.0.0/schema.json",
  "$schema": "http://json-schema.org/draft-07/schema#",
  "description": "Top-level schema.",
  "type": "object",
  "properties": {
    "ids_type": {
      "const": "my_unique_ids_name",
      "type": "string"
    },
    "ids_version": {
      "const": "v1.0.0",
      "type": "string"
    },
    "@idsConventionVersion": {
      "const": "v1.0.0",
      "type": "string"
    },
    "ids_namespace": {
      "const": "my_namespace",
      "type": "string"
    },
    "samples": {
      "type": "array",
      "items": {
        "$ref": "#/definitions/Sample"
      }
    }
  },
  "additionalProperties": false,
  "definitions": {
    "Batch": {
      "type": "object",
      "properties": {
        "id": {
          "type": [
            "string",
            "null"
          ]
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "barcode": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    },
    "Set": {
      "type": "object",
      "properties": {
        "id": {
          "type": [
            "string",
            "null"
          ]
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    },
    "Lot": {
      "type": "object",
      "properties": {
        "id": {
          "type": [
            "string",
            "null"
          ]
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    },
    "Holder": {
      "type": "object",
      "properties": {
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "type": {
          "type": [
            "string",
            "null"
          ]
        },
        "barcode": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "additionalProperties": false
    },
    "Location": {
      "type": "object",
      "properties": {
        "position": {
          "type": [
            "string",
            "null"
          ]
        },
        "row": {
          "type": [
            "number",
            "null"
          ]
        },
        "column": {
          "type": [
            "number",
            "null"
          ]
        },
        "index": {
          "type": [
            "number",
            "null"
          ]
        },
        "holder": {
          "$ref": "#/definitions/Holder"
        }
      },
      "additionalProperties": false
    },
    "Source": {
      "type": "object",
      "properties": {
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "type": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "name",
        "type"
      ],
      "additionalProperties": false
    },
    "ValueDataType": {
      "title": "ValueDataType",
      "description": "An enumeration.",
      "enum": [
        "string",
        "number",
        "boolean"
      ],
      "type": "string"
    },
    "RawSampleTime": {
      "type": "object",
      "properties": {
        "start": {
          "type": [
            "string",
            "null"
          ]
        },
        "created": {
          "type": [
            "string",
            "null"
          ]
        },
        "stop": {
          "type": [
            "string",
            "null"
          ]
        },
        "duration": {
          "type": [
            "string",
            "null"
          ]
        },
        "last_updated": {
          "type": [
            "string",
            "null"
          ]
        },
        "acquired": {
          "type": [
            "string",
            "null"
          ]
        },
        "modified": {
          "type": [
            "string",
            "null"
          ]
        },
        "lookup": {
          "type": [
            "string",
            "null"
          ]
        }
      },
      "required": [
        "lookup"
      ],
      "additionalProperties": false
    },
    "SampleTime": {
      "type": "object",
      "properties": {
        "start": {
          "type": [
            "string",
            "null"
          ]
        },
        "created": {
          "type": [
            "string",
            "null"
          ]
        },
        "stop": {
          "type": [
            "string",
            "null"
          ]
        },
        "duration": {
          "type": [
            "string",
            "null"
          ]
        },
        "last_updated": {
          "type": [
            "string",
            "null"
          ]
        },
        "acquired": {
          "type": [
            "string",
            "null"
          ]
        },
        "modified": {
          "type": [
            "string",
            "null"
          ]
        },
        "lookup": {
          "type": [
            "string",
            "null"
          ]
        },
        "raw": {
          "$ref": "#/definitions/RawSampleTime"
        }
      },
      "required": [
        "lookup"
      ],
      "additionalProperties": false
    },
    "Property": {
      "type": "object",
      "properties": {
        "source": {
          "$ref": "#/definitions/Source"
        },
        "name": {
          "description": "This is the property name",
          "type": "string"
        },
        "value": {
          "description": "The original string value of the parameter",
          "type": "string"
        },
        "value_data_type": {
          "description": "This is the type of the original value",
          "$ref": "#/definitions/ValueDataType"
        },
        "string_value": {
          "description": "If string_value has a value, then numerical_value,\nnumerical_value_unit, and boolean_value all have to be null",
          "type": [
            "string",
            "null"
          ]
        },
        "numerical_value": {
          "description": "If numerical_value has a value, then string_value and\nboolean_value both have to be null",
          "type": [
            "number",
            "null"
          ]
        },
        "numerical_value_unit": {
          "type": [
            "string",
            "null"
          ]
        },
        "boolean_value": {
          "description": "If boolean_value has a value, then numerical_value, numerical_value_unit,\nand string_value all have to be null",
          "type": [
            "boolean",
            "null"
          ]
        },
        "time": {
          "$ref": "#/definitions/SampleTime"
        }
      },
      "required": [
        "source",
        "name",
        "value",
        "value_data_type",
        "string_value",
        "numerical_value",
        "numerical_value_unit",
        "boolean_value",
        "time"
      ],
      "additionalProperties": false
    },
    "Label": {
      "type": "object",
      "properties": {
        "source": {
          "$ref": "#/definitions/Source"
        },
        "name": {
          "type": "string"
        },
        "value": {
          "type": "string"
        },
        "time": {
          "$ref": "#/definitions/SampleTime"
        }
      },
      "required": [
        "source",
        "name",
        "value",
        "time"
      ],
      "additionalProperties": false
    },
    "Sample": {
      "description": "See [here](https://developers.tetrascience.com/docs/ids-design-conventions-schema-templates#samples)\nfor specification of \"samples\". An instance of this class is one item in the\n`samples` array.",
      "type": "object",
      "properties": {
        "id": {
          "type": [
            "string",
            "null"
          ]
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "barcode": {
          "type": [
            "string",
            "null"
          ]
        },
        "batch": {
          "$ref": "#/definitions/Batch"
        },
        "set": {
          "$ref": "#/definitions/Set"
        },
        "lot": {
          "$ref": "#/definitions/Lot"
        },
        "location": {
          "$ref": "#/definitions/Location"
        },
        "properties": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Property"
          }
        },
        "labels": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Label"
          }
        }
      },
      "additionalProperties": false
    }
  }
}
```

</details>
