# TechScraper
A modular web scraping and data analysis tool designed to extract technical data and visualize it using Jupyter Notebooks and MongoDB.
* A GitHub Action workflow has been created to scrape the 5 latest pages of the website everyday to keep track of new articles.

## Choose Your Option

### Option A: Quick View (only observing)
If you don't want to run any code, you can see the results of the project here:

* **Data Storage:** Data is stored in a MongoDB Atlas cluster.
<img src='./assets/mongodb.png' alt='Database Screenshot' width='500'>
<img src='./assets/mongodb2.png' alt='Database Screenshot' width='500'>

* **Analysis:** Insights and graphs generated in the Jupyter Notebook.
> Comparing articles' main categories popularity
<img src='./assets/main_categories.png' alt="Comparing articles' main categories popularity" width='500'>
> Comparing articles count for GenAI models
<img src='./assets/genai.png' alt='Comparing articles count for GenAI models' width='500'>
> WordCloud for 2010
<img src='./assets/wordcloud2010.png' alt='WordCloud for 2010' width='500'>
> WordCloud for 2026
<img src='./assets/wordcloud2026.png' alt='WordCloud for 2026' width='500'>

---

### Option B: Run it locally

#### 1. Prerequisites
* [Install Docker](https://docs.docker.com/get-docker/)
* You need a MongoDB account. Youc can use your own `MONGO_URI` or ask me for the **Read-Only** access key

#### 2. Configuration
* Create a `.env` file in the root direcotry and add your connection string:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/techscraper
```

#### 3. Execution
* Run only the scrapper (lightweight):
```bash
docker-compose up scraper
```
* To run the scraper with specific parameters:
```bash
# P = number of pages to scrape, S = starting page
docker-compose run scraper --page P --start S
```
* To run the full environment (scraper + analysis notebook):
```bash
docker-compose up full
```
* Then access the Jupyter Notebook. Lokk in your terminal for a url looking like this: `http://[ip]:8888/tree?token=[token]` with `[ip]` and `[token]` being unique to you. Then open `analysis.ipynb`.

#### 4. Data Analysis


#### 5. Cleanup
When you're done don't forget to stop the containers:
* If you want to stop everything and remove the containers to save RAM/Disk space, run:
```bash
docker-compose down
```
