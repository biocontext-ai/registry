<!--
To add a new MCP server to the list, please add a `meta.yaml` file to the `mcp_servers` directory.
-->

Name: <!-- Please add the MCP server's name -->

Description: <!-- Please add the MCP server's name -->

Please complete the following checklist before submitting your pull request:

- [ ] **Unique Identifier**: The `id` field is unique and follows the format `https://github.com/<github_user>/<repository_name>`
- [ ] **Schema Compliance**: The `meta.yaml` file fully complies with the schema defined in `schema.json`. I have run the `pre-commit` hook to confirm.
- [ ] **Repository Access**: The source code repository URL is publicly accessible
- [ ] **Documentation Access**: The documentation URL is publicly accessible
- [ ] **Biomedical Relevance**: The MCP server provides specific tools for biomedical research or clinical activities (please briefly describe)
- [ ] **Open Source License**: The server is released under one of the [OSI-approved](https://opensource.org/license) licenses listed in the schema
- [ ] **Search Discoverability**: The description and tags enable relevant search queries to find the MCP server
- [ ] **Free Academic Usage**: The services exposed through the MCP server are free for academic research
- [ ] **Non-Duplication**: This is not a fully duplicate effort of an existing BioContextAI registry MCP server (if similar to another server, please explain the unique aspects)
- [ ] **MCP Compliance**: The server properly implements the Model Context Protocol specification
- [ ] **Installation Instructions**: Clear instructions for installing and running the server are provided
- [ ] **Maintained**: The project is not abandoned
- [ ] **Functionality Testing**: All exposed tools and resources have been tested and function as expected (manual or unit tests)
