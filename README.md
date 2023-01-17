<!-- PROJECT LOGO -->
<div align="center">

<h3 align="center">MMA data webscraper & data dashboard</h3>

  <p align="center">
    <br />
    <a href="https://danatomato.com/">Website</a>
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

Project includes the following:
* Python file `scrape_data_nested_list.py` which scrapes all available data from ufcstats.com and updates datasets. 
* Python file `create_datasets.py` which provides the different functions needed for the datasets.
* Files for dash website to produce a MMA stats dashboard.
* Scraped nested list `all_fight_data` and datasets needed for the website `all_f_data`, `all_f_data_pf`, `all_r_data`.

Structure of the scraped list (Should've just made it a dataframe...)
* All_fight_data = [Events] Ordered from old -> new.
* Event = [Fights, Date, Venue]
    * Fight = [Fighter1, Fighter2, Result]
        * Fighter1, Fighter2 = [Name, Total, Strikes]
            * Totals = [Total, First, Second, Third, Fourth, Fifth]
                * Total, First, etc = [Knockdowns, Takedowns, Reversals, Submission Attempted, Control Time]
                    * Takedowns = [Landed, Attempted]
            * Strikes = [Total, First, Second, Third, Fourth, Fifth]
                * Total, First, etc = [Significant Strikes, Head, Body, Leg, Distance, Clinch, Ground]
                    * Everything = [Landed, Attempted]
        * Result = [Winner, Method, Round, Time, Referee, Weight, Bonus, Details]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Pip packages

  ```sh
  pip install dash
  pip install plotly
  pip install dash_bootstrap_templates
  pip install urllib3
  pip install pandas
  pip install bs4
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Run `python scrape_data_nested_list.py` to create or update current data.

2. Run `python app.py` to start website locally.

3. Go to `http://localhost:8050/` to view website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Update scraper.
	- [ ] Create betting odds scraper.
	- [ ] Create scraper for fights outside the UFC.
	- [ ] Create scraper for judge data per round (Currently only final score available if decision.)
	- [ ] Transform scraper into dataframe instead of nested list.
- [ ] Update center graph.
	- [ ] Add option for group: Fights.
	- [ ] Add option for group: Judges.
	- [ ] Add average line.
	- [ ] Add colors for dots when 'All' is selected + certain fighters.
- [ ] Add different kinds of graphs from 'https://plotly.com/python/'.
- [ ] Create predictions graph/table.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



