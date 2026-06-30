# CLAUDE.md: Core Logic

This document provides a guide for AI agents developing the Core Logic for the Total Recall System.

## 1. Objective
To implement the main business logic and data models for the application.

## 2. Key Responsibilities

### 2.1. Data Models
- Define and maintain the core data models for the system, such as `Memory` and `User`.
- Ensure that these models are serializable and can be easily stored and retrieved.

### 2.2. Business Logic
- Implement the core business logic for the application, such as:
    - Adding new memories
    - Searching for memories
    - Managing user data
- Includes simulated financial engines: MarketDataService, PricingEngine, RiskEngine, CreditRatingEngine, BacktestEngine.

## 3. Neuro-Symbolic System Architecture (Signal Intelligence)

<system_graph>
  <entities>
    <entity id="Core_Engines" type="Procedural_Logic" />
    <entity id="Data_Models" type="Symbolic_Structures" />
  </entities>
  <relationships>
    <relationship source="Core_Engines" target="Data_Models" type="mutates" />
  </relationships>
  <signal_flows>
    <flow id="Engine_Execution">
      <step>Engines run procedurally to simulate financial market states.</step>
      <step>Outputs update Data_Models, which are then encoded downstream.</step>
    </flow>
  </signal_flows>
</system_graph>

## 4. Guiding Principles

- **Separation of Concerns:** The core logic should be independent of the CLI and LLM interaction modules.
- **Testability:** The code in this component should be well-tested and have high test coverage.
