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
        st.header(menu[0])
        M=st.number_input("Insert the number of components:", min_value = 2, max_value=5, value = 2, help="The number of components must belong to the interval from 2 and 5. If this does not fulfill your need, contact us.")

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
        st.subheader("Insert the parameter values below:")
        
        for i, col in M:
            Eta1s.append(st.number_input("Insert the characteristic life of the weak component (η\u2081)", min_value = 0.0, value = 3.0, help="This parameter specifies the scale parameter for the Weibull distribution, representing the defect arrival for the weaker component."))
            Beta1s.append(st.number_input("Insert the shape parameter of the weak component (β\u2082)", min_value = 1.0, max_value=5.0, value = 2.5, help="This parameter specifies the shape parameter for the Weibull distribution, representing the defect arrival for the weaker component."))
            Eta2s.append(st.number_input("Insert the characteristic life of the strong component (η\u2081)", min_value = 3.0, value = 18.0, help="This parameter specifies the scale parameter for the Weibull distribution, representing the defect arrival for the stronger component."))
            Beta2s.append(st.number_input("Insert the shape parameter of the strong component (β\u2082)", min_value = 1.0, max_value=5.0, value = 5.0, help="This parameter specifies the shape parameter for the Weibull distribution, representing the defect arrival for the stronger component."))
            ps.append(st.number_input("Insert the mixture parameter (p)", min_value = 0.0, value = 0.10, help="This parameter indicates the proportion of the weaker component within the total population of components."))
            Eta3s.append(st.number_input("Insert the characteristic life of the delay-time distribution (η\u2081)", min_value = 0.0, value = 2.0, help="This parameter defines the scale parameter for the Weibull distribution, which governs the transition from the defective to the failed state of a component."))
            Beta3s.append(st.number_input("Insert the shape parameter of the delay-time distribution (β\u2082)", min_value = 1.0, max_value=5.0, value = 2.0, help="This parameter defines the shape parameter for the Weibull distribution, which governs the transition from the defective to the failed state of a component."))
            Cis.append(st.number_input("Insert cost of inspection (C\u1da0)", value = 0.05, help="This parameter represents the inspection cost incurred."))
            Crs.append(st.number_input("Insert cost of replacement (inspections and age-based) (C\u02b3)", value = 1.0, help="This parameter represents the cost associated with preventive replacements, whether performed during inspections or when the age-based threshold is reached."))
            Cfs.append(st.number_input("Insert cost of failure (C\u1da0)", value = 10.0, help="This parameter represents the replacement cost incurred when a component fails."))
        
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
