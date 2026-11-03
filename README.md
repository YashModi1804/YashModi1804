<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/identity-dark.png">
  <img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/identity-dark.gif" alt="Yash Modi — Associate Engineer at Oracle, India. The letters disperse into an open particle cloud and gather back into the name." width="1200">
</picture>

I'm **Yash Modi**, an **Associate Engineer at Oracle** and a developer from **India**. I build **full-stack software and AI integrations**, with a focus on clear workflows, independent validation, and traceable decisions.

<p>
<a href="mailto:modi.yash18042004@gmail.com"><img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/contact-email.svg" alt="Email me" height="44"></a>
<a href="https://www.linkedin.com/in/yash-modi-1804y/"><img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/contact-linkedin.svg" alt="LinkedIn" height="44"></a>
<a href="https://github.com/YashModi1804/YashModi1804/issues"><img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/contact-questions.svg" alt="Ask me a question" height="44"></a>
</p>

## Selected work

### Folio · AI invoice processing & verification

From invoice PDFs to structured records—with arithmetic checked independently of the model, source evidence for reviewers, and a history that keeps the original extraction intact.

<a href="https://github.com/YashModi1804/folio-invoice-verification#how-it-works">
  <picture>
    <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/folio-pipeline-mobile.svg">
    <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/folio-pipeline.png">
    <img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/folio-pipeline.gif" alt="Folio architecture: document intake, typed extraction, independent Decimal verification, and human review. Illustrated synthetic example: 18 line items across two pages, with a USD 125 total discrepancy." width="1200">
  </picture>
</a>

**Three decisions you can inspect in the code:**

- **Verify the output.** [Decimal arithmetic](https://github.com/YashModi1804/folio-invoice-verification/blob/main/app/domain/verify.py) checks line items and totals; missing values never silently become zero.
- **Make failure explicit.** A [database-backed worker](https://github.com/YashModi1804/folio-invoice-verification/blob/main/app/worker.py) processes persisted jobs with explicit processing and failure states.
- **Keep the evidence.** [Review decisions](https://github.com/YashModi1804/folio-invoice-verification/blob/main/app/review.py) preserve the original extraction alongside the corrected result.

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/toolkit-project-mobile.svg">
  <img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/toolkit-project.svg" alt="Folio project stack: Python, FastAPI, Pydantic, PostgreSQL and Docker. The interface uses React and TypeScript." width="840">
</picture>

**[Explore the sample walkthrough ↗](https://yashmodi1804.github.io/folio-invoice-verification/)** · **[Source code](https://github.com/YashModi1804/folio-invoice-verification)** · **[Try the live demo](https://yashmodi1804.github.io/folio-invoice-verification/launch/)**

<a href="https://yashmodi1804.github.io/folio-invoice-verification/">
  <img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/folio-review.png" alt="Actual Folio public sample console showing the HelixPoint invoice, its source page and a USD 125 mismatch held for human review. Synthetic fixture; no live AI call." width="1200">
</a>

<sub>The screenshot and walkthrough use labeled synthetic fixtures. The live demo uses a temporary free backend and may need time to wake.</sub>

<br><br>

### Scholarship workflow

<a href="https://github.com/YashModi1804/RBAC-Driven-Scholarship-Workflow-Engine">
  <img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/scholarship-workflow.svg" alt="Scholarship workflow: a React and Express portal with student and admin screens, MongoDB records, and staged verification." width="1200">
</a>

A **React / Express / MongoDB** scholarship portal with student and administrative screens and staged verification records.

**[Explore the source ↗](https://github.com/YashModi1804/RBAC-Driven-Scholarship-Workflow-Engine)** · [Frontend routes](https://github.com/YashModi1804/RBAC-Driven-Scholarship-Workflow-Engine/blob/main/frontend/src/App.js) · [Verification model](https://github.com/YashModi1804/RBAC-Driven-Scholarship-Workflow-Engine/blob/main/backend/models/scholarshipDetails.js)

## My working toolkit

<p>
<img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/toolkit-code.svg" alt="Languages and interfaces: C, C++, JavaScript, TypeScript, React, HTML and CSS." width="405">
<img src="https://raw.githubusercontent.com/YashModi1804/YashModi1804/2097a7530c36a8f57bd8f8b742573db69aca2b33/assets/toolkit-systems.svg" alt="Server, data and workflow: Node.js, Express, MongoDB, MySQL, Git, GitHub and VS Code." width="405">
</p>

<details>
  <summary>Toolkit as text</summary>

**Languages:** C, C++, JavaScript, TypeScript. **Interface:** React, HTML, CSS.
**Backend:** Node.js, Express. **Data:** MongoDB, MySQL.
**Workflow:** Git, GitHub, VS Code.

</details>

## What I'm exploring next

I'm learning **low-latency software**, **system design**, and **cloud architecture**. I'm always up for a conversation about **C++**, **Node.js**, **React**, **REST APIs**, or whatever you're building.

> In the stillness of the mind, one can find the universe!

<details>
  <summary><b>GitHub activity</b> — contributions, streaks & languages</summary>
  <br>
  <img src="./assets/activity-dark.svg?v=bronze-1" alt="GitHub activity: profile contributions and streaks over the last 365 days; public repository and star totals; language distribution across original public repositories." width="1200">

  A dated weekly snapshot from GitHub's public profile and repository data.
  Contributions are not commit counts. Streaks cover the displayed 365-day window;
  language shares measure source bytes in original public repositories, excluding HTML.

  [Snapshot & sources](./data/activity.json) · [How it updates](./design/MAINTENANCE.md)

  Original views: [Profile stats](https://github-readme-stats-salesp07.vercel.app/api?username=YashModi1804&count_private=true&show_icons=true&theme=react&rank_icon=github&border_radius=10) · [Streaks](https://github-readme-streak-stats-salesp07.vercel.app/?user=YashModi1804&count_private=true&theme=react&border_radius=10) · [Top languages](https://github-readme-stats-salesp07.vercel.app/api/top-langs/?username=YashModi1804&hide=HTML&langs_count=8&layout=compact&theme=react&border_radius=10&size_weight=0.5&count_weight=0.5&exclude_repo=github-readme-stats)

</details>

<br>

<img src="https://visitor-badge.laobi.icu/badge?page_id=YashModi1804.YashModi1804" alt="Profile visitor counter">
