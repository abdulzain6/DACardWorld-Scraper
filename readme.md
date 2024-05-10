# DACardWorld Scraper

This project is a web scraper for "https://www.dacardworld.com" using Selenium, designed to automate the extraction of data from the website. It can be deployed using Docker or run locally by installing the necessary Python dependencies.

## Features

- **Selenium-Based Scraping**: Utilizes Selenium to navigate and scrape data efficiently from DACardWorld.
- **Docker Compatibility**: Includes a Dockerfile for easy and consistent deployment.
- **Flexible Deployment**: Can be run using Docker or directly on your machine after setting up Python and necessary packages.

## Prerequisites

- Python 3.11 or higher
- Docker (optional for Docker-based deployment)

## Installation and Setup

### Local Setup

1. **Clone the repository:**

```bash
git clone https://github.com/abdulzain6/DACardWorld-Scraper.git
cd DACardWorld-Scraper
```

2. **Install the required Python packages:**

```bash
pip install -r requirements.txt
```

### Docker Setup

1. **Build the Docker container:**

```bash
docker build -t dacardworld-scraper .
```

2. **Run the scraper using Docker:**

```bash
docker run dacardworld-scraper
```

## Usage

To run the scraper:

```bash
python dac.py
```

This command will initiate the scraper to begin extracting data from DACardWorld, which will be saved or processed according to the script's configuration.

## Contributing

Contributions are welcome! Please feel free to fork this repository, make changes, and submit pull requests.