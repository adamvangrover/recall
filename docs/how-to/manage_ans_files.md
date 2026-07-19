# How to Manage `.ans` Files

`.ans` files (acting as `AGENTS.md`) represent the neuro-symbolic map for the LLM. They should be strictly maintained whenever the architecture changes.

1. **Locate the relevant `.ans` file:** The file should be in the directory associated with the codebase change.
2. **Update YAML Frontmatter:**
   - `module`: The component name.
   - `type`: E.g., `symbolic_node`.
   - `dependencies`: Relevant system boundaries.
   - `status`: E.g., `active`, `stable`, `draft`.
3. **Update the `<system_graph>` XML:** Ensure it accurately reflects any new entities or signal flows between modules.
4. **Log Recent Signals:** Add a bullet under `Recent Memory Signals` summarizing what changes the model should be aware of.