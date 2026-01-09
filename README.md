# TRACE: Total Recognition And Course Evaluation

## Project Overview

**TRACE** is a Python-based desktop application designed to help users compare Course Learning Outcomes (CLOs) from different Excel files. The tool leverages advanced natural language processing (NLP) using the `all-MiniLM-L6-v2` Sentence Transformer model to calculate semantic similarity between CLOs. This allows for a deep understanding of curriculum changes beyond simple keyword matching. 

The application is built with a PyQt5 graphical user interface and utilizes multithreading to handle large batches of CLO comparisons efficiently.

---

## Key Features

- **Semantic Similarity Analysis**: Uses the `all-MiniLM-L6-v2` transformer model to compare CLOs based on meaning.
- **Excel File Comparison**: Seamlessly compare CLOs from old and new course Excel files.
- **Interactive UI**: A modern PyQt5-based interface for easy file selection and results visualization.
- **Multithreaded Processing**: Process large datasets without freezing the UI.
- **Dynamic Thresholding**: Adjust similarity thresholds directly within the app to refine comparison results.
- **Exportable Results**: Download and save comparison reports.

---

## Project Structure

```
TRACE/
├── CLOComparisonApp/
│   ├── UI/                    # PyQt UI component definitions
│   ├── icons/                 # Application icons and assets
│   ├── tests/                 # Unit tests for core logic
│   ├── main.py                # Main entry point for the application
│   ├── models.py              # Sentence Transformer model initialization
│   ├── threads.py             # Multithreading logic for comparisons
│   ├── ui_components.py        # Custom UI widgets and layouts
│   └── utils.py               # Data extraction and utility functions
├── LICENSE                    # MIT License
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## Installation and Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AkshunChauhan/TRACE.git
   cd TRACE
   ```

2. **Set up a virtual environment (recommended)**:

   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python CLOComparisonApp/main.py
   ```

---

## Running Tests

To ensure the correctness of the extraction and comparison logic, run the included tests:

```bash
pytest CLOComparisonApp/tests/
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue for any bugs or feature requests.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Author

**Akshun Chauhan**
- GitHub: [@AkshunChauhan](https://github.com/AkshunChauhan)
