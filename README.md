# Customer-revenue-analysis
#### Overview
This project analyzes customer behavior and revenue patterns in an e-commerce setting to identify key drivers of customer value and retention.
It combines data cleaning, feature engineering, exploratory analysis, and an interactive dashboard to generate actionable business insights.

#### Objectives
* Identify high-value customers and spending patterns
* Analyze the impact of membership tiers on revenue
* Define and evaluate customer churn risk
* Understand the relationship between satisfaction and spending
* Provide actionable business recommendations
#### Tech Stack
* **Python:** Pandas, NumPy
* **Visualization:** Matplotlib, Streamlit
* **Data Handling:** CSV / SQL-ready structure

#### Key Insights 
* Data cleaning and preprocessing pipeline
* Feature engineering:

  * Customer segmentation (Low / Medium / High spend)
  * Churn risk classification (Low / Medium / High)
  * Average spend per item
* Interactive Streamlit dashboard with filters
* Business-focused analysis and recommendations
#### Business Recommendations
* **Membership tier is a strong revenue driver:**
  Gold members spend nearly **3x more** than Bronze members

* **Churn risk strongly impacts revenue:**
  High-risk customers spend significantly less (~595 vs ~969 average spend)

* **Customer satisfaction correlates with value:**
  High-value customers are consistently satisfied, while low-value customers show higher dissatisfaction

* **Customer behavior is segmented:**
  A significant portion of customers fall into high churn-risk, indicating retention opportunities

#### Business Recommendations

* **Targeted Membership Upgrades:**
  Encourage high-spending Silver customers to upgrade to Gold

* **Retention Campaigns:**
  Focus on high churn-risk customers with personalized offers or engagement strategies

* **Improve Customer Satisfaction:**
  Address dissatisfaction among low-value customers to increase lifetime value

* **Early Warning System:**
  Monitor medium-risk customers to prevent future churn

#### Dashboard

The project includes an interactive dashboard built using Streamlit to explore:

* Revenue metrics
* Churn distribution
* Membership performance
* Customer satisfaction patterns


#### Future Improvements

* Add predictive models for churn and customer lifetime value
* Incorporate time-series data for trend analysis
* Deploy the dashboard online for public access
