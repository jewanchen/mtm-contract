# Using MTM Contract with MCP and Function Calling

> **Status:** Phase 1 — schema documented; Phase 3 will publish a
> reference MCP server and OpenAI function-calling schemas as
> separate packages.

This guide covers two related but distinct integrations:

1. **Model Context Protocol (MCP)** — Anthropic's open protocol
   for AI tool integration. An MCP server exposes MTM Contract
   operations as tools usable by any MCP-compatible client (Claude
   Desktop, agent frameworks adopting MCP, future IDE plugins).
2. **OpenAI / Anthropic function calling** — JSON-schema-based
   tool descriptions readable by the major LLM APIs. The MTM
   Contract structure translates to a function schema that any
   agent can invoke.

Both reduce MTM Contract from a *markdown convention* to a
*structured tool call* — preserving the eleven-field discipline
while letting the agent emit contracts programmatically rather than
in prose.

---

## Function-calling schema

The eleven-field MTM Contract maps directly onto a JSON schema
suitable for `tools` in OpenAI's Chat Completions API, `tools` in
the Anthropic Messages API, and MCP tool descriptions.

```json
{
  "name": "create_mtm_contract",
  "description": "Create an MTM Contract for a non-trivial task. Fill in all required fields before implementation begins. UNKNOWN preconditions must be resolved by tool use (grep, read, list) before the contract is finalised.",
  "input_schema": {
    "type": "object",
    "required": [
      "intent",
      "affected_layers",
      "preconditions",
      "expected_outcome",
      "confidence",
      "escalation"
    ],
    "properties": {
      "intent": {
        "type": "string",
        "description": "One observable sentence stating what the user will be able to do, see, or experience."
      },
      "affected_layers": {
        "type": "array",
        "description": "Enumeration of subsystems that change and subsystems that deliberately do not.",
        "items": {
          "type": "object",
          "required": ["layer", "change"],
          "properties": {
            "layer": { "type": "string" },
            "change": { "type": "string" }
          }
        }
      },
      "preconditions": {
        "type": "array",
        "description": "Conditions that must be true before implementation. Each must include how it has been verified.",
        "items": {
          "type": "object",
          "required": ["condition", "verified_by"],
          "properties": {
            "condition": { "type": "string" },
            "verified_by": {
              "type": "string",
              "description": "Citable reference: commit hash, file path, migration name, or 'UNKNOWN: <what to verify>' if not yet resolved."
            }
          }
        }
      },
      "schema_assumptions": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["assumption", "source"],
          "properties": {
            "assumption": { "type": "string" },
            "source": { "type": "string" }
          }
        }
      },
      "cross_module_contract": {
        "type": "object",
        "properties": {
          "emit": { "type": "array", "items": { "type": "string" } },
          "listen": { "type": "array", "items": { "type": "string" } },
          "depends_on": { "type": "array", "items": { "type": "string" } },
          "guaranteed_to_callers": { "type": "array", "items": { "type": "string" } }
        }
      },
      "expected_outcome": {
        "type": "array",
        "description": "Externally observable end-states, each with a verifiable_by reference.",
        "items": {
          "type": "object",
          "required": ["outcome", "verifiable_by"],
          "properties": {
            "outcome": { "type": "string" },
            "verifiable_by": { "type": "string" }
          }
        }
      },
      "confidence": {
        "type": "object",
        "required": ["overall"],
        "properties": {
          "overall": { "enum": ["high", "medium", "low"] },
          "low_confidence_subitems": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["subitem", "reason", "plan"],
              "properties": {
                "subitem": { "type": "string" },
                "reason": { "type": "string" },
                "plan": {
                  "enum": ["escalate", "spike", "document_and_proceed"]
                }
              }
            }
          }
        }
      },
      "escalation": {
        "type": "object",
        "properties": {
          "decisions_to_defer": {
            "type": "array",
            "items": { "type": "string" }
          },
          "halt_conditions": {
            "type": "array",
            "items": { "type": "string" }
          }
        }
      },
      "grounding": {
        "type": "array",
        "items": { "type": "string" }
      },
      "rollback_plan": {
        "type": "object",
        "properties": {
          "code": { "type": "string" },
          "schema": { "type": "string" },
          "env": { "type": "string" }
        }
      },
      "test_plan": {
        "type": "object",
        "properties": {
          "local": { "type": "string" },
          "staging": { "type": "string" },
          "prod": { "type": "string" }
        }
      }
    }
  }
}
```

And the audit-time companion:

```json
{
  "name": "audit_mtm_contract",
  "description": "Audit a completed MTM Contract clause by clause.",
  "input_schema": {
    "type": "object",
    "required": ["contract_path", "results"],
    "properties": {
      "contract_path": { "type": "string" },
      "results": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["clause", "mark"],
          "properties": {
            "clause": { "type": "string" },
            "mark": { "enum": ["PASS", "FAIL", "MUTATED", "UNVERIFIED"] },
            "reason": { "type": "string" }
          }
        }
      },
      "mutated_summary": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["clause", "original", "actual", "reason"],
          "properties": {
            "clause": { "type": "string" },
            "original": { "type": "string" },
            "actual": { "type": "string" },
            "reason": { "type": "string" }
          }
        }
      },
      "follow_ups": { "type": "array", "items": { "type": "string" } },
      "overall_code_level": { "enum": ["PASS", "FAIL"] },
      "overall_observation_level": { "enum": ["PASS", "INCOMPLETE"] },
      "overall_contract_completeness": { "enum": ["high", "medium", "low"] }
    }
  }
}
```

Register these schemas as tools in your agent stack, and the agent
will emit and audit contracts as first-class function calls rather
than free-text markdown.

---

## MCP server (planned, Phase 3)

A planned MCP server will expose these schemas as MCP tools, plus
filesystem operations to persist contracts to a project's
`contracts/` directory.

Stub server structure (TypeScript, reference implementation):

```typescript
// Planned in Phase 3 — see roadmap in the main article.
import { McpServer } from '@anthropic-ai/mcp-sdk';

const server = new McpServer({ name: 'mtm-contract', version: '1.0' });

server.tool('mtm_new', /* schema */, async ({ task }) => {
  // Copy TEMPLATE.md into contracts/YYYY-MM-DD_<task>.md
});

server.tool('mtm_validate', /* schema */, async ({ path }) => {
  // Parse the file, check all 11 fields are populated,
  // check that verified_by references resolve to real
  // files / commits in the repo.
});

server.tool('mtm_audit', /* schema */, async ({ path, results }) => {
  // Append the audit section to the contract file.
});

server.tool('mtm_metrics', /* schema */, async () => {
  // Walk contracts/, compute one-pass rate, hallucinations
  // caught, MUTATED frequency.
});

server.start();
```

When the server ships, any MCP-compatible client gets MTM Contract
integration without code changes — point Claude Desktop or your
preferred MCP host at the server and the tools are available.

---

## Programmatic use today (Phase 1)

You don't need to wait for the MCP server. Today, you can:

- **Copy the JSON schemas above** into your agent stack's
  `tools` array (OpenAI Assistants API, Anthropic Messages API,
  LangChain, CrewAI, etc.).
- **Wire the tool handler** to write the contract to a
  `contracts/` directory in your project.
- **Validate manually** that the agent's tool call fills all
  required fields and that `verified_by` references resolve.

The Phase 3 MCP server will not invent new functionality; it will
package this same workflow into one drop-in dependency.

---

## Cross-vendor compatibility

The schemas above are vendor-neutral:

- **OpenAI**: paste as a `function` in your Chat Completions
  `tools` array.
- **Anthropic**: paste as a `tool` in your Messages API
  `tools` array.
- **Google Gemini**: translate to Gemini's `function_declaration`
  format (structure is identical, naming differs slightly).
- **MCP**: register as an MCP tool definition.

The MTM Contract methodology is layer 1 — model-agnostic.
Function-calling and MCP are layer 2 — the wire format. Both
serve the same underlying discipline.

---

*See the main repository for the full methodology:
[github.com/jewanchen/mtm-contract](https://github.com/jewanchen/mtm-contract).*
