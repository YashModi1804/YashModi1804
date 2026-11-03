# Asset sources

The toolkit layouts, profile artwork, and workflow illustrations are original
compositions for this profile. Technology logos identify the tools shown; they do
not imply endorsement by their owners or a proficiency rating.

## Technology logos

Eighteen logos are vendored from
[Devicon](https://github.com/devicons/devicon/tree/32fe1d3b3f36ad11f90ab94f7db59738139c2bf6)
at revision `32fe1d3b3f36ad11f90ab94f7db59738139c2bf6`: C, C++, JavaScript,
TypeScript, React, HTML5, CSS3, Node.js, Express, MongoDB, MySQL, Git, GitHub,
Visual Studio Code, Python, FastAPI, PostgreSQL, and Docker.
Devicon is distributed under the MIT license, copyright 2015 konpa. The complete
notice is retained in [icons/LICENSE.devicon](icons/LICENSE.devicon).

The Pydantic logo is vendored from
[Simple Icons](https://github.com/simple-icons/simple-icons/tree/90646e4bf7f3b89df6c37e65baf3e7bc759a517c)
at revision `90646e4bf7f3b89df6c37e65baf3e7bc759a517c`. Simple Icons is
distributed under CC0 1.0 Universal; the complete text is retained in
[icons/LICENSE.simple-icons](icons/LICENSE.simple-icons).

[icons/sources.json](icons/sources.json) records the exact source URL and original
byte count for each logo. The vendored files retain their original geometry.
The renderer embeds and scales that geometry, prefixes internal SVG identifiers
to prevent collisions, and places each logo beside a native text label. It does
not fetch remote images at render time. Brand names and marks remain the property
of their respective owners; the collection licenses do not grant trademark rights.

## Rebuilding the toolkit

From the repository root, run:

```sh
python3 scripts/render_toolkit.py
```

The renderer uses the Python standard library and the pinned local SVG sources.
It generates `toolkit-code.svg`, `toolkit-systems.svg`, `toolkit-project.svg`,
and `toolkit-project-mobile.svg`. The first two preserve the profile's original technology
list. The separate Folio strip identifies technologies used in that project.
