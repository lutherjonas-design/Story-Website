# Story-Website (Syllable-Highlighting Reading Assistant)

### Context & Status
**Paused Prototype (Refactoring Planned)**  
I created this project as a reading helper for my girlfriend to practice German by highlighting syllable boundaries. It includes a basic story-storage system, a word-and-syllable processing database, and a React frontend. Development is currently paused while I focus on setting up my home server setup, and resuming it will require a framework refactor.

### Tech Stack
* **Backend:** Python (Django, Django REST Framework, SQLAlchemy)
* **Frontend:** React
* **Infrastructure:** Docker, Docker Compose

### Key Takeaways & Lessons Learned

* **Data Structure & Representation:** To make syllable coloring easier on the frontend, I designed a nested list data structure for processing text. For example, the string `"Hello World!"` is split and delivered to the frontend as `[["Hel", "lo"], " ", ["World"], "!"]`.
* **API Foundations:** This project served as my first deep dive into designing RESTful APIs, processing backend data specifically for frontend consumption, and understanding how data flows between decoupled systems.
* **Framework Evaluation:** Building this application gave me a solid grasp of Django's architecture. It also helped me understand its trade-offs, leading to the realization that while Django is powerful and feature-rich, a more lightweight asynchronous framework (like FastAPI) would be better suited for this specific processing workload.
