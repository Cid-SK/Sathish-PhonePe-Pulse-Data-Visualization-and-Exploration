import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
import requests
import json
from PIL import Image

#sql connection
mydb = mysql.connector.connect(host="localhost",user="root",password="sk23",database='p1')
mycursor = mydb.cursor(buffered=True)

#sql data to df
mycursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1 =mycursor.fetchall()
df_aggre_tran = pd.DataFrame(table1,columns=("State","Year","Quarter","Transaction_type","Transaction_Count","Transaction_Amount"))

mycursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2 =mycursor.fetchall()
df_aggre_user = pd.DataFrame(table2,columns=("State","Year","Quarter","Brands","Registered_Users","Percentage"))

mycursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3 = mycursor.fetchall()
df_map_tran = pd.DataFrame(table3,columns=("State","Year","Quarter","District","Transaction_Count","Transaction_Amount"))

mycursor.execute("SELECT * FROM map_user")
mydb.commit()
table4 = mycursor.fetchall()
df_map_user = pd.DataFrame(table4,columns=("State","Year","Quarter","District","Registered_Users","App_Opens"))

mycursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5 = mycursor.fetchall()
df_top_tran = pd.DataFrame(table5,columns=("State","Year","Quarter","Postalcode","Transaction_Count","Transaction_Amount"))

mycursor.execute("SELECT * FROM top_user")
mydb.commit()
table6 = mycursor.fetchall()
df_top_user = pd.DataFrame(table6,columns=("State","Year","Quarter","Postalcode","Registered_Users"))

#geo map
def india_map1():
    transm1 =df_aggre_tran.groupby("State")[["Transaction_Amount"]].sum()
    transm1.reset_index(inplace=True)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data = json.loads(response.content) 

    States_Name =[]
    for i in data["features"]:
        States_Name.append(i["properties"]["ST_NM"])

    States_Name.sort()

    india_map=px.choropleth(transm1,geojson=data,locations="State",featureidkey="properties.ST_NM",
                            color="Transaction_Amount",color_continuous_scale="ylgnbu",
                            range_color=(transm1["Transaction_Amount"].min(),transm1["Transaction_Amount"].max()),hover_name="State",
                            title="All transaction",fitbounds="locations",height=800,width=650)
    india_map.update_geos(visible=False)
    st.plotly_chart(india_map)

def india_map2():
    transm1 =df_aggre_user.groupby("State")[["Registered_Users"]].sum()
    transm1.reset_index(inplace=True)
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data = json.loads(response.content) 

    States_Name =[]
    for i in data["features"]:
        States_Name.append(i["properties"]["ST_NM"])

    States_Name.sort()

    india_map=px.choropleth(transm1,geojson=data,locations="State",featureidkey="properties.ST_NM",color="Registered_Users",
                            color_continuous_scale="ylgnbu",
                            range_color=(transm1["Registered_Users"].min(),transm1["Registered_Users"].max()),hover_name="State",
                            title="All Users",fitbounds="locations",height=800,width=650)
    india_map.update_geos(visible=False)
    st.plotly_chart(india_map)

# transaction type values
z1=df_aggre_tran[df_aggre_tran["Transaction_type"] == "Recharge & bill payments"]
z01=z1["Transaction_Amount"].sum()
z2=df_aggre_tran[df_aggre_tran["Transaction_type"] == "Peer-to-peer payments"]
z02=z2["Transaction_Amount"].sum()
z3=df_aggre_tran[df_aggre_tran["Transaction_type"] == "Merchant payments"]
z03=z3["Transaction_Amount"].sum()
z4=df_aggre_tran[df_aggre_tran["Transaction_type"] == "Financial Services"]
z04=z4["Transaction_Amount"].sum()
z5=df_aggre_tran[df_aggre_tran["Transaction_type"] == "Others"]
z05=z5["Transaction_Amount"].sum()

#transaction type pie chart
def transaction_pie1(pstate,pyear):
    ap = df_aggre_tran[df_aggre_tran["State"] == pstate]
    ap.reset_index(drop = True,inplace = True)
    ay=ap[ap["Year"]==pyear]
    bp=ay.groupby("Transaction_type")[["Transaction_Amount"]].sum()
    bp.reset_index(inplace=True)
    
    fig_pie_1 = px.pie(bp,names="Transaction_type",values="Transaction_Amount",title =f"{pstate} {pyear} Transaction Amount",hole=0.5)
    st.plotly_chart(fig_pie_1)

def transaction_pie2(pstate1,pyear1):
    ap = df_aggre_tran[df_aggre_tran["State"] == pstate1]
    ap.reset_index(drop = True,inplace = True)
    ay=ap[ap["Year"]==pyear1]
    bp=ay.groupby("Transaction_type")[["Transaction_Count"]].sum()
    bp.reset_index(inplace=True)
    
    fig_pie_1 = px.pie(bp,names="Transaction_type",values="Transaction_Count",title =f"{pstate1} {pyear1} Transaction Count",hole=0.5)
    st.plotly_chart(fig_pie_1)

#User brands pie chart
def user_pie1(pstate3,pyear3):
    ap = df_aggre_user[df_aggre_user["State"] == pstate3]
    ap.reset_index(drop = True,inplace = True)
    ay=ap[ap["Year"]==pyear3]
    bp=ay.groupby("Brands")[["Registered_Users"]].sum()
    bp.reset_index(inplace=True)

    fig_pie_1 = px.pie(bp,names="Brands",values="Registered_Users",title =f"{pstate3} {pyear3} User Count",hole=0.5)
    st.plotly_chart(fig_pie_1)

#overview of transaction
def transaction_df1(year,quarter):
    year_f = df_aggre_tran[df_aggre_tran["Year"]==year]
    year_f.reset_index(drop = True,inplace=True)
    quarter_f = year_f[year_f["Quarter"]==quarter]
    quarter_f.reset_index(drop=True,inplace=True)
    state_f=quarter_f.groupby("State")[["Transaction_Count","Transaction_Amount"]].sum()
    state_f.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col2:
        aaaaa=px.bar(state_f,x="State",y="Transaction_Amount",title=f"{year} Q{quarter} Transaction Amount",height=700,width=600)
        st.plotly_chart(aaaaa)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content) 

        States_Name =[]
        for i in data["features"]:
            States_Name.append(i["properties"]["ST_NM"])

        States_Name.sort()

        india_map=px.choropleth(state_f,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Transaction_Amount",color_continuous_scale="ylgnbu",
                                range_color=(state_f["Transaction_Amount"].min(),state_f["Transaction_Amount"].max()),hover_name="State",
                                title=f"{year} Q{quarter} Transaction Amount",fitbounds="locations",height=700,width=600)
        india_map.update_geos(visible=False)
        st.plotly_chart(india_map)

def transaction_df2(df,year,quarter):
    year_f = df[df["Year"]==year]
    year_f.reset_index(drop = True,inplace=True)
    quarter_f = year_f[year_f["Quarter"]==quarter]
    quarter_f.reset_index(drop=True,inplace=True)
    state_f=quarter_f.groupby("State")[["Transaction_Count"]].sum()
    state_f.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col2:
        aaaaa=px.bar(state_f,x="State",y="Transaction_Count",title=f"{year} Q{quarter} Transaction Count",height=700,width=600)
        st.plotly_chart(aaaaa)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content) 

        States_Name =[]
        for i in data["features"]:
            States_Name.append(i["properties"]["ST_NM"])

        States_Name.sort()

        india_map=px.choropleth(state_f,geojson=data,locations="State",featureidkey="properties.ST_NM",color="Transaction_Count",
                                color_continuous_scale="ylgnbu",
                                range_color=(state_f["Transaction_Count"].min(),state_f["Transaction_Count"].max()),hover_name="State",
                                title=f"{year} Q{quarter} Transaction Count",fitbounds="locations",height=700,width=600)
        india_map.update_geos(visible=False)
        st.plotly_chart(india_map)

#overview of users
def user_df1(df,year,quarter):
    year_f = df[df["Year"]==year]
    year_f.reset_index(drop = True,inplace=True)
    quarter_f = year_f[year_f["Quarter"]==quarter]
    quarter_f.reset_index(drop=True,inplace=True)
    state_f=quarter_f.groupby("State")[["Registered_Users"]].sum()
    state_f.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col2:
        aaaaa=px.bar(state_f,x="State",y="Registered_Users",title=f"{year} Q{quarter} User Count ",height=700)
        st.plotly_chart(aaaaa)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data = json.loads(response.content) 

        States_Name =[]
        for i in data["features"]:
            States_Name.append(i["properties"]["ST_NM"])

        States_Name.sort()

        india_map=px.choropleth(state_f,geojson=data,locations="State",featureidkey="properties.ST_NM",
                                color="Registered_Users",color_continuous_scale="ylgnbu",
                                range_color=(state_f["Registered_Users"].min(),state_f["Registered_Users"].max()),
                                hover_name="State",
                                title=f"{year} Q{quarter} User Count",fitbounds="locations",height=700,width=600)
        india_map.update_geos(visible=False)
        st.plotly_chart(india_map)

def charts(dstate1,dyear1,Quarter,dchart,ac):              
    ds=df_map_tran[df_map_tran["State"]==dstate1]
    ds.reset_index(drop = True,inplace = True)
    dy=ds[ds["Year"]==dyear1]
    dy.reset_index(drop=True,inplace=True)
    dq=dy[dy["Quarter"]==Quarter]
    if ac == "Amount":
        yaxis = "Transaction_Amount"
    elif ac == "Counts":
        yaxis = "Transaction_Count"

    coll1,coll2=st.columns([6,2])
    with coll1:
        if dchart == "Line":
            dcb=px.line(dq,x="District",y=yaxis,markers=True,title=f"{dyear1} Q{Quarter} Transaction {ac} ",height=500,width=800)
            st.plotly_chart(dcb)
        elif dchart == "Area":
            dcb=px.area(dq,x="District",y=yaxis,markers=True,title=f"{dyear1} Q{Quarter} Transaction {ac} ",height=500,width=800)
            st.plotly_chart(dcb)
        elif dchart == "Bar":
            dcb=px.bar(dq,x="District",y=yaxis,title=f"{dyear1} Q{Quarter} Transaction {ac} ",height=500,width=800)
            st.plotly_chart(dcb)

def charts2(dstate2,dyear2,Quarter,dchart,ra):              
    ds=df_map_user[df_map_user["State"]==dstate2]
    ds.reset_index(drop = True,inplace = True)
    dy=ds[ds["Year"]==dyear2]
    dy.reset_index(drop=True,inplace=True)
    dq=dy[dy["Quarter"]==Quarter]
    if ra == "Registered Users":
        yaxis2 = "Registered_Users"
    elif ra == "App opens":
        yaxis2 = "App_Opens"

    coll1,coll2=st.columns([6,2])
    with coll1:
        if dchart == "Line":
            dcb=px.line(dq,x="District",y=yaxis2,markers=True,title=f"{dyear2} Q{Quarter} {ra} ",height=500,width=800)
            st.plotly_chart(dcb)
        elif dchart == "Area":
            dcb=px.area(dq,x="District",y=yaxis2,markers=True,title=f"{dyear2} Q{Quarter} {ra} ",height=500,width=800)
            st.plotly_chart(dcb)
        elif dchart == "Bar":
            dcb=px.bar(dq,x="District",y=yaxis2,title=f"{dyear2} Q{Quarter} {ra} ",height=500,width=800)
            st.plotly_chart(dcb)

#overview of transaction
def ot1():
    col1,col2 = st.columns(2)
    with col1:
        india_map1()
    with col2:
        with st.container(border=True):
            st.header(":violet[Transactions]")
        with st.container(border=True):  
            rupee_symbol = "\u20B9"
            a = df_aggre_tran["Transaction_Amount"].sum()
            b = df_aggre_tran["Transaction_Count"].sum()
            avg = a/b
            avg_Trans = round(avg)
            total_amt = "{:,}".format(a)

            st.subheader(":blue[Total PhonePe Transactions]",divider = 'red')
            st.title(f"{rupee_symbol}{total_amt}")

            st.subheader(":blue[Avg. Transaction Value]",divider = 'red')
            st.header(f"{rupee_symbol}{avg_Trans}")
            
        with st.container(border=True):
            st.header(":blue[Categories]",divider = 'red')
            col1,col2=st.columns(2)
            with col1:
                st.subheader(":blue[Peer-to-peer payments]")
                st.subheader(":blue[Merchant payments]")
                st.subheader(":blue[Recharge & bill payments]")
                st.subheader(":blue[Financial Services]")
                st.subheader(":blue[Others]")
            with col2:
                zz1="{:,}".format(z01)
                zz2="{:,}".format(z02)
                zz3="{:,}".format(z03)
                zz4="{:,}".format(z04)
                zz5="{:,}".format(z05)
                st.subheader(f"{rupee_symbol}{zz2}")
                st.subheader(f"{rupee_symbol}{zz3}")
                st.subheader(f"{rupee_symbol}{zz1}")
                st.subheader(f"{rupee_symbol}{zz4}")
                st.subheader(f"{rupee_symbol}{zz5}")

        with st.container(border=True): 
            st.subheader(":blue[Top List]",divider='red') 
            s1=df_aggre_tran.groupby("State")[["Transaction_Amount"]].sum()
            s1.reset_index(inplace=True)
            s2=s1.sort_values(by="Transaction_Amount",ascending=False)
            s3=s2.iloc[0:10]
            d1=df_map_tran.groupby("District")[["Transaction_Amount"]].sum()
            d1.reset_index(inplace=True)
            d2=d1.sort_values(by="Transaction_Amount",ascending=False)
            d3=d2.iloc[0:10]
            p1=df_top_tran.groupby("Postalcode")[["Transaction_Amount"]].sum()
            p1.reset_index(inplace=True)
            p2=p1.sort_values(by="Transaction_Amount",ascending=False)
            p3=p2.iloc[0:10]

            c1,c2,c3,c4=st.columns([2.5,3,4,8])
            with c1: 
                a=st.button(":blue[States]")
            with c2:
                b=st.button(":blue[Districts]")    
            with c3:
                c=st.button(":blue[Postal codes]")
            if a:
                st.subheader(":blue[Top 10 States]")
                cc1,cc2,cc3=st.columns([1,8,6])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in s3["State"]:
                        st.subheader(i)
                with cc3:
                    for i in s3["Transaction_Amount"]:
                        z1=i/1000000000
                        z2=str(round(z1,2))
                        st.subheader(z2+' bn')
            elif b:
                st.subheader(":blue[Top 10 Districts]")
                cc1,cc2,cc3=st.columns([1,9,6])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in d3["District"]:
                        st.subheader(i)
                with cc3:
                    for i in d3["Transaction_Amount"]:
                        z1=i/1000000000
                        z2=str(round(z1,2))
                        st.subheader(z2+' bn')
            elif c:
                st.subheader(":blue[Top 10 Postal Codes]")
                cc1,cc2,cc3=st.columns([1,5,5])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in p3["Postalcode"]:
                        st.subheader(i)
                with cc3:
                    for i in p3["Transaction_Amount"]:
                        z1=i/1000000000
                        z2=str(round(z1,2))
                        st.subheader(z2+' bn')

#overview of users
def ou1():
    col1,col2 = st.columns(2)
    with col1:
        india_map2()
    with col2:
        with st.container(border=True):
            st.header(":violet[Users]")
        with st.container(border=True):  
            tu = df_aggre_user["Registered_Users"].sum()
            total_user="{:,}".format(tu)
            st.subheader(":blue[Registered PhonePe Users(Till Q1 2022)]",divider = 'red')
            st.title(f"{total_user}")
        with st.container(border=True):  
            st.subheader(":blue[Top List]",divider='red')
            s1=df_aggre_user.groupby("State")[["Registered_Users"]].sum()
            s1.reset_index(inplace=True)
            s2=s1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
            s3=s2.iloc[0:10]
            d1=df_map_user.groupby("District")[["Registered_Users"]].sum()
            d1.reset_index(inplace=True)
            d2=d1.sort_values(by="Registered_Users",ascending=False)
            d3=d2.iloc[0:10]
            p1=df_top_user.groupby("Postalcode")[["Registered_Users"]].sum()
            p1.reset_index(inplace=True)
            p2=p1.sort_values(by="Registered_Users",ascending=False)
            p3=p2.iloc[0:10]

            c1,c2,c3,c4=st.columns([2.5,3,4,10])
            with c1: 
                a=st.button(":blue[States]")
            with c2:
                b=st.button(":blue[Districts]")    
            with c3:
                c=st.button(":blue[Postal codes]")
            if a:
                st.subheader(":blue[Top 10 States]")
                cc1,cc2,cc3=st.columns([1,8,6])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in s3["State"]:
                        st.subheader(i)
                with cc3:
                    for i in s3["Registered_Users"]:
                        z1=i/10000000
                        z2=str(round(z1,2))
                        st.subheader(z2+' Cr')
            elif b:
                st.subheader(":blue[Top 10 Districts]")
                cc1,cc2,cc3=st.columns([1,9,6])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in d3["District"]:
                        st.subheader(i)
                with cc3:
                    for i in d3["Registered_Users"]:
                        z1=i/10000000
                        z2=str(round(z1,2))
                        st.subheader(z2+' Cr')
            elif c:
                st.subheader(":blue[Top 10 Postal Codes]")
                cc1,cc2,cc3=st.columns([1,5,5])
                with cc1:
                    for i in range(1,11):
                        st.subheader(i)
                with cc2:
                    for i in p3["Postalcode"]:
                        st.subheader(i)
                with cc3:
                    for i in p3["Registered_Users"]:
                        z1=i/100000
                        z2=str(round(z1,2))
                        st.subheader(z2+' Lac')
            
def top_tpincode(statepc,yearpc):
    ps=df_top_tran[df_top_tran["State"]==statepc]
    py=ps[ps["Year"]==yearpc]
    py1=py.groupby("Postalcode")[["Transaction_Amount"]].sum()
    py1.reset_index(inplace=True)
    pt=py1.sort_values(by="Transaction_Amount",ascending=False,ignore_index=True)
    tt=pt.iloc[0:10]
    c1,c2,c3,c4=st.columns([1,2,2.5,14])
    with c1:
        st.text("S.No")
        for i in range(1,11):
            st.text(i)
    with c2:
        st.text("Postalcode")

        for i in tt["Postalcode"]:
            st.text(i)
    with c3:
        st.text("Transaction Amount")
        for i in tt["Transaction_Amount"]:
            #st.subheader(i)
            z1=i/10000000
            z2=str(round(z1,2))
            st.text(z2+' Cr')
    with c4:
        fig = px.bar(tt,x="Postalcode",y="Transaction_Amount")
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)

def top_upincode(statepc,yearpc):
    ps=df_top_user[df_top_user["State"]==statepc]
    py=ps[ps["Year"]==yearpc]
    py1=py.groupby("Postalcode")[["Registered_Users"]].sum()
    py1.reset_index(inplace=True)
    pt=py1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
    tt=pt.iloc[0:10]
    c1,c2,c3,c4=st.columns([1,2,2.5,14])
    with c1:
        st.text("S.No")
        for i in range(1,11):
            st.text(i)
    with c2:
        st.text("Postalcode")

        for i in tt["Postalcode"]:
            st.text(i)
    with c3:
        st.text("Registered Users")
        for i in tt["Registered_Users"]:
            st.text(i)
    with c4:
        fig = px.pie(tt,names="Postalcode",values="Registered_Users")
        fig.update_xaxes(type='category')
        st.plotly_chart(fig)

#streamlit web application            
st.set_page_config(page_title="PhonePe",layout="wide")
st.title(":violet[PHONEPE PULSE]")
st.subheader("Data Visualization and Exploration")
st.markdown("<style>div.block-container{padding-top:1rem;}</style>",unsafe_allow_html=True)

tab1,tab2,tab3,tab4 = st.tabs(["#### Home","#### Overview","#### Explore Data","#### Insights"])

with tab2:
    h1,h2=st.columns(2)
    with h1:
        st.header(":blue[All India]")
    with h2:
        t1= st.radio(" ",["Transactions","Users"])
    if t1 == "Transactions":
        ot1()
    if t1 == "Users":
        ou1()

with tab3:
    st.header(":blue[Visualizing Transactions and Users by State]")
    col1,col2,col3,col4= st.columns([4,2,2,8])
    with col1:
        select =st.selectbox(' ',["Transaction","User"])
    with col2:
        if select == "Transaction":
            Year1 = st.selectbox(" ",df_aggre_tran["Year"].unique()) 
            y1 = df_aggre_tran[df_aggre_tran["Year"] == Year1]
            y1.reset_index(drop = True,inplace = True) 
            a1=y1["Quarter"].unique()
            as1=pd.Series(a1)
            as1.replace([1,2,3,4],["Q1","Q2","Q3","Q4"],inplace=True)
        elif select == "User":
            Year2= st.selectbox(" ",df_aggre_user["Year"].unique())
            y2 = df_aggre_user[df_aggre_user["Year"] == Year2]
            y2.reset_index(drop = True,inplace = True)
            a2=y2["Quarter"].unique()
            as2=pd.Series(a2)
            as2.replace([1,2,3,4],["Q1","Q2","Q3","Q4"],inplace=True)
    with col3:  
        if select == "Transaction":
            Quarter1 = st.selectbox(" ",as1)
            if Quarter1 == "Q1":
                Quarter = 1
            elif Quarter1 == "Q2":
                Quarter = 2
            elif Quarter1 == "Q3":
                Quarter = 3
            elif Quarter1 == "Q4":
                Quarter = 4
        elif select == "User":
            Quarter2 = st.selectbox(" ",as2) 
            if Quarter2 == "Q1":
                Quarter = 1
            elif Quarter2 == "Q2":
                Quarter = 2
            elif Quarter2 == "Q3":
                Quarter = 3
            elif Quarter2 == "Q4":
                Quarter = 4 
    if select == "Transaction":         
        a=st.radio(" ",["Amount","Count"])
        if a =="Amount":
            transaction_df1(Year1,Quarter)
            st.header(":blue[Transaction Amount Distribution by Categories]")
            c1,c2,c3=st.columns([4,2,8]) 
            with c1:
                pstate=st.selectbox(" ",df_aggre_tran["State"].unique(),key="pt1s")
                y1 = df_aggre_tran[df_aggre_tran["State"] == pstate]
            with c2:
                pyear=st.selectbox(" ",y1["Year"].unique(),key="pt1y")
            transaction_pie1(pstate,pyear)

        elif a=="Count":
            transaction_df2(df_aggre_tran,Year1,Quarter)
            st.header(":blue[Transaction Count Distribution by Categories]")
            c1,c2,c3=st.columns([4,2,8]) 
            with c1:
                pstate1=st.selectbox(" ",df_aggre_tran["State"].unique(),key="pt1s1")
                y1 = df_aggre_tran[df_aggre_tran["State"] == pstate1]
            with c2:
                pyear1=pstate=st.selectbox(" ",y1["Year"].unique(),key="pt1y1")
            transaction_pie2(pstate1,pyear1)
    elif select == "User":
        user_df1(df_aggre_user,Year2,Quarter)
        st.header(":blue[Users Distribution by Brands]")
        c1,c2,c3=st.columns([4,2,8]) 
        with c1:
            pstate3=st.selectbox(" ",df_aggre_user["State"].unique(),key="pt1s3")
            y1 = df_aggre_user[df_aggre_user["State"] == pstate3]
        with c2:
            pyear3=st.selectbox(" ",y1["Year"].unique(),key="pt1y3")
        user_pie1(pstate3,pyear3)
    
 
    st.header(":blue[Interactive Analysis Dashboard for Transactions and Users]")
    col1,col2,col3,col4,col5,col6=st.columns([6,2,2,2,4,4])
    with col5:
        df = st.selectbox(" ",["Transactions","Users"])
    with col1:
        if df == "Transactions":
            dstate1 = st.selectbox(" ",df_map_tran["State"].unique(),key="ds1")
            dsy1=df_map_tran[df_map_tran["State"]==dstate1]
        elif df == "Users":
            dstate2 = st.selectbox(" ",df_map_user["State"].unique(),key="ds2")
            dsy2=df_map_user[df_map_user["State"]==dstate2]
    with col3:
        if df =="Transactions":
            dyear1 = st.selectbox(" ",dsy1["Year"].unique(),key="dy1")
            dyq1=dsy1[dsy1["Year"]==dyear1]
            q1=dyq1["Quarter"].unique()
            q2=pd.Series(q1)
            q2.replace([1,2,3,4],["Q1","Q2","Q3","Q4"],inplace=True)
        elif df == "Users":
            dyear2 = st.selectbox(" ",dsy2["Year"].unique(),key="dy2")
            dyq2=dsy2[dsy2["Year"]==dyear2]
            q11=dyq2["Quarter"].unique()
            q22=pd.Series(q11)
            q22.replace([1,2,3,4],["Q1","Q2","Q3","Q4"],inplace=True)            
    with col4:
        if df == "Transactions":        
            dquarter1=st.selectbox(" ",q2,key='dq1')
            if dquarter1 == "Q1":
                Quarter = 1
            elif dquarter1 == "Q2":
                Quarter = 2
            elif dquarter1 == "Q3":
                Quarter = 3
            elif dquarter1 == "Q4":
                Quarter = 4
        elif df == "Users":
            dquarter2=st.selectbox(" ",q22,key='dq2')
            if dquarter2 == "Q1":
                Quarter = 1
            elif dquarter2 == "Q2":
                Quarter = 2
            elif dquarter2 == "Q3":
                Quarter = 3
            elif dquarter2 == "Q4":
                Quarter = 4

    with col2:
        dchart= st.selectbox(" ",["Bar","Line","Area"])
    with col6:
        if df == "Transactions":
            ac = st.selectbox(" ",["Amount","Counts"])
        elif df == "Users":
            ra = st.selectbox(" ",["Registered Users","App opens"])
    
    if df == "Transactions":
        charts(dstate1,dyear1,Quarter,dchart,ac)
    elif df =="Users":
        charts2(dstate2,dyear2,Quarter,dchart,ra)

    st.header(":blue[Top Postal Code Analysis for Transactions and Users]")
    s1,s2,s3,s4=st.columns([4,2,4,6])
    with s1:
        statepc=st.selectbox(" ",df_top_tran["State"].unique(),key="pc1")
    with s2:
        yearpc=st.selectbox(" ",df_top_tran["Year"].unique(),key="pc2")
    with s3:
        dfp=st.selectbox(" ",["Transaction","User"],key="sdfp")

    if dfp=="Transaction":
        top_tpincode(statepc,yearpc)
    elif dfp=="User":
        top_upincode(statepc,yearpc)

with tab1:
    c1,c2=st.columns([7,4])
    with c2:
        st.image(Image.open(r"D:\SK\DS\image\phonepe\phonepe2.jpg"),width=380)
    
    with c1:
        st.write(" ")
        st.write(" ")
        st.subheader(":violet[PhonePe] is a mobile payment platform using which you can transfer money using UPI, \
                recharge phone numbers, pay utility bills, etc.")
        st.subheader("PhonePe works on the Unified Payment Interface (UPI)\
                system and all you need is to feed in your bank account details and create a UPI ID.")
        
    c3,c4=st.columns([4,7])
    with c3:
        st.write(" ")
        st.write(" ")
        st.image(Image.open(r"D:\SK\DS\image\phonepe\phonepepulse.jpg"),width=480)
    with c4:
        st.markdown("## :violet[About Pulse:] ")
        st.write("#### The Indian digital payments story has truly captured the world's imagination. \
                From the largest towns to the remotest villages, there is a payments revolution being driven by\
                the penetration of mobile phones and data.")
        
        st.write("#### When PhonePe started 5 years back, we were constantly looking for definitive data sources\
                on digital payments in India.This year as we became India's largest digital payments platform with\
                46% UPI market share, we decided to demystify the what, why and how of digital payments in India.")
        
with tab4:
    st.header(":blue[Insights Dashboard: Transaction and User Analysis]")
    x1,x2=st.columns([2,14])
    with x1:
        insight=st.selectbox(" ",["Transaction","Users"],key="insight1")
    if insight=="Transaction":
        with x2:
            questions = st.selectbox(" ",("1.Top 10 States based on Transaction Amount",
                                            "2.Least 10 States based on Transaction Amount",
                                            "3.Top 10 States based on Transaction Count",
                                            "4.Least 10 States based on Transaction Count",
                                            "5.Top 10 Districts based on Transaction Amount",
                                            "6.Least 10 Districts based on Transaction Amount",
                                            "7.Top 10 Districts based on Transaction Count",
                                            "8.Least 10 Districts based on Transaction Count",
                                            "9.Top 10 PostalCode based on Transaction Amount",
                                            "10.Least 10 PostalCode based on Transaction Amount",
                                            "11.Top 10 PostalCode based on Transaction Count",
                                            "12.Least 10 PostalCode based on Transaction Count"))
        #1
        if questions == "1.Top 10 States based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_tran.groupby("State")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 States based on Transaction Amount]")
                fig=px.bar(atsq1,x="State",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #2   
        elif questions == "2.Least 10 States based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_tran.groupby("State")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 States based on Transaction Amount]")
                fig=px.bar(atsq1,x="State",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        
        #3
        elif questions == "3.Top 10 States based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_tran.groupby("State")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Count",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 States based on Transaction Count]")
                fig=px.bar(atsq1,x="State",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)

        #4
        elif questions == "4.Least 10 States based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_tran.groupby("State")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Count",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 States based on Transaction Count]")
                fig=px.bar(atsq1,x="State",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #5
        elif questions == "5.Top 10 Districts based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_tran.groupby("District")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 Districts based on Transaction Amount]")
                fig=px.bar(atsq1,x="District",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)

        #6
        elif questions == "6.Least 10 Districts based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_tran.groupby("District")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 Districts based on Transaction Amount]")
                fig=px.bar(atsq1,x="District",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)     
        #7
        elif questions == "7.Top 10 Districts based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_tran.groupby("District")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Count",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 Districts based on Transaction Count]")
                fig=px.bar(atsq1,x="District",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                            height=400,width=700)
                st.plotly_chart(fig)
        #8
        elif questions == "8.Least 10 Districts based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_tran.groupby("District")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Transaction_Count",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 Districts based on Transaction Count]")
                fig=px.bar(atsq1,x="District",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                            height=400,width=700)
                st.plotly_chart(fig)
        #9
        elif questions == "9.Top 10 PostalCode based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_tran.groupby("Postalcode")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 PostalCode based on Transaction Amount]")
                fig=px.bar(atsq1,x="Postalcode",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)
        #10
        elif questions == "10.Least 10 PostalCode based on Transaction Amount":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_tran.groupby("Postalcode")[["Transaction_Amount"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str)
                asq1=q1.sort_values(by="Transaction_Amount",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 PostalCode based on Transaction Amount]")
                fig=px.bar(atsq1,x="Postalcode",y="Transaction_Amount",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)
        #11
        elif questions == "11.Top 10 PostalCode based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_tran.groupby("Postalcode")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str)
                asq1=q1.sort_values(by="Transaction_Count",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 PostalCode based on Transaction Count]")
                fig=px.bar(atsq1,x="Postalcode",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)
        #12
        elif questions == "12.Least 10 PostalCode based on Transaction Count":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_tran.groupby("Postalcode")[["Transaction_Count"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str) 
                asq1=q1.sort_values(by="Transaction_Count",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 PostalCode based on Transaction Count]")
                fig=px.bar(atsq1,x="Postalcode",y="Transaction_Count",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)

    elif insight=="Users":
        with x2:
            questions = st.selectbox(" ",("1.Top 10 States based on Registered Users",
                                        "2.Least 10 States based on Registered Users",
                                        "3.Top 5 Brands based on Registered Users",
                                        "4.Least 5 Brands based on Registered Users",
                                        "5.Top 10 Districts based on Registered Users",
                                        "6.Least 10 Districts based on Registered Users",
                                        "7.Top 10 Districts based on App Openings",
                                        "8.Least 10 Districts based on App Openings",
                                        "9.Top 10 PostalCode based on Registered Users",
                                        "10.Least 10 PostalCode based on Registered Users"))

        #1
        if questions == "1.Top 10 States based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_user.groupby("State")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 States based on Registered Users]")
                fig=px.bar(atsq1,x="State",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #2
        elif questions == "2.Least 10 States based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_user.groupby("State")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 States based on Registered Users]")
                fig=px.bar(atsq1,x="State",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #3
        elif questions == "3.Top 5 Brands based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_user.groupby("Brands")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
                at=asq1.iloc[[0,1,2,3,5,6]]
                at.reset_index(drop=True,inplace=True)
                at.index=at.index+1
                atsq1=at.head(5)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 5 Brands based on Registered Users]")
                fig=px.bar(atsq1,x="Brands",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #4
        elif questions == "4.Least 5 Brands based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_aggre_user.groupby("Brands")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(5)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 5 Brands based on Registered Users]")
                fig=px.bar(atsq1,x="Brands",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #5
        elif questions == "5.Top 10 Districts based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_user.groupby("District")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 Districts based on Registered Users]")
                fig=px.bar(atsq1,x="District",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #6
        elif questions == "6.Least 10 Districts based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_user.groupby("District")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="Registered_Users",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 Districts based on Registered Users]")
                fig=px.bar(atsq1,x="District",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #7
        elif questions == "7.Top 10 Districts based on App Openings":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_user.groupby("District")[["App_Opens"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="App_Opens",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 Districts based on App Openings]")
                fig=px.bar(atsq1,x="District",y="App_Opens",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #8
        elif questions == "8.Least 10 Districts based on App Openings":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_map_user.groupby("District")[["App_Opens"]].sum()
                q1.reset_index(inplace=True)
                asq1=q1.sort_values(by="App_Opens",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 Districts based on App Openings]")
                fig=px.bar(atsq1,x="District",y="App_Opens",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                st.plotly_chart(fig)
        #9
        elif questions == "9.Top 10 PostalCode based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_user.groupby("Postalcode")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str)
                asq1=q1.sort_values(by="Registered_Users",ascending=False,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Top 10 PostalCode based on Registered Users]")
                fig=px.bar(atsq1,x="Postalcode",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)
        #10
        elif questions == "10.Least 10 PostalCode based on Registered Users":
            c1,c2=st.columns([2,4])
            with c1:
                st.write("  ")
                st.write("  ")
                q1=df_top_user.groupby("Postalcode")[["Registered_Users"]].sum()
                q1.reset_index(inplace=True)
                q1["Postalcode"] = q1["Postalcode"].astype(str)
                asq1=q1.sort_values(by="Registered_Users",ascending=True,ignore_index=True)
                asq1.index=asq1.index+1
                atsq1=asq1.head(10)
                st.write(atsq1)
            with c2:
                st.header(":blue[Least 10 PostalCode based on Registered Users]")
                fig=px.bar(atsq1,x="Postalcode",y="Registered_Users",color_discrete_sequence=px.colors.sequential.Jet_r,
                        height=400,width=700)
                fig.update_xaxes(type='category')
                st.plotly_chart(fig)


##############
