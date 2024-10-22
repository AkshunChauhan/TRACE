# CLO Comparison Tool

## Project Overview

The **CLO Comparison Tool** is a Python-based desktop application that helps users compare Course Learning Outcomes (CLOs) from different Excel files. The tool uses advanced text similarity algorithms (semantic similarity and Jaccard index) to analyze and compare CLOs between existing and new course files, providing users with a clear comparison of CLO changes. This application is designed to handle large batches of CLOs efficiently using multithreading, making it ideal for institutions or organizations managing curriculum updates.

---

## Key Features

- **Excel File Comparison**: Compare CLOs from two Excel files.
- **Batch Processing**: Process large batches of CLOs in parallel using multithreading.
- **Similarity Calculation**: Uses multiple algorithms like semantic similarity and Jaccard index to compare CLOs.
- **User-Friendly Interface**: A clean and intuitive PyQt-based graphical user interface (GUI).
- **Scalable Architecture**: The codebase is organized with modular components for easy expansion.
- **Logging**: Integrated logging to track events, errors, and performance.

---

## Project Structure

```
CLO-Comparison-App/
│
├── app/
│   ├── __init__.py            # Initialize the app module
│   ├── main.py                # Main entry point for the application
│   ├── ui/
│   │   ├── __init__.py        # Initialize UI module
│   │   ├── main_window.py     # Main window UI setup
│   ├── data/
│   │   ├── clo_extractor.py   # Functions to extract and process CLO data
│   │   ├── similarity.py      # Functions to calculate similarity (semantic and Jaccard)
│   ├── utils/
│   │   ├── batch_processor.py # Functions to process CLOs in batches using threading
│   │   ├── logging_config.py  # Logging configuration and setup
├── tests/
│   ├── test_similarity.py     # Unit tests for similarity calculations
│   ├── test_clo_extractor.py  # Unit tests for CLO extraction
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Docker configuration for containerized deployment
└── README.md                  # Instructions and project overview
```

---

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AkshunChauhan/CLO-Comparison-Tool.git
   cd CLO-Comparison-App
   ```

2. **Set up a virtual environment (optional but recommended)**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python3 -m app.main
   ```

---

## Running Tests

Unit tests are included to ensure the correctness of the similarity calculations and CLO extraction logic. To run the tests, use:

```bash
pytest tests/
```

---

## Docker Setup

To run the application in a containerized environment, build the Docker image and run it:

1. **Build the Docker image**:

   ```bash
   docker build -t clo-comparison-app .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 8080:8080 clo-comparison-app
   ```

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss improvements or bug fixes.

---

## Ownership

This project is owned and developed by Akshun Chauhan. All rights reserved.
