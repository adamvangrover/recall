# Neuro-Symbolic `.ans` Schema

The `.ans` file is the fundamental building block of the Total Recall System's external hippocampus. Each file requires the following structure:

## YAML Frontmatter

```yaml
---
module: <string>
type: <string>
dependencies: [<list_of_strings>]
status: <string>
---
```

## System Graph XML

```xml
<system_graph>
  <entities>
    <entity id="Module_Name" type="Component_Type" />
  </entities>
  <relationships>
    <relationship source="Module_Name" target="Other_Module" type="interacts_with" />
  </relationships>
  <signal_flows>
    <flow id="Flow_Name">
      <step>Describe the interaction.</step>
    </flow>
  </signal_flows>
</system_graph>
```

## Structure
Files must also contain `## Objective`, `## Key Responsibilities`, and `## Guiding Principles` or `## Recent Memory Signals`.