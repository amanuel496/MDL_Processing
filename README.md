
# Master Data Load (MDL) Processing Tool

This repository contains a Python-based tool designed to facilitate the processing and management of Master Data Load (MDL) files.

## Overview

The MDL Processing Tool enables users to:

- **Parse and Analyze MDL Files:** Efficiently read and interpret MDL files to extract and understand their contents.
- **Transform Data:** Apply necessary transformations to the data within MDL files to meet specific requirements.
- **Validate Data Integrity:** Ensure that the data within MDL files adheres to predefined standards and is free from errors.

## Features

- **Robust Parsing Capabilities:** Handles various MDL file formats and structures.
- **Data Transformation Functions:** Includes utilities for data cleaning, normalization, and restructuring.
- **Validation Mechanisms:** Implements checks to verify data consistency and integrity.

## Project Structure

- **lib/**: Contains library modules utilized by the main application.
- **test_data/**: Includes sample MDL files for testing and demonstration purposes.
- **mdl_main.py**: The primary script to execute MDL processing tasks.
- **test_mdl.py**: Comprises unit tests to validate the tool's functionality.
- **Pipfile**: Specifies the Python dependencies required for the project.
- **log4j.properties**: Configuration file for logging properties.

## Getting Started

To set up the project locally, follow these steps:

### Prerequisites

- **Python 3.6+**: Ensure that Python is installed on your system.
- **Pipenv**: Used for managing Python dependencies. Install it using pip if it's not already installed:

  ```bash
  pip install pipenv
  ```

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/amanuel496/MDL_Processing.git
   cd MDL_Processing
   ```

2. **Install Dependencies:**

   Use Pipenv to install the required packages:

   ```bash
   pipenv install
   ```

3. **Activate the Virtual Environment:**

   ```bash
   pipenv shell
   ```

### Usage

1. **Processing MDL Files:**

   Execute the main script with the desired MDL file as an argument:

   ```bash
   python mdl_main.py path/to/your_mdl_file.mdl
   ```

   Replace `path/to/your_mdl_file.mdl` with the actual path to your MDL file.

2. **Running Tests:**

   To run the unit tests:

   ```bash
   python -m unittest test_mdl.py
   ```

## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository**

2. **Create a Feature Branch:**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes:**

   ```bash
   git commit -m 'Add a meaningful message'
   ```

4. **Push to the Branch:**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

Special thanks to the open-source community and the creators of the tools and resources that made this project possible.
