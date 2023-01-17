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
* Python file `scrape_data_nested_list.py` which scrapes all available data from ufcstats.com. 
* Python file `create_datasets.py` which updates the different sets of datasets needed for the website.
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

### Prerequisites
* npm
  ```sh
  pip install dash
  pip install plotly
  pip install dash_bootstrap_templates
  pip install urllib3
  pip install pandas
  pip install bs4
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



