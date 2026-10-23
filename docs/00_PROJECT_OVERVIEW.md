# ECE 425/525 Project

**Team P07 | Fall 2026**
Working concept: ECE Learning and Career Advisor

## Project idea

We are building an interactive website that helps prospective and current UofA ECE students decide what to learn next. It connects their background and career interests with university courses, complementary coursework, online resources, and current job opportunities.

The experience adapts to the student. An incoming student starts with interests and possible career goals. A current student adds completed courses and projects. Returning students update their progress and receive revised recommendations.

The first release focuses on **AI/ML and embedded systems**. We can import a larger course catalog through the same pipeline, while reviewing career mappings and prerequisite rules for these two directions first.

## Core features

- A short profile covering academic standing, interests, completed coursework, and relevant experience.
- A learning roadmap showing completed work, suggested next steps, later courses, and prerequisite status.
- RAG explanations that use retrieved course and resource information, with links to the supporting sources.
- Curated online resources alongside relevant coursework.
- Available internships and jobs through one search provider, with location and opportunity filters.
- Saved profiles so students can return and update their progress.
- An expandable view showing retrieval results, similarity scores, and an embedding visualization.

Use a simple dark interface with **My Profile**, **My Roadmap**, and **Opportunities**. Keep technical details in the expandable view.

## Role of RAG

Retrieval-augmented generation is the main deep learning component. The app retrieves relevant records, passes them to a language model, and generates a personalized explanation using those records. Source links make the reasoning easier to inspect.

Prerequisite checks run separately in Python. Generated explanations use those results and cannot change them. Requirements can be satisfied, unsatisfied, or unknown.

## First build

Start with five verified courses and a small profile form. Complete the full retrieval, generation, and citation flow before expanding the interface or catalog.

A successful interaction should answer: **“Given my background and goal, what should I learn next, and why?”** Changing the goal or marking a course complete should update the relevant results.

The final release keeps job search and saved progress. Graduate advising, a complete degree audit, automatic semester scheduling, and unrestricted web research are outside the initial scope.

## Project files

| File | Contents |
| --- | --- |
| [01_RAG_DESIGN.md](01_RAG_DESIGN.md) | Retrieval, context selection, generation, and source handling |
| [02_TECHNICAL_DESIGN.md](02_TECHNICAL_DESIGN.md) | Stack, data records, module boundaries, and academic rules |
| [03_PROJECT_ROADMAP.md](03_PROJECT_ROADMAP.md) | Build order and milestones |
| [04_TESTING_AND_DEMO.md](04_TESTING_AND_DEMO.md) | Evaluation, acceptance checks, and presentation evidence |
| [05_REFERENCES.md](05_REFERENCES.md) | Course materials, technical documentation, and source-review notes |
| [06_TEAM_PROGRESS.md](06_TEAM_PROGRESS.md) | Ownership, current status, decisions, and next tasks |

## Deadlines

- **Mid-project:** November 1, 2026, at 11:59 PM MST.
- **Final presentation and submission:** December 11.

The first local prototype is implemented. The next step is to verify live model access, resolve catalog requirements, and record the first real RAG demonstration. See [team progress](06_TEAM_PROGRESS.md) for status and the repository README for launch instructions.
