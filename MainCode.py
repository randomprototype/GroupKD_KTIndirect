"""
Victor Hugo Resende Lima
vhugoreslim@gmail.com

Esse código necessita dos seguintes pacotes nas respectivas versões:
Pillow==9.0.1
scipy==1.7.3
streamlit==1.5.0
click==8
"""
import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import quad #Single integral
from scipy.integrate import dblquad
from PIL import Image

def main():
    #criando 3 colunas
    col1, col2, col3= st.columns(3)
    foto = Image.open('randomen.png')
    #st.sidebar.image("randomen.png", use_column_width=True)
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    #O código abaixo centraliza e atribui cor
    st.markdown("<h2 style='text-align: center; color: #306754;'>Indirect Grouping for Hybrid Inspection/Age-Based Policies</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #F3F3F3; padding: 10px; text-align: center;">
          <p style="font-size: 20px; font-weight: bold;">Indirect and direct grouping maintenance models for an hybrid policy under the delay-time model</p>
          <p style="font-size: 15px;">By: Victor H. R. Lima & Cristiano A. V. Cavalcante</p>
        </div>
        """, unsafe_allow_html=True)

    menu = ["Cost-rate", "Information", "Website"]
    
    choice = st.sidebar.selectbox("Select here", menu)
    
    if choice == menu[0]:
        Eta1s=[]
        Beta1s=[]
        Eta2s=[]
        Beta2s=[]
        ps=[]
        Eta3s=[]
        Beta3s=[]
        Crs=[]
        Cis=[]
        Cfs=[]
        st.header(menu[0])
        if 'num_columns' not in st.session_state:
            st.session_state.num_columns = 2
        def add_column():
            st.session_state.num_columns += 1
        def remove_column():
            if st.session_state.num_columns > 1:
                st.session_state.num_columns -= 1
        
        col1, col2 = st.columns(2)

        # Botões com balões informativos, cada um em uma coluna
        with col1:
            st.button("Add Repairperson", on_click=add_column, help="You should add columns to the parameters of the repairperson as you want (each column is related to one repairperson).")
        
        with col2:
            st.button("Remove Repairperson", on_click=remove_column)

        FixedCosts=[]
        Ci=[]
        Alpha=[]
        Beta=[]
        columns = st.columns(st.session_state.num_columns)

        for i, col in enumerate(columns):
            col.write(f"**Inspector {i+1}:**") 
            FixedCosts.append(col.number_input(f"Fixed Cost (C\u02b0)", min_value=0.0, value=0.1, key=f"FixedCosts_{i}", help="This parameter defines the cost related to the hiring of the repairperson."))
            Ci.append(col.number_input(f"Inspection Cost (C\u2071)", min_value=0.0, value=0.15, key=f"Ci_{i}", help="This parameter represents the cost of conducting a single inspection by this repairperson."))
            Alpha.append(col.number_input(f"False-Positive Percentage (α)", min_value=0.0, value=0.1, key=f"Alpha_{i}", help="This parameter defines the probability that, during an inspection, the repairperson will incorrectly classify a component as defective when it is actually not."))
            Beta.append(col.number_input(f"False-Negative Percentage (ε)", min_value=0.0, value=0.05, key=f"Beta_{i}", help="This parameter defines the probability that, during an inspection, the repairperson will incorrectly classify a component as good when it is actually defective."))
        st.subheader("Insert the parameter values below:")
        
        col1, col2 = st.columns(2)
        
        st.subheader("Click on botton below to run this application:")    
        botao = st.button("Get cost-rate")
        if botao:
            st.write("---RESULT---")
            st.write("Cost-rate", 0)
            
    if choice == menu[1]:
        st.header(menu[1])
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>This app is designed to compute the cost rate and cost savings achieved through setup cost sharing in a hybrid inspection and age-based maintenance policy. We consider a multicomponent system where all components operate under Delay-Time Modeling (DTM).</h6>", unsafe_allow_html=True)
        
        st.write("<h6 style='text-align: justify; color: Blue;'>Key features:</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Defect Arrival Distributions: Each component has a defect arrival distribution that reflects a mixture of weak and strong spare parts.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Maintenance Actions: Component renovation occurs through corrective maintenance-triggered by failures- or preventive maintenance-performed during inspections when a defect is detected or when the age-based threshold is reached.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Economic Dependence: Cost savings arise from setup cost sharing when multiple actions (inspections or age-based replacements) are executed simultaneously. In such cases, only the maximum expected setup cost is incurred for the group of actions, leading to savings.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Infinite Horizon: Expected setup costs are computed over an infinite planning horizon.</h6>", unsafe_allow_html=True)
        
        st.write("<h6 style='text-align: justify; color: Blue;'>How the app works:</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Policy:</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>The last action for each component is always the age-based.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>If only one action is specified, no inspections are performed for that component.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>If two or more actions are specified, inspections occur as per the sequence provided.</h6>", unsafe_allow_html=True)

        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>User Input:</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>Specify the sequence of the moments to perform actions for each component, separated by spaces.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>Actions occurring at the same time are grouped to share setup costs.</h6>", unsafe_allow_html=True)

        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 20px;'>Cost Calculations:</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay; padding-left: 40px;'>The app computes the cost rate and cost savings for the given solution.</h6>", unsafe_allow_html=True)
        
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>By exploring dependencies among components and grouping actions effectively, the app highlights opportunities to minimize long-term maintenance costs.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>For further questions or assistance in finding the optimal solution of your problem, please contact us at:</h6>", unsafe_allow_html=True)
        
        st.write('''

v.h.r.lima@random.org.br

c.a.v.cavalcante@random.org.br

''' .format(chr(948), chr(948), chr(948), chr(948), chr(948)))       
    if choice==menu[2]:
        st.header(menu[2])
        
        st.write('''The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 
                 in order to bring together different researchers who work in the following areas: risk, maintenance a
                 nd operation modelling. Learn more about it through our website.''')
        st.markdown('[Click here to be redirected to our website](https://sites.ufpe.br/random/#page-top)',False)        
if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
