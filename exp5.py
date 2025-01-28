import streamlit as st
import mysql.connector
import pandas as pd

#SQL connection
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="pass123",
        database = 'retail_orders',
        autocommit = True)
mycursor = mydb.cursor()

@st.cache_data
def query_database(query):
    df = pd.read_sql(query,mydb)
    return df

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1e3c72, #2a5298); /* Gradient background */
        font-family: 'Roboto', sans-serif; /* Modern font */
        color: #ffffff; /* White text for contrast */
    }
    .header-title {
        color: #FFD700; /* Gold text for header */
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4); /* Subtle shadow for effect */
    }
    .question-box {
        color: #ffffff; /* White text for question box */
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        border-radius: 8px;
        background: rgba(0, 0, 0, 0.4); /* Transparent background for contrast */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2); /* Subtle shadow */
        margin: 15px 0;
    }
    .question-box:hover {
        background: rgba(255, 255, 255, 0.2); /* Hover effect */
        transition: 0.3s ease-in-out; /* Smooth transition */
    }
    </style>
""", unsafe_allow_html=True)


#st.markdown('<div class="header-title">Real-time MySQL Database Queries</div>', unsafe_allow_html=True)



r = st.sidebar.radio('Navigation',['About Project','Institutional','Self written'])

if r == "About Project":
    st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <div class="header-title">Retail Order Analysis</div>
        <div style="font-size: 32px;">🛒</div>
    </div>
    """,
    unsafe_allow_html=True,
)
    
    st.write("""
        This project demonstrates the real-time querying of a MySQL database using Streamlit. It provides:
        - **Institutional Queries**: Predefined queries related to business analytics and insights.
        - **Self-written Queries**: Custom queries for exploring the dataset.
        
        **Technologies Used**:
        - **Streamlit**: For building the interactive web application.
        - **MySQL**: For database management and querying.
        - **Pandas**: For data manipulation and presentation.

        **Features**:
        - Dynamic query selection using dropdowns.
        - Stylish presentation with a user-friendly interface.
        - Real-time fetching of query results.

        Explore the tabs on the left to get started!
    """)

elif r=='Institutional':


    st.header("Institutional queries")

    #define a dictionary that map questions
    Question =[{"Question": "1.Find top 10 highest revenue generating products", "query": '''select product_id, cast(sum(sale_price * quantity)as decimal(10,2)) as total_revenue 
    from result2 
    group by product_id
    order by total_revenue desc
    limit 10 '''},
                {"Question":"2.Find the top 5 cities with the highest profit margins","query":'''select city,
    cast(sum((sale_price - cost_price)*quantity)/sum(sale_price * quantity) as decimal(10,4)) as profit_margin 
    from result2
    group by city
    order by profit_margin desc
    limit 5'''},
                {"Question":"3.Calculate the total discount given for each category","query":'''select category,
    cast(sum(discount * sale_price* quantity)as decimal(15,2)) as total_discount 
    from result2
    group by category
    order by total_discount desc'''},
                {"Question":"4.Find the average sale price per product category","query":'''select sub_category,
    cast(avg(sale_price)as decimal(10,2)) as average_sale_price
    from result2
    group by sub_category
    order by average_sale_price desc'''},
                {"Question":"5.Find the region with the highest average sale price","query":'''select region,
    cast(avg(sale_price)as decimal(10,2)) as average_sale_price
    from result2
    group by region
    order by average_sale_price desc
    limit 1'''},
                {"Question":"6.Find the total profit per category","query":'''select category,
    cast(sum(profit * quantity)as decimal (10,2)) as total_profit
    from result2
    group by category
    order by total_profit desc'''},
                {"Question":"7.Identify the top 3 segments with the highest quantity of orders","query":'''select segment,
    sum(quantity) as total_quantity
    from  result2
    group by segment 
    order by total_quantity desc
    limit 3'''},
                {"Question":"8.Determine the average discount percentage given per region","query":'''select region,
    avg(discount_percent) as average_discount_percent
    from result2
    group by region
    order by average_discount_percent desc'''},
                {"Question":"9.Find the product category with the highest total profit","query":'''select sub_category,
    cast(sum(profit *quantity)as decimal(15,2)) as total_profit
    from result2
    group by sub_category
    order by total_profit desc
    limit 1'''},
                {"Question":"10.Calculate the total revenue generated per year","query":'''select extract(year from order_date) as order_year,
    cast(sum(sale_price * quantity)as decimal(15,2)) as total_revenue
    from result2
    group by order_year
    order by order_year'''} ]




    # create select box
    selected_question= st.selectbox("select a question", [q["Question"] for q in Question])

    #loop through questions
    for q in Question:
        if q["Question"] == selected_question:
            df = query_database(q["query"])
            
            
            st.write(df)

if r=='Self written':
    st.header("Self written queries")

    Question =[{"Question": "1.Get average discount percent for each category", "query": '''select o.category,
avg(p.discount_percent) as average_disc_percent
from  orders o 
join products p on o.order_id = p.order_id
group by o.category '''},
                {"Question":"2.Get total sales for each region ","query":'''select o.region,
cast(sum(p.sale_price * p.quantity)as decimal(15,2)) as total_sales
from orders o 
join products p on o.order_id = p.order_id
group by region'''},
                {"Question":"3.Find top 10 orders with highest profit margin ","query":'''select o.order_id,p.product_id,
cast(((p.sale_price - p.cost_price)/p.sale_price * 100)as decimal (15,2))as profit_margin
from orders o join products p on o.order_id = p.order_id
order by profit_margin desc
limit 10'''},
                {"Question":"4.Get total profit for each year","query":'''select substr(o.order_date,-4)as order_year,
cast(sum(p.profit)as decimal(15,2)) as total_profit
from orders o 
inner join products p 
on o.order_id = p.order_id
group by order_year'''},
                {"Question":"5.Find the average order value by segment ","query":'''SELECT 
  o.segment, 
  cast(AVG(p.sale_price * p.quantity) as dec(15,2)) AS avg_order_value
FROM 
  orders o
  JOIN products p ON o.order_id = p.order_id
GROUP BY 
  o.segment
ORDER BY 
  avg_order_value DESC;'''},
                {"Question":"6.Find total Sales by Ship Mode","query":'''SELECT 
  o.ship_mode, 
  cast(SUM(p.sale_price * p.quantity) as dec(15,2)) AS total_sales
FROM 
  orders o
  JOIN products p ON o.order_id = p.order_id
GROUP BY 
  o.ship_mode
ORDER BY 
  total_sales DESC;'''},
                {"Question":"7.Retrieve all orders for south region","query":'''select o.order_id,o.order_date,p.product_id,p.sub_category
from orders o 
inner join products p 
on o.order_id = p.order_id
where o.region = 'South';'''},
                {"Question":"8.Select top 5 products by profit","query":'''select p.product_id,p.sub_category,
sum(p.profit) as total_profit
from orders o 
inner join products p 
on o.order_id = p.order_id
group by p.product_id,p.sub_category
order by total_profit desc 
limit 5;'''},
                {"Question":"9.Retrieve total sales for each city from highest to lowest","query":'''select o.city,
cast(sum(p.sale_price * p.quantity)as decimal(15,2)) as total_sales 
from orders o 
inner join products p 
on o.order_id = p.order_id
group by o.city
order by total_sales desc;'''},
                {"Question":"10.Get the complete list of products and its details delivered to Florida","query":'''select p.* from orders o 
join products p 
on o.order_id = p.order_id
where o.state = 'Florida';'''} ]



    # create tabs
    selected_question= st.selectbox("select a question", [q["Question"] for q in Question])

    #loop through questions
    for q in Question:
        if q["Question"] == selected_question:
            df = query_database(q["query"])
            
            
            st.write(df)