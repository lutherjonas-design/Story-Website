# Integrated Data & Web Application Core (VReiraum & Analytics)

### ⚠️ **Project Status: Paused Prototype**  
I created this project to help my girlfriend practise German reading by highlighting syllable boundaries. I partially implemented a story-storage system, a word-and-syllable database, an API, and a frontend. 

Development is currently paused while I focus on setting up a home server for the [`zero-to-scale-PI`](...) project. Resuming this app would require refactoring it to use a different framework instead of Django.

### 🛠️ **Tech Stack**
* **Backend:** Python, Django, SQLAlchemy, rest_framework
* **Frontend:** React
* **Infrastructure:** Docker, Docker-Compose

---

## Key Architectural Insights & Academic Evolution
* **Frontend Development:** Partial Interface for syllable Input, that's missing the integration to the API, as well as partialy implemented display 
* **Data representation:** Syllables are stored in nested lists to make syllable coloring easier. For example, `Hello World!` could be represented as `[["Hel", "lo"], " ", ["World"], "!"]`.
* **Backend and API:** first deeper dive into API's and there function and the usage of them. Also the understanding of Django being a mighty, but general and slow tool
