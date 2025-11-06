# BioContextAI Registry MCP Servers

[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https://biocontext.ai/registry)](https://biocontext.ai/registry)
[![Create and deploy JSON](https://github.com/biocontext-ai/registry/actions/workflows/deploy-json.yaml/badge.svg)](https://github.com/biocontext-ai/registry/actions/workflows/deploy-json.yaml)
[![Validate MCP schema](https://github.com/biocontext-ai/registry/actions/workflows/validate-schema.yaml/badge.svg)](https://github.com/biocontext-ai/registry/actions/workflows/validate-schema.yaml)

This repository maintains a curated list of MCP servers within the **BioContextAI Registry** that appear on https://biocontext.ai and contribute to the BioContextAI project.

The primary purpose is to enhance the discoverability of MCP servers for biomedical research and facilitate users in finding suitable tools. Read our paper to learn more about BioContextAI: [https://www.nature.com/articles/s41587-025-02900-9](https://www.nature.com/articles/s41587-025-02900-9).

Inclusion in this list indicates that a server meets certain baseline criteria as described below. It **does not** constitute an endorsement or suggest that a comprehensive evaluation has been conducted, nor does it account for subsequent modifications to the server.

Accepted servers will be available in the [Registry UI](https://biocontext.ai/registry), in the [Registry JSON](https://biocontext.ai/registry.json) and will be automatically posted on our [Bluesky account](https://bsky.app/profile/biocontext.ai).

**Tip:** To receive alerts about newly added MCP servers, simply use GitHub's "watch" feature for this repository.

## How to Add Your MCP Server to the List

First you might want to check whether there exists a similar MCP server in the [Registry](https://biocontext.ai/registry). If a similar project exists, you might still submit your MCP server, but we would encourage you to reach out and join forces where possible, unless technical demands or different use cases require different implementations.

To add your MCP server to the Registry, fork this repository, add a `meta.yaml` file for your MCP server to the `servers` directory and open a pull request to add it to this repository. You can use our [editor](https://biocontext.ai/registry/editor) to generate the `meta.yaml` file.

- See other entries as reference examples
- Complete specification of available fields can also be found in [`schema.json`](schema.json)
- Include the checklist from below in your pull request description and respond to all items

## Setup the repository locally

This repository comes with a pre-commit hook to ensure that `meta.yaml` files are valid. Please set it up locally to confirm that your contribution adheres to the expected schema.

```bash
uv venv
source .venv/bin/activate
uv sync
pre-commit install
```

## Qualification Requirements for Registry MCP Servers

For an MCP server to be approved as part of the BioContextAI Registry, it must meet the following requirements:

1. **Biomedical Focus**: The MCP server must have a specific application for biomedical research or clinical activities beyond basic tools (not just general coding, document search, mathematics, etc.).

2. **Free Academic Access**: The services exposed through the MCP server must be free to use for academic research purposes.

3. **Open Source License**: The code must be released under an OSI-approved open-source license as specified in the `schema.json` file.

4. **MCP Compliance**: The server must follow the Model Context Protocol specifications and properly implement the required interfaces.

5. **Documentation**: The server must have clear, comprehensive documentation explaining its functionality, installation, and usage. A well-written README is generally considered sufficient, though more complex servers may benefit from additional documentation.

6. **Public Accessibility**: Both the source code repository and documentation must be publicly accessible.

Additionally, the following are strongly encouraged (and may become mandatory in the future):

- Low-configuration setup and deployment process
- Clear usage examples
- Regular maintenance and updates
- Container availability for easy deployment
- Fully typed tools when using dynamic programming languages
- Comprehensive test suite

We provide a [MCP server cookiecutter template](https://github.com/biocontext-ai/mcp-server-cookiecutter) to help you get started. You can use it to generate a new MCP server by running:

```bash
uvx cookiecutter https://github.com/biocontext-ai/mcp-server-cookiecutter.git
```

Just follow the instructions to fill in the details of your MCP server.

## MCP Server Submission Checklist

Please complete the following checklist in your pull request description. This checklist should be included automatically when opening new PRs.

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

## Display the Registry Badge

Once your MCP server is part of the Registry, showcase it by adding this badge to your README and documentation:

```markdown
[![BioContextAI - Registry](https://img.shields.io/badge/Registry-package?style=flat&label=BioContextAI&labelColor=%23fff&color=%233555a1&link=https://biocontext.ai/registry)](https://biocontext.ai/registry)
```

This badge helps users identify your server as part of the official BioContextAI Registry.

## Spread the Word

Help grow the Registry by:

- Announcing your participation on social media
- Publishing a blog post about your MCP server integration
- Presenting at conferences and workshops
- Encouraging collaborators to explore the BioContextAI Registry
- Citing the BioContextAI project in your publications

## Citation

If our work is useful to your research, please cite it as below. Please also acknowledge the MCP servers that you end up using.

```bibtex
@article{BioContext_AI_Kuehl_Schaub_2025,
  title={BioContextAI is a community hub for agentic biomedical systems},
  url={http://dx.doi.org/10.1038/s41587-025-02900-9},
  urldate = {2025-11-06},
  doi={10.1038/s41587-025-02900-9},
  year = {2025},
  month = nov,
  journal={Nature Biotechnology},
  publisher={Springer Science and Business Media LLC},
  author={Kuehl, Malte and Schaub, Darius P. and Carli, Francesco and Heumos, Lukas and Hellmig, Malte and Fernández-Zapata, Camila and Kaiser, Nico and Schaul, Jonathan and Kulaga, Anton and Usanov, Nikolay and Koutrouli, Mikaela and Ergen, Can and Palla, Giovanni and Krebs, Christian F. and Panzer, Ulf and Bonn, Stefan and Lobentanzer, Sebastian and Saez-Rodriguez, Julio and Puelles, Victor G.},
  year={2025},
  month=nov,
  language={en},
}
```
