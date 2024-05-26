# 📱 app-store-review-etl

[//]: # (![PyPI - Downloads]&#40;&#41;)

[//]: # (![PyPI - License]&#40;&#41;)

[//]: # (<a href="" /></a>)

*app-store-review-etl* is a Python app to fetch app reviews, generate review analysis and provide report with a Google Sheet. 

This app leverages Google Gemini AI model to summarize top liked and disliked features, using VADER, WordCloud and matplotlib library for sentiment analysis and data visualization.

Get your API keys 🔑 ready, then you could analyze app reviews 📊 easily.

## Description
As a python programmer with product management and marketing work experience in the past, I am fascinated by automation tools ⚙️ that facilitate work efficiency 🚀 and drive better customer experience 😃.

In 2024, AI productivity tool is not a dream anymore. Both OpenAI and Google provide LLM models for developers to build AI products.

Thus, the highlight of this app is that I used Google Gemini model to generate AI-wise app review analysis.
Besides, I chose Google Sheet as a database for flexibility and scalability, then you could use the output Google Sheet as data source for further data visualization with Looker or Tableau.

## Features
- 💾 Fetch App Reviews
- 💛 Sentiment Analysis
- 🧠 AI-wise Top Liked and Disliked Analysis with Google Gemini Model 
- ☁️ WordCloud and Distribution Data Graphs
- 🗂️ Get all the data and analysis in one place - Google Sheet

## Example & Result
Output Google Sheet Demo Link : 
https://docs.google.com/spreadsheets/d/1fp0-D0fspQ4W8nTSor8Oa_WFtEG1kD31JLGzABUJGdo/edit?usp=sharing

Screenshots of the output Google Sheet provide app reviews analysis from app [YouTube: Watch, Listen, Stream](https://apps.apple.com/us/app/youtube-watch-listen-stream/id544007664).

![resultImage](https://raw.githubusercontent.com/whygreedy/app-store-review-etl/main/images/demo_output_result.png)

## Quickstart

### Using the command line interface
1. Clone this repo from GitHub to your local directory
    ```bash
    git clone https://github.com/whygreedy/app-store-review-etl.git
    ```
2. Change directory to the repo folder just downloaded
    ```bash
    cd app-store-review-etl
    ```
3. Create a new project on [Google Developers Console](https://console.developers.google.com/). 
   Enable **Google Drive API** and **Google Sheets API**, and set up **OAuth consent screen**.

4. Add `credentials_gspread.json` file that includes your **OAuth Client Credential** to the repo folder

5. Add `.env` file that includes your **[Google Gemini API key](https://ai.google.dev/gemini-api)** and **the filepath to OAuth Client Credential** to the repo folder
    ```
    # your .env file
    CREDENTIALS_GSPREAD_FILE_PATH='../credentials_gspread.json'
    GEMINI_API_KEY=<your Gemini API Key>
    ```
6. Create venv
    ```bash
    virtualenv venv
    ```
7. Activate venv
    ```bash
    source venv/bin/activate
    ```
8. Change directory to the folder that includes main.py file
    ```bash
    cd app_store_review_etl
    ```
9. Execute main.py file
    ```bash
    python3 main.py -c <app_country> -n <app_name> -d <date_after> -m <ai_model>
    ```
    By default, we fetch YouTube app store reviews posted after 2024/1/1 
    ,and using Gemini 1.0 pro model. You could adjust arguments at your needs.
    
    For example, you could fetch UberEats app store reviews posted after 2023/12/1 by the following command.
    ```bash
    python3 main.py -n uber-eats-food-delivery -d 2023-12-1
    ```


### Using app-store-review-etl in a Python script
1. Create venv
    ```bash
    virtualenv venv
    ```
2. Activate venv
    ```bash
    source venv/bin/activate
    ```
3. Install from PyPI with pip
    ```bash
    pip install app-store-review-etl
    ```
4. Create a new project on [Google Developers Console](https://console.developers.google.com/). 
   Enable **Google Drive API** and **Google Sheets API**, and set up **OAuth consent screen**.

5. Add `credentials_gspread.json` file that includes your **OAuth Client Credential** to the repo folder

6. Add `.env` file that includes your **[Google Gemini API key](https://ai.google.dev/gemini-api)** and **the filepath to OAuth Client Credential** to the repo folder
    ```
    # your .env file
    CREDENTIALS_GSPREAD_FILE_PATH='../credentials_gspread.json'
    GEMINI_API_KEY=<your Gemini API Key>
    ```
   
7. Import the package and execute it with a Python Script
    ```python
    # your Python script
    from app_store_review_etl import main
    
    main.main()
    ```
