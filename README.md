# recall
wip prob storage

````markdown
# README_AGENTS.md
# Total Recall System: Production Specification (v1.0)

## 1. Project Vision & Core Principles

### 1.1. Vision
To create a secure, private, and powerful personal recall system that provides users with a searchable, semantic memory of their digital interactions. This system will act as a foundational layer for augmenting human intelligence and enabling proactive, agentic AI workflows.

### 1.2. Core Principles
This specification is binding for all development, testing, and deployment agents. Adherence is non-negotiable.

* **User Sovereignty:** The user has absolute and sole control over their data. The system is a personal tool, not a data collection service.
* **Privacy & Security by Design:** The architecture MUST be built on a zero-trust, hardware-anchored security model from the ground up. (See Phase 4).
* **On-Device Processing:** All user data (snapshots, OCR text, embeddings) MUST be processed and stored locally on the user's machine. No personal data is sent to the cloud for AI processing.
* **Seamless Integration:** The system must operate efficiently in the background, leveraging NPUs to avoid performance degradation.

---

## 2. Agent Directives & System Prompts

This section contains machine-readable JSON prompts for initializing AI agents assigned to specific, critical development tasks.

### 2.1. Security Compliance Agent (SecurityAgent)

This agent's role is to audit all code contributions, architectural decisions, and automation scripts to ensure strict adherence to the Phase 4 Zero-Trust framework.

```json
{
  "role": "SecurityComplianceAuditorAgent",
  "version": 1.0,
  "system_prompt": "You are a 'Security Compliance Auditor Agent' specializing in Zero-Trust, on-device security. Your single-minded purpose is to enforce the 'Total Recall System' production specification. Your analysis must be strict and uncompromising.",
  "tasks": [
    "Analyze all new code commits, pull requests, and architectural documents.",
    "REJECT any implementation that does not adhere to the 'Privacy & Security by Design' principle.",
    "Ensure all data storage and processing logic complies with Phase 4 requirements (Windows Hello ESS, VBS isolation, TPM-anchored keys).",
    "Block any code that attempts to send personal user data (images, text, embeddings) to an external cloud API.",
    "Validate that all user controls (opt-in, delete, pause, exclude) are implemented as specified.",
    "Reference 'Phase 4: Security & Privacy Hardening' as your non-negotiable source of truth."
  ],
  "output_format": {
    "compliance_status": "PASS/FAIL",
    "violations": [
      {
        "spec_reference": "Phase X.Y",
        "issue": "Description of the security violation.",
        "remediation": "Specific, actionable steps to fix the violation."
      }
    ]
  }
}
````

### 2.2. NPU Optimization Agent (NpuAgent)

This agent's role is to ensure all local AI models (OCR, embeddings) meet the performance and hardware requirements specified in Phase 2.

```json
{
  "role": "NpuOptimizationSpecialistAgent",
  "version": 1.0,
  "system_prompt": "You are an 'NPU Optimization Specialist Agent'. Your mission is to ensure the 'Total Recall System's' AI pipeline runs with maximum efficiency on local NPU hardware, as defined in Phase 2.",
  "tasks": [
    "Analyze the model integration pipeline (OCR, multimodal embeddings).",
    "Ensure all models are converted to and optimized for ONNX Runtime.",
    "Verify that the system correctly detects NPU hardware with a minimum of 40 TOPS.",
    "Design and validate automation scripts that benchmark model inference speed (ms) and NPU utilization (%).",
    "REJECT any implementation that falls back to CPU/GPU for core AI processing if a 40+ TOPS NPU is present.",
    "Ensure the system gracefully disables itself if the minimum hardware requirement is not met, as per the spec."
  ],
  "output_format": {
    "hardware_compliance": "PASS/FAIL/NOT_PRESENT",
    "min_tops_met": true,
    "model_benchmarks": [
      {
        "model": "OCR",
        "runtime": "ONNX",
        "accelerator": "NPU",
        "inference_time_ms": "<value>"
      },
      {
        "model": "Multimodal_Embedding",
        "runtime": "ONNX",
        "accelerator": "NPU",
        "inference_time_ms": "<value>"
      }
    ]
  }
}
```

-----

## 3\. Phased Implementation Plan & Artifacts

### Phase 1: The Ingestion Engine (Core Service)

  * **Objective:** Develop the background Windows Service for secure screen capture and local storage.
  * **Key Components:** Windows Service, `Windows.Graphics.Capture` API, local SQLite (for metadata), local file system (for PNGs), DPAPI (initial encryption).

#### AUTOMATION EXECUTION: Phase 1 Test Script

This script validates the core functionality of the ingestion service.

```bash
#!/bin/bash
# P1_Validation.sh - Phase 1 Validation Script (Pseudocode)

echo "Running Phase 1 Validation..."

# 1. Check if the Windows Service is running
SERVICE_NAME="TotalRecallIngestionService"
SERVICE_STATUS=$(sc query $SERVICE_NAME | grep "STATE" | awk '{print $4}')

if [ "$SERVICE_STATUS" != "RUNNING" ]; then
  echo "FAIL: $SERVICE_NAME is not running."
  exit 1
else
  echo "PASS: $SERVICE_NAME is RUNNING."
fi

# 2. Check for data store creation
DATA_PATH="$LOCALAPPDATA/TotalRecall/data"
DB_FILE="$DATA_PATH/metadata.db"
SNAPSHOT_DIR="$DATA_PATH/snapshots"

if [ ! -f "$DB_FILE" ] || [ ! -d "$SNAPSHOT_DIR" ]; then
  echo "FAIL: Data store not created at $DATA_PATH"
  exit 1
else
  echo "PASS: Data store directories exist."
fi

# 3. Monitor for new snapshot creation
echo "Monitoring for new snapshots (10s)..."
initial_count=$(ls -1 $SNAPSHOT_DIR | wc -l)
sleep 10
final_count=$(ls -1 $SNAPSHOT_DIR | wc -l)

if [ $final_count -gt $initial_count ]; then
  echo "PASS: New snapshots are being captured."
else
  echo "FAIL: No new snapshots detected in the last 10 seconds."
  exit 1
fi

echo "Phase 1 Validation Complete."
```

-----

### Phase 2: On-Device Intelligence (The Retrieval Core)

  * **Objective:** Implement the on-device AI pipeline (OCR, embeddings) and the local vector database.
  * **Key Components:** NPU (40+ TOPS req), local OCR model, local multimodal embedding model (ONNX), in-process vector database (e.g., LanceDB).

#### YAML ARTIFACT: Hardware Requirement Manifest

This manifest is used by the installer and the `NpuAgent` to validate hardware.

```yaml
# HardwareRequirementManifest.yaml
# Defines the minimum hardware needed for the On-Device Intelligence phase.

system:
  architecture: x64
  os: Windows 11 (22H2 or later) # Required for modern NPU drivers
  
required_components:
  - component: NPU # Neural Processing Unit
    type: "On-Chip-AI-Accelerator"
    minimum_performance:
      value: 40
      unit: TOPS # Trillions of Operations Per Second
    status_check: "REQUIRED" # System will not run without this.

  - component: TPM
    version: "2.0"
    status_check: "REQUIRED" # Required for Phase 4.

failure_mode:
  on_missing_npu:
    action: "DISABLE"
    user_message: "Total Recall requires an NPU (Neural Processing Unit) with at least 40 TOPS to run. This feature will be disabled as your hardware does not meet this requirement."
```

#### AUTOMATION EXECUTION: Phase 2 NPU Check

This script checks for the NPU hardware requirement.

```bash
#!/bin/bash
# P2_NpuCheck.sh - Phase 2 NPU Validation (Pseudocode)

echo "Running Phase 2 NPU Check..."

# This is a pseudocode representation.
# A real implementation would use WMI, DirectX diagnostics, or Windows AI APIs.
NPU_TOPS=$(get_npu_performance_tops)
MIN_TOPS=40

if [ $NPU_TOPS -ge $MIN_TOPS ]; then
  echo "PASS: NPU detected with $NPU_TOPS TOPS (Minimum: $MIN_TOPS)."
  # Trigger NpuAgent to benchmark models
  run_agent NpuOptimizationSpecialistAgent --task benchmark
else
  echo "FAIL: NPU does not meet minimum requirement. Found $NPU_TOPS TOPS."
  # Trigger system graceful disable logic
  set_feature_flag TotalRecallEnabled false
  exit 1
fi
```

-----

### Phase 3: The User Experience (Recall Interface)

  * **Objective:** Build the user-facing application for search and interaction.
  * **Key Components:** Timeline UI, semantic search bar, "Actionable Snapshots" (copy text, crop image).

#### AUTOMATION EXECUTION: Phase 3 Semantic Search Test

This script simulates a UI test for the semantic search feature.

```bash
#!/bin/bash
# P3_SearchTest.sh - Phase 3 Semantic Search E2E Test (Pseudocode)

echo "Running Phase 3 Semantic Search Test..."

# 1. Define a test query
QUERY_TEXT="that email about the quarterly budget"

# 2. Agent simulates vectorizing the query
# This calls the same local model used for ingestion
QUERY_VECTOR=$(./local_embedder_cli --text "$QUERY_TEXT")

# 3. Agent simulates querying the vector DB
# This queries the local vector DB directly
SEARCH_RESULTS=$(./vector_db_cli --query_vector $QUERY_VECTOR --top_k 1)

# 4. Validate the result
# 'SEARCH_RESULTS' would be a JSON/text output, e.g., "snapshot_id: 12345, score: 0.92"
SNAPSHOT_ID=$(echo $SEARCH_RESULTS | awk '{print $1}')
CONFIDENCE=$(echo $SEARCH_RESULTS | awk '{print $2}')

if [ "$SNAPSHOT_ID" != "NULL" ] && [ $(echo "$CONFIDENCE > 0.8" | bc) -eq 1 ]; then
  echo "PASS: Semantic search returned result $SNAPSHOT_ID with confidence $CONFIDENCE."
else
  echo "FAIL: Semantic search failed to find a relevant result for query: '$QUERY_TEXT'"
  exit 1
fi
```

-----

### Phase 4: Security & Privacy Hardening (The Zero-Trust Framework)

  * **Objective:** Re-architect the system for maximum, non-negotiable security.
  * **Key Components:** Mandatory Opt-In, Windows Hello ESS, TPM/Pluton key protection, AES-256 encryption, VBS isolation, granular user controls.

#### AUTOMATION EXECUTION: Phase 4 Security Audit

This script is run by the `SecurityAgent` to audit the production build.

```bash
#!/bin/bash
# P4_SecurityAudit.sh - Phase 4 Security Compliance Audit (Pseudocode)

echo "Running Phase 4 Security Audit..."
FAIL_COUNT=0

# 1. Check for Mandatory Opt-In (Default Disabled)
IS_ENABLED_DEFAULT=$(read_config_default "TotalRecallEnabled")
if [ "$IS_ENABLED_DEFAULT" != "false" ]; then
  echo "FAIL: Feature is NOT disabled by default. (Mandatory Opt-In)"
  ((FAIL_COUNT++))
else
  echo "PASS: Feature is disabled by default."
fi

# 2. Check for VBS Enclave
# This would check OS configuration and service registration
VBS_STATUS=$(check_service_isolation_status "TotalRecallIngestionService")
if [ "$VBS_STATUS" != "VBS_SECURE_ENCLAVE" ]; then
  echo "FAIL: Service is not running in a VBS secure enclave."
  ((FAIL_COUNT++))
else
  echo "PASS: Service is isolated within VBS."
fi

# 3. Check for TPM-Bound Keys
# This would use Windows APIs to check key storage properties
KEY_PROTECTION_STATUS=$(check_key_protection "RecallMasterKey")
if [ "$KEY_PROTECTION_STATUS" != "TPM_PROTECTED_PLUS_HELLO_ESS" ]; then
  echo "FAIL: Master encryption key is not anchored in TPM and gated by Windows Hello ESS."
  ((FAIL_COUNT++))
else
  echo "PASS: Master key is hardware-anchored and biometrically gated."
fi

# 4. Check for Cloud Communication
echo "Sniffing network traffic from service (15s)..."
# This would run a local network monitor (e.g., Wireshark/tcpdump)
# filtered for the service executable.
TRAFFIC_LOG=$(sniff_network_traffic $SERVICE_NAME 15)
if grep -q -E "(http|https|ftp)://" <<< "$TRAFFIC_LOG"; then
  echo "FAIL: Service initiated unauthorized cloud communication."
  ((FAIL_COUNT++))
else
  echo "PASS: No external cloud traffic detected."
fi

# Final Verdict
if [ $FAIL_COUNT -gt 0 ]; then
  echo "AUDIT FAILED: $FAIL_COUNT critical security violations found."
  exit 1
else
  echo "AUDIT PASSED: System meets Phase 4 Zero-Trust requirements."
fi
```

-----

### Phase 5: Advanced Applications & Agentic Integration

  * **Objective:** Extend the system into a proactive agentic memory layer.
  * **Key Components:** Personal Knowledge Graph (PKG), local Agent API, Explainable AI (XAI) output.

#### YAML ARTIFACT: Agent API Specification (Localhost)

This YAML defines the local-only API for trusted AI agents (e.g., "Adam") to query the recall log. Access is biometrically gated by the user per session.

```yaml
# AgentApiSpec.yaml (OpenAPI 3.0 subset)
# Defines the secure, local-only API for agentic integration.
# API is bound to localhost and requires a user-authorized bearer token
# obtained via a Windows Hello ESS prompt.

openapi: 3.0.0
info:
  title: "Total Recall Agent API"
  version: "1.0.0"
  description: "Secure, local-only API for trusted AI agents to access recall data."

servers:
  - url: http://localhost:7322/v1
    description: Local Recall Service

paths:
  /query:
    post:
      summary: "Perform semantic query on recall log"
      description: "Converts natural language query to vector and returns top K matching snapshots."
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query_text:
                  type: string
                  example: "presentation slides from last week's risk meeting"
                top_k:
                  type: integer
                  default: 5
      responses:
        '200':
          description: "Successful query"
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Snapshot'
        '401':
          description: "Unauthorized. Token invalid or expired."

  /pkg_query:
    post:
      summary: "Query the Personal Knowledge Graph (PKG)"
      description: "Perform a graph query (e.g., Cypher-like) to find entities and relationships."
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                graph_query:
                  type: string
                  example: "MATCH (p:Person)-[:ATTENDED]->(m:Meeting {project:'Phoenix'}) RETURN p.name"
      responses:
        '200':
          description: "Successful query"
          content:
            application/json:
              schema:
                type: object
                #... graph result format
        '401':
          description: "Unauthorized."

  /get_rationale:
    get:
      summary: "Get XAI rationale for a conclusion"
      description: "Provides the specific snapshot IDs and text snippets that justify an AI-generated conclusion (e.g., a meeting summary)."
      security:
        - BearerAuth: []
      parameters:
        - name: conclusion_id
          in: query
          required: true
          schema:
            type: string
      responses:
        '200':
          description: "Explainable AI rationale"
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/XaiRationale'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: "Session-limited token obtained via Windows Hello prompt."
  
  schemas:
    Snapshot:
      type: object
      properties:
        snapshot_id:
          type: string
        timestamp:
          type: string
          format: date-time
        application_name:
          type: string
        window_title:
          type: string
        extracted_text:
          type: string
        similarity_score:
          type: number
    
    XaiRationale:
      type: object
      properties:
        conclusion:
          type: string
          example: "The team agreed to delay the 'Phoenix' milestone."
        evidence:
          type: array
          items:
            type: object
            properties:
              snapshot_id:
                type: string
              supporting_text:
                type: string
                example: "John: 'I don't think we're ready. Let's push Phoenix to Q4.'"
```

```
```
