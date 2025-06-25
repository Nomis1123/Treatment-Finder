# Treatment Finder - An AI-Powered Hospital Recommender

This project is an advanced Python application that demonstrates a modern, AI-driven solution to a real-world healthcare logistics problem. It analyzes raw, unstructured patient medical data and provides a sorted list of specialized hospitals best equipped to provide treatment. The application is built with a clean, object-oriented architecture and showcases a sophisticated hybrid AI strategy for balancing performance, cost, and accuracy.

## Features

*   **Hybrid AI Analysis Engine:**
    *   Implements a smart, two-tiered strategy for classifying patient conditions.
    *   **Tier 1 (Local NLP):** Utilizes a fast, local `spaCy` model with a comprehensive, curated keyword map (`SPACY_SPECIALTY_MAP`) to instantly handle common and clearly defined medical cases.
    *   **Tier 2 (Generative AI Escalation):** For complex, rare, or ambiguously worded conditions that the local model cannot confidently resolve, the system automatically escalates the task to the powerful **Google Gemini Pro** API.
*   **Intelligent Prompt Engineering:**
    *   The Gemini API calls are controlled by a carefully engineered prompt that constrains the AI's output. It forces the model to choose from a pre-defined list of valid medical specialties, ensuring the response is always structured, predictable, and compatible with the system's hospital data.
*   **Data-Driven Hospital Matching:**
    *   Patient conditions, once classified into a standard specialty (e.g., "Cardiology", "Oncology"), are matched against a detailed, inverted map (`HOSPITAL_TO_SPECIALTIES_MAP`) of Toronto-area hospitals and their core competencies.
*   **Advanced Recommendation Sorting:**
    *   Goes beyond simple matching by allowing recommendations to be sorted by secondary metrics. The current implementation includes a `sort_hospitals_by_busyness` feature, which re-ranks the list of suitable hospitals from least busy to most busy.
*   **Robust Object-Oriented Design:**
    *   The application is architected with a clean separation of concerns, where each major component is encapsulated in its own class:
        *   `PatientDataProcessor`: Handles all loading and pre-processing of patient data.
        *   `SpecialtyAnalyzer`: The "brain" of the application, containing the hybrid AI logic.
        *   `HospitalMatcher`: Manages all hospital data and matching/sorting logic.
        *   `GeminiClient`: A dedicated client for all interactions with the external API.
*   **Secure API Key Management:**
    *   Uses a `.env` file and the `python-dotenv` library to ensure API keys are never hard-coded or committed to version control.

## Stack

-   **Language:** Python 3.10+
-   **Core Libraries:**
    -   `pandas`: For all data manipulation and CSV handling.
    -   `spacy`: For fast, local Natural Language Processing to identify keywords.
    -   `google-generativeai`: For interacting with the Gemini Pro API.
    -   `python-dotenv`: For securely managing API keys.

## Project Structure

The project is organized into a `finder` package that contains all the core logic, managed by a main `run_client.py` script.

```
Treatment-Finder/
├── Data/
│   ├── hospitalData.csv
│   └── patientData.csv
│
├── finder/
│   ├── __init__.py
│   ├── ai_funcs.py             # GeminiClient class
│   ├── analysis.py             # SpecialtyAnalyzer class
│   ├── hospital_finder.py      # HospitalFinder class (matcher)
│   └── matching_engine.py      # PatientDataHandler class (processor)
│
├── .env                      # For storing secret API keys
├── .gitignore
├── requirements.txt
└── run_client.py             # Main executable script
```

## Setup and Installation

Follow these steps to get the project running on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Nomis1123/Treatment-Finder.git
cd Treatment-Finder
```

### 2. Create and Activate a Virtual Environment

```bash
# Create the environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

Install all required Python libraries and download the necessary `spaCy` model.

```bash
# Install Python packages
pip install -r requirements.txt

# Download the English language model for spaCy
python -m spacy download en_core_web_sm
```

### 4. Configure Your API Key

The application requires a Google Gemini API key to function.

1.  In the root directory, create a file named `.env`.
2.  Add your API key to this file in the following format:
    ```
    GEMINI_KEY="your_actual_api_key_here"
    ```

## Usage

The application is run via the command line from the project's root directory.

```bash
python run_client.py
```

The script will execute the full end-to-end pipeline and print a final report to the console. The output will include:
-   Initialization logs from each component.
-   Real-time status updates indicating whether `spaCy` or `Gemini` is used for each patient.
-   A final, formatted pandas DataFrame showing the patient ID, their injury, the specialty determined by the engine, and the final list of recommended hospitals.
