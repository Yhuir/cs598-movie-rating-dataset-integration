# Ethics and Legal Considerations for Data Acquisition

## Data Sources and Licensing

This project uses publicly available movie metadata and ratings from the following sources:

1. **The Movie Database (TMDb) Dataset**  
   - **Data Source**: [Kaggle TMDb Dataset](https://www.kaggle.com/rounakbanik/the-movies-dataset)  
   - **License**: The dataset is made publicly available on Kaggle under a **CC0 (public domain)** license for non-commercial educational use.  
   - **Ethical Use**: The data is provided without personal identifiers and does not contain sensitive or private information. It is used for educational analysis and comparison.

2. **OMDb API (Rotten Tomatoes and IMDb Ratings)**  
   - **API**: [OMDb API](https://www.omdbapi.com/)  
   - **License**: The OMDb API offers access to Rotten Tomatoes and IMDb ratings for free for non-commercial educational use, as outlined in the OMDb Terms of Service.  
   - **Rate-Limits**: The API enforces rate-limiting and requires an **API key** to access the data. Rate limits are respected to ensure ethical access and avoid overburdening the service.

3. **IMDb Datasets** (planned for future use)  
   - **Data Source**: [IMDb Datasets](https://datasets.imdbws.com/)  
   - **License**: IMDb datasets are available for educational and non-commercial use, under IMDb's terms. Data from IMDb is used solely for academic purposes and analysis.

## Data Privacy and Usage

This project does **not** use any personally identifiable information (PII). All datasets used are publicly available and contain no private user data. Data is processed and stored in compliance with the respective data providers' terms and conditions.

## Scraping and API Usage Compliance

- **OMDb API**: We use the OMDb API to retrieve Rotten Tomatoes and IMDb ratings. The API is accessed under its official terms of service, which require rate-limiting, respect for API usage limits, and educational/non-commercial use only. The rate limits are explicitly handled in the project to prevent violations.
- **Web Scraping**: No direct web scraping is done in this project. We rely on the OMDb API for accessing Rotten Tomatoes data, which eliminates the need for web scraping and ensures compliance with RT’s terms of service.

## Non-commercial Use and Educational Focus

This project is **non-commercial** and is developed as part of an educational course (CS598). The goal is to create a **reproducible, ethical workflow** for integrating publicly available movie data sources for **educational analysis** only. All data usage complies with the terms of service of the respective sources and is used in accordance with the course's non-commercial nature.

## Acknowledgments

- The TMDb dataset is provided by [TMDb](https://www.themoviedb.org/).
- IMDb data is sourced from [IMDb Datasets](https://datasets.imdbws.com/).
- Rotten Tomatoes ratings are provided by the [OMDb API](https://www.omdbapi.com/).

This document ensures that the data acquisition process is transparent, compliant, and ethical.

