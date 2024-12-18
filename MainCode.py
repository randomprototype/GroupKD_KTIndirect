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

def JointCost_RateComputation(Solutions,Solution,Ordering):
    
    def SingleCostRateComputation(Component,Actions,K,delta,T):
        ############Defect arrival component 1#####################################
        def f01(x):
            return (Beta1/Eta1)*((x/Eta1)**(Beta1-1))*np.exp(-(x/Eta1)**Beta1)
        ############Defect arrival component 2#####################################
        def f02(x):#
            return (Beta2/Eta2)*((x/Eta2)**(Beta2-1))*np.exp(-(x/Eta2)**Beta2)
        ###########Mixture for defect arrival######################################
        def fx(x):
            return (p*f01(x))+((1-p)*f02(x))
        ##########Delay-time distribution##########################################
        def fh(h):
            return (Beta3/Eta3)*((h/Eta3)**(Beta3-1))*np.exp(-(h/Eta3)**Beta3)
        ##########Cumulative for defect arrival####################################
        def Fx(x):
            return (p*(1-np.exp(-(x/Eta1)**Beta1)))+((1-p)*(1-np.exp(-(x/Eta2)**Beta2)))
        #########Reliability function for defect arrival###########################
        def Rx(x):
            return 1-Fx(x)
        ##########Cumulative function delay-time###################################
        def Fh(h):
            return 1-np.exp(-(h/Eta3)**Beta3)
        ##########Reliability function delay-time##################################
        def Rh(h):
            return np.exp(-(h/Eta3)**Beta3)
        
        if isinstance(delta, np.ndarray):
            delta=delta.tolist()
        delta.insert(0,0)
        ###########################################################################
        Eta1=Eta1s[Component]
        Eta2=Eta2s[Component]
        Beta1=Beta1s[Component]
        Beta2=Beta2s[Component]
        Eta3=Eta3s[Component]
        Beta3=Beta3s[Component]
        p=ps[Component]
        Ci=Cis[Component]
        Cr=Crs[Component]
        Cf=Cfs[Component]
        ############Scenario 1: Defect arrival and failure between inspections#####
        def C1():
            Setup=[0]*len(Actions)
            PROB1=0
            EC1=0
            EL1=0
            for i in range(0, K):
                PROB1+=dblquad(lambda h, x: fx(x)*fh(h), delta[i], (delta[i+1]),0,lambda x:(delta[i+1])-x)[0]
                EL1+=dblquad(lambda h, x: (x+h)*fx(x)*fh(h), delta[i], (delta[i+1]),0,lambda x:(delta[i+1])-x)[0]
                EC1+=(i*(Ci+Si)+Cf+Sr)*dblquad(lambda h, x: fx(x)*fh(h), delta[i], (delta[i+1]),0,lambda x:(delta[i+1])-x)[0]
                for j in range(0,len(Actions),1):
                    if (i>Actions[j]):
                        Setup[j]+=Si*dblquad(lambda h, x: fx(x)*fh(h), delta[i], (delta[i+1]),0,lambda x:(delta[i+1])-x)[0]
            return PROB1,EC1,EL1,Setup
        
        ############Scenario 2: Defect arrival and surviving until next inspection without error at inspection####
        def C2():
            Setup=[0]*len(Actions)
            PROB2=0
            EC2=0
            EL2=0
            for i in range(0, K):
                PROB2+=quad(lambda x: fx(x)*(1-Fh((delta[i+1])-x)),delta[i], (delta[i+1]))[0]
                EC2+=((i+1)*(Ci+Si)+Cr+Sr)*quad(lambda x: fx(x)*(1-Fh((delta[i+1])-x)),delta[i], (delta[i+1]))[0]
                EL2+=(delta[i+1])*quad(lambda x: fx(x)*(1-Fh((delta[i+1])-x)),delta[i], (delta[i+1]))[0]
                for j in range(0,len(Actions),1):
                    if (i>=Actions[j]):
                        if (i==Actions[j]):
                            Setup[j]+=(Si+Sr)*quad(lambda x: fx(x)*(1-Fh((delta[i+1])-x)),delta[i], (delta[i+1]))[0]
                        else:
                            Setup[j]+=Si*quad(lambda x: fx(x)*(1-Fh((delta[i+1])-x)),delta[i], (delta[i+1]))[0]
            return PROB2,EC2,EL2,Setup
        
        ##########Scenario 3: Defect arrival after inspections and failure#########
        def C3():
            Setup=[0]*len(Actions)
            PROB3=dblquad(lambda h, x: fx(x)*fh(h), delta[K], T,0,lambda x:T-x)[0]
            EC3=(K*(Ci+Si)+Cf+Sr)*PROB3
            EL3=dblquad(lambda h, x: (x+h)*fx(x)*fh(h), delta[K], T,0,lambda x:T-x)[0]
            for j in range(0,len(Actions),1):
                if (Actions[j]<K): #If it is an inspection
                    Setup[j]+=Si*dblquad(lambda h, x: fx(x)*fh(h), delta[K], T,0,lambda x:T-x)[0]
            return PROB3,EC3,EL3,Setup
        
        ###########Scenario 4: Defect arrival after inspections and preventive at T####
        def C4():
            Setup=[0]*len(Actions)
            PROB4=quad(lambda x: fx(x)*(1-Fh(T-x)),delta[K],T)[0]
            EC4=(K*(Ci+Si)+Cr+Sr)*PROB4
            EL4=T*PROB4
            for j in range(0,len(Actions),1):
                if (Actions[j]==K):
                    Setup[j]+=Sr*quad(lambda x: fx(x)*(1-Fh(T-x)),delta[K],T)[0]
                else:
                    Setup[j]+=Si*quad(lambda x: fx(x)*(1-Fh(T-x)),delta[K],T)[0]
            return PROB4,EC4,EL4,Setup
        
        ##########Scenario 5: No defect arrival####################################
        def C5():
            Setup=[0]*len(Actions)
            PROB5=Rx(T)
            EC5=(K*(Ci+Si)+Cr+Sr)*PROB5
            EL5=T*PROB5
            for j in range(0,len(Actions),1):
                if (Actions[j]==K):
                    Setup[j]+=Sr*Rx(T)
                else:
                    Setup[j]+=Si*Rx(T)
            return PROB5,EC5,EL5,Setup
        ###########################################################################
        C1=C1()
        C2=C2()
        C3=C3()
        C4=C4()
        C5=C5()
        ########Defining cost and life based on previous scenarios#################
        TOTAL_EC=C1[1]+C2[1]+C3[1]+C4[1]+C5[1]
        TOTAL_EL=C1[2]+C2[2]+C3[2]+C4[2]+C5[2]
        Setup=[sum(values) for values in zip(C1[3],C2[3],C3[3],C4[3],C5[3])]
        for i in range(0,len(Setup),1):
            Setup[i]/=TOTAL_EL
        return TOTAL_EC/TOTAL_EL,Setup
    
    Setups=[]
    CRs=0
    Savings=0
    for i in range(0,len(Solutions),1):
        Actions=[]
        for j in range(0,len(Solutions[i]),1):
            Actions.append(j)
        CR,Stps=SingleCostRateComputation(i, Actions, len(Solutions[i])-1, Solutions[i][:-1], Solutions[i][-1])
        CRs+=CR
        Setups.append(Stps)
    for i in range(0,len(Solution),1):
        if (len(Solution[i])>1):
            Costs=[]
            for j in range(0,len(Solution[i]),1):
                Costs.append(Setups[Ordering[Solution[i][j]][0]][Ordering[Solution[i][j]][1]])
            for j in range(0,len(Costs),1):
                if (max(Costs)!=Costs[j]):
                    Savings+=Costs[j]
    return CRs,Savings

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
        if 'num_columns' not in st.session_state:
            st.session_state.num_columns = 2
        def add_column():
            st.session_state.num_columns += 1
        def remove_column():
            if st.session_state.num_columns > 2:
                st.session_state.num_columns -= 1

        st.subheader("Insert the parameter values below:")

        Si=st.number_input("Insert the setup cost for an inspection", min_value = 0.0, value = 0.07, help="This parameter specifies the common cost for all components when one or more inspections are carried out.")
        Sr=st.number_input("Insert the setup cost for an replacement", min_value = 0.0, value = 0.7, help="This parameter specifies the common cost for all components when one or more replacements are carried out (preventively or correctively).")
        
        col1, col2 = st.columns(2)

        with col1:
            st.button("Add Component", on_click=add_column, help="You should add columns to the parameters of the repairperson as you want (each column is related to one repairperson).")
        with col2:
            st.button("Remove Component", on_click=remove_column)

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
        Solutions=[]
        columns = st.columns(st.session_state.num_columns)

        for i, col in enumerate(columns):
            col.write(f"**Component {i+1}:**")
            Eta1s.append(col.number_input(f"\u03B7¹", min_value=0.0, value=3.0, key=f"Eta1_{i}", help="This parameter represents the characteristic life of the defect arrival for weak component i."))
            Beta1s.append(col.number_input(f"\u03B2¹", min_value=1.0, max_value=5.0, value=3.0, key=f"Beta1_{i}", help="This parameter represents the shape parameter of the defect arrival for weak component i."))
            Eta2s.append(col.number_input(f"\u03B7²", min_value=0.0, value=18.0, key=f"Eta2_{i}", help="This parameter represents the characteristic life of the defect arrival for strong component i."))
            Beta2s.append(col.number_input(f"\u03B2²", min_value=1.0, max_value=5.0, value=3.0, key=f"Beta2_{i}", help="This parameter represents the shape parameter of the defect arrival for strong component i."))
            ps.append(col.number_input(f"p", min_value=0.0, max_value=1.0, value=0.1, key=f"p_{i}", help="This parameter represents the mixture between weak and strong spare parts for component i."))
            Eta3s.append(col.number_input(f"\u03B7³", min_value=0.0, value=2.0, key=f"Eta3_{i}", help="This parameter represents the characteristic life of the delay-time for component i."))
            Beta3s.append(col.number_input(f"\u03B2³", min_value=1.0, max_value=5.0, value=3.0, key=f"Beta3_{i}", help="This parameter represents the shape parameter of the delay-time for component i."))
            Cis.append(col.number_input(f"Inspection Cost", min_value=0.0, value=0.05, key=f"C^I_{i}", help="This parameter represents the cost of conducting an inspection on component i."))
            Crs.append(col.number_input(f"Replacement Cost", min_value=0.0, value=1.0, key=f"C^R_{i}", help="This parameter represents the cost of conducting a replacement (during inspection or at the age-based action) on component i."))
            Cfs.append(col.number_input(f"Failure Cost", min_value=0.0, value=10.0, key=f"C^F_{i}", help="This parameter represents the cost of conducting a replacement during the failure on component i."))
            moments_input=col.text_input(f"Insert moments for component {i+1}:", key=f"moments_{i}", help="Enter the moments of actions, with at least one moment of action, according to the characteristics of the policy.")    
            if moments_input:
                moments_list = [float(x.strip()) for x in moments_input.split(' ')]
                Solutions.append(moments_list)
        
        st.subheader("Click on botton below to run this application:")    
        botao = st.button("Get cost-rate and cost savings")
        if botao:
            Ordering=[]
            for i in range(0,len(Solutions),1):
                for j in range(0,len(Solutions[i]),1):
                    Ordering.append((i,j))
            
            SolutionsFlat=[item for sublist in Solutions for item in sublist]
            Index=[]
            for i in range(0,len(Ordering),1):
                Index.append(i)
            
            Solution=[]
            i=0
            while (i<len(SolutionsFlat)):
                Group=[Index[i]]
                j=i+1
                while (j<len(SolutionsFlat)):
                    if (SolutionsFlat[j]==SolutionsFlat[i]):
                        Group.append(Index[j])
                        Index.pop(j)
                        SolutionsFlat.pop(j)
                    else:
                        j+=1
                Solution.append(Group)
                i+=1
                
            CostRates,Savs=JointCost_RateComputation(Solutions, Solution, Ordering)
            Savs=(Savs/CostRates)*100
            st.write("---RESULT---")
            st.write("Cost-rate", CostRates, "cost saving", Ordering,"%")
            
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
