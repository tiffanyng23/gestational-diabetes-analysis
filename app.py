from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np 
import plotly.express as px
import dash_bootstrap_components as dbc
import os

#DATASET
dataset= pd.read_csv("gdm_vat_data_cleaned.csv")

#categorical variables
cat_var_data = dataset[["ethnicity", "pregnancies", "type_of_delivery", "gestational_dm"]]

#continuous variables + gestational_dm 
cont_var_data = dataset[["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
"first_fasting_glucose","bmi_pregestational", "child_birth_weight", 
"gestational_age_at_birth", "current_gestational_age", "age", "gestational_dm"]]


#Initializes the app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

#creating cards
card_description = dbc.Card([
    html.Div(
        [
            html.P("BMI has been long associated with gestational diabetes. However, BMI does not differentiate between muscle, fat, and bone mass; and does not indicate fat distribution around the body. Individuals with a tendency to store visceral fat (e.g central/lower belly fat) are at a higher risk of metabolic diseases, therefore visceral fat may be a viable alternative to use to predict cardiometabolic disease risk. In the study by Rocha et al. (2020), visceral adipose tissue was measured in a cohort of 133 women in the first half of pregnancy to assess its ability to predict gestational diabetes at the end of pregnancy.",
            className="card-text"),
            html.P("Below are a series of visualizations created using the data from the study which can be used to identify differences in clinical markers between those with and without gestational diabetes (GDM). Note that for GDM status, non-GDM=0 and GDM=1. For the variable ethnicity, white=1 and non-white=0. For the variable type of delivery, vaginal=0 and cesarean section=1."),
            html.P("Reference: Rocha ADS, Bernardi JR, Matos S, et al. Maternal visceral adipose tissue during the first half of pregnancy predicts gestational diabetes at the time of delivery - a cohort study. PLoS One. 2020;15(4):e0232155. Published 2020 Apr 30. doi:10.1371/journal.pone.0232155",
            className="card-text"),
        ]),
    ], 
    body=True, color="lightgrey"
)

card_cat_var = dbc.Card([
        html.Div([
            html.Label(children='Choose a Graph:'),
            dcc.Dropdown(
                options = ["violin", "histogram"], 
                value="violin", id="violin_hist"
                ),
            html.Label(children='Choose a Categorical Variable:'),
            dcc.Dropdown(
                options=["ethnicity", "pregnancies", "type_of_delivery"], 
                value="pregnancies", id="violin_hist_var"),
            ]),
        ], 
        body=True, color="lightgrey",
    )

card_cont_var = dbc.Card([
    html.Div([
            html.Label('Choose a Graph:'),
            dcc.Dropdown(
                options=["histogram", "boxplot"], 
                value="boxplot", id="hist_box"),
            html.Label('Choose a Continuous Variable:'),
            dcc.Dropdown(
                options=["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
                        "first_fasting_glucose","bmi_pregestational", "child_birth_weight", 
                        "gestational_age_at_birth", "current_gestational_age", "age","gestational_dm"], 
                value="first_fasting_glucose", id='hist_box_var'),
        ]),
    ],
    body=True, color="lightgrey",
)

card_scatter = dbc.Card([
    html.Div([
        html.Label('Choose a Continuous X Variable:'),
        dcc.Dropdown(
            options=["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
            "first_fasting_glucose", "child_birth_weight", "bmi_pregestational",
            "gestational_age_at_birth", "current_gestational_age", "age","gestational_dm"], 
            value="bmi_pregestational", id='x1'),
        html.Label('Choose a Continuous Y Variable:'),
        dcc.Dropdown(
            options=["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
            "first_fasting_glucose", "child_birth_weight", "bmi_pregestational",
            "gestational_age_at_birth", "current_gestational_age", "age",], 
            value="first_fasting_glucose", id='y1'),
    ])
], body=True, color="lightgrey")

card_heatmap = dbc.Card([
    html.Div([
        html.Label('Select Variables:'),
        dcc.Checklist(
            options=["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
            "first_fasting_glucose", "child_birth_weight", "bmi_pregestational",
            "gestational_age_at_birth", "current_gestational_age", "age", "pregnancies"], 
            value=["mean_diastolic_bp", "mean_systolic_bp", "central_armellini_fat",
            "first_fasting_glucose", "child_birth_weight", "bmi_pregestational",
            "gestational_age_at_birth", "current_gestational_age", "age", "pregnancies"], 
            id='heatmap-checklist'),
    ])
], body=True, color="lightgrey")




#App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H1('Representation of Data from a Gestational Diabetes Study', className= "card-title"),
        html.Hr()
    ]),
    dbc.Row([
        card_description,
        html.Hr()
    ]),
    dbc.Tabs([
        dbc.Tab(label = "Visualizations of Variables", children = [
            #Violin plot
            dbc.Row([
                dbc.Col(card_cat_var, width=3),
                dbc.Col(dcc.Graph(figure={}, id= "controls-and-violin-graph"), width=9),
            ],align= "center",
            ),
            dbc.Row([
                dbc.Col(card_cont_var, width=3),
                dbc.Col(dcc.Graph(figure={}, id= "controls-and-hist-graph"), width=9)
            ], align="center"),
        ]),

        dbc.Tab(label= "Relationship Between Variables", children = [
            dbc.Row([
                dbc.Col(card_scatter, width=3),
                dbc.Col(dcc.Graph(figure={}, id= "controls-and-scatter-graph"), width=9)
            ], align="center"),
            dbc.Row([
                dbc.Col(card_heatmap, width=3),
                dbc.Col(dcc.Graph(figure={}, id= "heatmap-graph"),width=9)
            ], align="center")
        ])
    ])
])



#CALLBACKS
#adding callback for violin plot
@callback(
    Output(component_id="controls-and-violin-graph", component_property="figure"),
    Input(component_id='violin_hist', component_property="value"),
    Input(component_id='violin_hist_var', component_property="value")
)

def update_violin_box(violin_hist, violin_hist_var):
    if violin_hist == "violin":
        fig = px.violin(cat_var_data, 
                        x=violin_hist_var, 
                        color="gestational_dm", 
                        facet_col ="gestational_dm",
                        title=f"Violin Plot of {violin_hist_var}",
                        labels={"gestational_dm":"GDM Status"},
                        template="seaborn",
                        )
        fig.update_layout(xaxis_title=f"{violin_hist_var}")
    else:
        fig = px.histogram(cat_var_data, 
                        x=violin_hist_var, 
                        color="gestational_dm", 
                        facet_col="gestational_dm",
                        histnorm="probability density",
                        title=f"Histogram of {violin_hist_var}",
                        labels={"gestational_dm":"GDM Status"},
                        template="seaborn",
                        )
        fig.update_layout(xaxis_title=f"{violin_hist_var}", yaxis_title="Probability Density")
    return fig

#adding callback for histogram and boxplot
@callback(
    Output(component_id="controls-and-hist-graph", component_property="figure"),
    Input(component_id='hist_box', component_property="value"),
    Input(component_id='hist_box_var', component_property="value")
    
)

def update_hist_box(hist_box, hist_box_var):
    if hist_box == "histogram":
        fig = px.histogram(cont_var_data, 
                        x=hist_box_var, 
                        color="gestational_dm", 
                        facet_col="gestational_dm",
                        histnorm="probability density",
                        title=f"Histogram of {hist_box_var}",
                        labels={"gestational_dm":"GDM Status"},
                        template="seaborn",
                        )
        fig.update_layout(xaxis_title=f"{hist_box_var}", yaxis_title="Probability Density")
    else:
        fig = px.box(cont_var_data,
                    x=hist_box_var, 
                    color="gestational_dm", 
                    facet_col="gestational_dm",
                    title=f"Boxplot of {hist_box_var}",
                    labels={"gestational_dm":"GDM Status"},
                    template="seaborn",)
        fig.update_layout(xaxis_title=f"{hist_box_var}")
    return fig



#adding callback for scatterplot
@callback(
    Output(component_id="controls-and-scatter-graph", component_property="figure"),
    Input(component_id='x1', component_property="value"),
    Input(component_id='y1', component_property="value")
)

def update_scatter(x1, y1):
    fig = px.scatter(cont_var_data, 
                    x=x1,
                    y=y1, 
                    color="gestational_dm", 
                    title=f"Scatterplot Depicting Relationship Between {x1} and {y1}",
                    labels={"gestational_dm":"GDM Status"},
                    template="ggplot2",
                    width=900,
                    height=500,
                    )
    fig.update_layout(xaxis_title=x1, yaxis_title=y1)

    return fig


#adding callback for heatmap
@callback(
    Output(component_id="heatmap-graph", component_property="figure"),
    Input(component_id='heatmap-checklist', component_property="value")
)
def update_heatmap(variables):
    #create dynamic dataset so it only includes selected variables
    corr_data = dataset[list(variables)]
    #pearsons correlation test, to create correlation matrix for heatmap
    corr_matrix = corr_data.corr(method = "pearson")
    #heatmap
    fig = px.imshow(corr_matrix, 
                    title="Heatmap Depicting Correlation Between Variables",
                    width=900,
                    height=600,
                    template="ggplot2",
                    )

    return fig


#Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
    
