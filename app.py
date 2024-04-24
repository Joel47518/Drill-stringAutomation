import streamlit as st
from specifications import specification
from Tracjectory import trajectory
import numpy as np
import matplotlib.pyplot as plt
from Trajectory import build_and_hold, build_hold_and_drop


def index(diameter_list, choice):
    count = 1
    for indx in diameter_list:
        if choice == indx:
            break
        count += 1
    choice = count
    return choice


def drill_collar_length(nominal_weight, WOB=50000.0, BF=0.8):
    return WOB / (0.85 * BF * nominal_weight)


# Plot functions
def well_trajectory_3D(EAST, NORTH, VERT):
    ax = plt.axes(projection='3d')
    x = tuple(EAST)
    y = tuple(NORTH)
    z = tuple(VERT)
    ax.invert_zaxis()
    plt.title(" WELL TRAJECTORY ")
    ax.set_zlabel(" DEPTH  ft")
    plt.xlabel(" EAST  m ")
    plt.ylabel(" NORTH m ")
    ax.plot3D(x, y, z, 'b')


def well_trajectory_2D(EAST, VERT):
    plt.figure(2)
    plt.title(" WELL TRAJECTORY ")
    plt.xlabel(" EAST  m ")
    plt.ylabel(" DEPTH ft ")
    plt.plot(EAST, VERT)
    plt.gca().invert_yaxis()


def collapse_pressure(coll_plot):
    plt.figure(3)
    coll_plotx = [1, 1, 2, 2, 3, 3]
    plt.ylabel(" MAX  COLLAPSE PRESSURES   psi ")
    plt.plot([1, 4], [coll_plot[6], coll_plot[6]], color='red', label='Simulated \n Collapse pressure')
    plt.legend()
    plt.scatter(coll_plotx[:2], coll_plot[:2])
    plt.text(x=coll_plotx[0], y=coll_plot[0], s="  Sel Grade D")
    plt.text(x=coll_plotx[1], y=coll_plot[1], s="  Sel Grade E")
    plt.scatter(coll_plotx[2:4], coll_plot[2:4])
    plt.text(x=coll_plotx[2], y=coll_plot[2], s="  Alt_1 Grade D")
    plt.text(x=coll_plotx[3], y=coll_plot[3], s="  Alt_1 Grade E")
    plt.scatter(coll_plotx[4:6], coll_plot[4:6])
    plt.text(x=coll_plotx[4], y=coll_plot[4], s="  Alt_2Grade D")
    plt.text(x=coll_plotx[5], y=coll_plot[5], s="  Alt_2 Grade E")


def tensile_loading_sel(DSys_Load, ESys_Load, Load):
    plt.figure(4)

    plt.ylabel("   LOADS  lb ")
    plt.xlabel(" CATEGORY OF LOAD ")
    plt.plot([1, 4], [DSys_Load[0], DSys_Load[0]], color='red', label='Grade D')
    plt.plot([1, 4], [ESys_Load[0], ESys_Load[0]], color='green', label='Grade E')
    plt.legend()
    plt.scatter(1, Load[0])
    plt.text(x=1, y=Load[0], s="  Total Load lb")
    plt.scatter(3, Load[1])
    plt.text(x=3, y=Load[1], s="  Load with S.F lb")
    plt.scatter(2, Load[2])
    plt.text(x=2, y=Load[2], s="  Max Allow_Load lb")


def tensile_loading_alt(DSys_Load, ESys_Load, Load):
    plt.figure(5)
    a1 = plt.subplot(1, 2, 1)
    plt.title(" TENSILE LOADING OF ALTERNATIVE 1   ")
    plt.ylabel("   LOADS  lb ")
    plt.xlabel(" CATEGORY OF LOAD ")
    plt.plot([1, 4], [DSys_Load[1], DSys_Load[1]], color='red', label='Grade D')
    plt.plot([1, 4], [ESys_Load[1], ESys_Load[1]], color='green', label='Grade E')
    plt.legend(loc="upper left")

    plt.scatter(1, Load[3])
    plt.text(x=1, y=Load[3], s="  Total Load lb")
    plt.scatter(3, Load[4])
    plt.text(x=3, y=Load[4], s="  Load with S.F lb")
    plt.scatter(2, Load[5])
    plt.text(x=2, y=Load[5], s="  Max Allow_Load lb")

    a2 = plt.subplot(1, 2, 2)
    plt.title(" TENSILE LOADING OF ALTERNATIVE 2  ")
    plt.ylabel("   LOADS  lb ")
    plt.xlabel(" CATEGORY OF LOAD ")
    plt.plot([1, 4], [DSys_Load[2], DSys_Load[2]], color='red', label='Grade D')
    plt.plot([1, 4], [ESys_Load[2], ESys_Load[2]], color='green', label='Grade E')
    plt.legend(loc="upper left")

    plt.scatter(1, Load[6])
    plt.text(x=1, y=Load[6], s="  Total Load lb")
    plt.scatter(3, Load[7])
    plt.text(x=3, y=Load[7], s="  Load with S.F lb")
    plt.scatter(2, Load[8])
    plt.text(x=2, y=Load[8], s="  Max Allow_Load lb")


# Create a sidebar
st.sidebar.title('Input Options')

options = st.sidebar.multiselect('Select well trajectory parameters', ['KOP', 'Build-up rate', 'Horizontal displacement', 'Drop-off rate', 'TVD at end of drop', 'Final inclination'])

Build_Hold = None
for items in options:
    if items == "Drop-off rate": # TODO improve logic for choosing s profile
        Build_Hold = False
    elif items == "Build-up rate":
        Build_Hold = True
        # elif len(items) == 1: # TODO handle not selecting enough params
        #     st.write("Parameters you have selected is not enough")

if Build_Hold:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        northings = st.number_input('northing', value=None, step=None)
        eastings = st.number_input('easting', value=None)
        tvd_target = st.number_input('TVD', value=None)
    with col2:
        kop = st.number_input('KOP', value=None)
        bur = st.number_input('Build-up rate', value=None) # can't take decimals
    if northings == None or eastings == None or tvd_target == None:
        st.error("Please enter non-zero values for well trajectory parameters.")
        total_MD = None
    else:
        HD, TVD, total_MD = build_and_hold(bur_=bur, kop_=kop, northings=northings, eastings=eastings, tvd_target_=tvd_target)
        plt.plot(HD, TVD)
        plt.gca().invert_yaxis()
        st.pyplot() # Try and reduce size of the graph

if Build_Hold == False:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        northings = st.number_input('northing', value=None, step=None)
        eastings = st.number_input('easting', value=None)
        tvd_target = st.number_input('TVD', value=None)
        tvd_eod = st.number_input('TVD drop', value=None)
        kop = st.number_input('KOP', value=None)
    with col2:
        bur = st.number_input('Build-up rate', value=None)
        dor = st.number_input('Drop-off rate', value=None)
        hd = st.number_input('Horiz. Displacement', value=None)
        a2 = st.number_input('Final inclination', value=None) # final inclination

    if northings == None or eastings == None or tvd_target == None:
        st.error("Please enter non-zero values for well trajectory parameters.")
        total_MD = None
    else:
        HD, TVD, total_MD = build_hold_and_drop(tvd_target_=tvd_target, kop_=kop, bur_=bur, tvd_eod_=tvd_eod, dor_=dor, a2_=a2, hd_=hd)
        plt.plot(HD, TVD)
        plt.gca().invert_yaxis()
        st.pyplot()

st.sidebar.divider()

# Select box input
brand = st.sidebar.selectbox('Brand selection', ["new pipe", 'premium', 'class 2'])

st.sidebar.divider()

# header for pipe column
st.sidebar.markdown('<h3 style="text-align: center;">Pipe Properties</h3>', unsafe_allow_html=True)

# using radio instead of checkbox
dp_diameter_list = [(4.0, 3.476), (4.0, 3.340), (4.5, 3.826), (4.5, 3.640), (5.0, 4.408), (5.0, 4.276), (5.5, 4.778), (5.5, 4.670), (6.625, 5.965)]
if brand == 'new pipe':
    choice_1 = st.sidebar.radio('(Outer diameter and Inn', dp_diameter_list)
elif brand == 'premium':
    choice_1 = st.sidebar.radio('(Outer diameter and Inn', dp_diameter_list)
else:
    choice_1 = st.sidebar.radio('(Outer diameter and Inn', dp_diameter_list)

if Build_Hold == None:
    st.warning("Select the appropriate well trajectory parameters")
else:
    if total_MD == None:
        pass
    else:
        # Getting the choice as numbers so logic doesn't change
        # creating an object of the specification class
        mySpec = specification()
        choice_1 = index(diameter_list=dp_diameter_list, choice=choice_1)
        # Alternative 1
        if choice_1 == 1:
              choice_2 = choice_1 + 2
              choice_2 = choice_2 - 1
        else:
              choice_2 = choice_1 - 1

        # Alternative 2
        if choice_1 == 9:
              choice_3 = choice_1 - 2
        elif choice_1 == 1:
              choice_3 = choice_1 + 2
        else:
              choice_3 = choice_1 + 1

        # Getting the nominal weight for each pipe
        if brand == 'new pipe':
            Selected_nom = mySpec.new_drill_pipe_design_updated(choice_1)[1] # there is new_drill_pipe_design_updated
            Alt1_nom = mySpec.new_drill_pipe_design_updated(choice_2)[1]
            Alt2_nom = mySpec.new_drill_pipe_design_updated(choice_3)[1]

        elif brand == 'premium':
            Selected_nom = mySpec.premium_drill_pipe_design_updated(choice_1)[1] # there is premium_drill_pipe_design_updated
            Alt1_nom = mySpec.premium_drill_pipe_design_updated(choice_2)[1]
            Alt2_nom = mySpec.premium_drill_pipe_design_updated(choice_3)[1]

        elif brand == 'regular':
            Selected_nom = mySpec.class2_drill_pipe_design_updated(choice_1)[1] # class2_udpated
            Alt1_nom = mySpec.class2_drill_pipe_design_updated(choice_2)[1]
            Alt2_nom = mySpec.class2_drill_pipe_design_updated(choice_3)[1]

        # divider
        st.sidebar.divider()

        # header for collar column
        st.sidebar.markdown('<h3 style="text-align: center;">Collar Properties</h3>', unsafe_allow_html=True)


        # using radio instead of checkbox
        dc_diameter_list = [(4.0, 2.0), (4.0, 2.25), (4.5, 2.0), (4.5, 2.25), (5.0, 2.25), (5.0, 2.5), (5.5, 2.25), (5.5, 2.5), (6.0, 3.0)]
        if brand == 'new pipe':
            dc_choice_1 = st.sidebar.radio('(OD, ID)', dc_diameter_list)
        elif brand == 'premium': # 18/01/2024 -> Update this section with correct parameters
            dc_choice_1 = st.sidebar.radio('(OD, ID)', dc_diameter_list)
        else:
            dc_choice_1 = st.sidebar.radio('(OD, ID)', dc_diameter_list)

        # # Getting the choice as numbers so logic doesn't change
        dc_choice_1 = index(diameter_list=dc_diameter_list, choice=dc_choice_1)

        # Alternative 1
        if dc_choice_1 == 1:
            dc_choice_2 = dc_choice_1 + 2
            dc_choice_2 = dc_choice_2 - 1
        else:
            dc_choice_2 = dc_choice_1 - 1

        # Alternative 2
        if dc_choice_1 == 9:
            dc_choice_3 = dc_choice_1 - 2
        elif dc_choice_1 == 1:
            dc_choice_3 = dc_choice_1 + 2
        else:
            dc_choice_3 = dc_choice_1 + 1

        # Extracting nominal weight for drill collar length calculation
        Selected_dc_nom = mySpec.drill_collar_design(dc_choice_1)[1]
        Alt1_dc_nom = mySpec.drill_collar_design(dc_choice_2)[1]
        Alt2_dc_nom = mySpec.drill_collar_design(dc_choice_3)[1]

        # Drill collar length for collars
        Selected_dc_len = drill_collar_length(Selected_dc_nom)
        Alt1_dc_len = drill_collar_length(Alt1_dc_nom)
        Alt2_dc_len = drill_collar_length(Alt2_dc_nom)

        st.sidebar.divider()

        ####################################################################################################
        # Creating list to append for plotting
        # '''Plot Data For System Analysis'''
        # properties
        Sys_Sel = []  # all drill pipe properties
        Sys_Alt_1 = []  # all drill pipe properties for alt 1
        Sys_Alt_2 = []

        Sys_Sel_dc = []  # all drill collar properties
        Sys_Alt_1_dc = []
        Sys_Alt_2_dc = []

        # collapse pressure
        coll_plot = []
        coll_plotx = [1,1,2,2,3,3]

        dc_coll_plot = []
        dc_coll_plotx = [1,1,2,2,3,3]

        # Loads
        Load = []
        DSys_Load = []  # D_Torsion
        ESys_Load = []  # E_Torsion
        XSys_Load = []
        GSys_Load = []
        SSys_Load = []


        dc_Load = []
        dc_DSys_Load = []  # D_Torsion
        dc_ESys_Load = []  # E_Torsion

        SelectedLM = [] # Did we use this at all
        AlternativeLM1 = []
        AlternativeLM2 = []

        ########################################################################################################################
        # Drill pipe section
        ########################################################################################################################
        if brand == 'new pipe':
            Selected = mySpec.new_drill_pipe_design_updated(choice_1)
        elif brand == 'premium':
            Selected = mySpec.premium_drill_pipe_design_updated(choice_1)
        else:
            Selected = mySpec.class2_drill_pipe_design_updated(choice_1)

        # "Extract individual properties"
        # 'DP'
        Sys_Sel.append(Selected)

        DSys_Load.append(Selected[13])  # D_Torsion
        ESys_Load.append(Selected[14])  # E_Torsion
        XSys_Load.append(Selected[15])  # X_Torsion
        GSys_Load.append(Selected[16])  # G_Torsion
        SSys_Load.append(Selected[17])  # S_Torsion

        coll_plot.append(Selected[3])  # DCol_Pres
        coll_plot.append(Selected[4])  # ECol_Pres
        coll_plot.append(Selected[5])  # XCol_Pres
        coll_plot.append(Selected[6])  # GCol_Pres
        coll_plot.append(Selected[7])  # SCol_Pres

        # "Assigning variables for calculation"
        # DP
        Wght_dp = Selected[1]  # nom
        OD = Selected[0]
        ID = Selected[2]
        DYSmin = Selected[8]
        EYSmin = Selected[9]
        XYSmin = Selected[10]
        GYSmin = Selected[11]
        SYSmin = Selected[12]
        DCol_Pres = Selected[3]
        ECol_Pres = Selected[4]
        XCol_Pres = Selected[5]
        GCol_Pres = Selected[6]
        SCol_Pres = Selected[7]
        Torque = Selected[9]
        Torsion = Selected[10]

        # '''
        # We need to get DC properties before we can determine dysfunction
        # '''
        # 'Drill collar condition'
        Selected_dc = mySpec.drill_collar_design(dc_choice_1)
        Sys_Sel_dc.append(Selected_dc)

        dc_DSys_Load.append(Selected_dc[7])  # D_Torsion
        dc_ESys_Load.append(Selected_dc[8])  # E_Torsion
        dc_coll_plot.append(Selected_dc[3])  # DCol_Pres
        dc_coll_plot.append(Selected_dc[4])  # ECol_Pres

        Wght_dc = Selected_dc[1]  # nom
        ODc = Selected_dc[0]
        IDc = Selected_dc[2]
        DYSminC = Selected_dc[7]
        EYSminC = Selected_dc[8]
        DCol_PresC = Selected_dc[3]
        ECol_PresC = Selected_dc[4]
        TorqueC = Selected_dc[9]
        TorsionC = Selected_dc[10]

        # "Dysfunction determination for DP and DC"
        # mySpec.collapse_pressure(TVD=init_Vert ,Mud_W=12) # have not appended collapse pressure
        # MD_init can be replace with total_MD
        mySpec.loads(MD=total_MD,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=Wght_dc,Mud_W=10.0,MOP=100000.0)  # Making adjustment to arguments to factor DP length, consider selected and alternative pipes
        mySpec.Torque(RPM=100.0,OD=OD,ID=ID,YSmin= EYSmin)
        Load.append(mySpec.Total_Load)
        Load.append(mySpec.Act_Load_Top)
        Load.append(mySpec.Max_Allw_Load)
        # mySpec.printer()

        # DC
        mySpec.loads(MD=total_MD,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=Wght_dc,Mud_W=10.0,MOP=100000.0)  # Making adjustment to arguments to factor DP length, consider selected and alternative pipes
        mySpec.Torque(RPM=100.0,OD=ODc,ID=IDc,YSmin= EYSminC)
        dc_Load.append(mySpec.Total_Load)
        dc_Load.append(mySpec.Act_Load_Top)
        dc_Load.append(mySpec.Max_Allw_Load)
        # mySpec.printer()

        ############################################## Alternatives for pipes ##################################################
        # "Alternative1 for drill pipe"
        # Repeating the whole process again
        if brand == 'new':
            Alternative1 = mySpec.new_drill_pipe_design_updated(choice_2)
        elif brand == 'premium':
            Alternative1 = mySpec.premium_drill_pipe_design_updated(choice_2)
        else:
            Alternative1 = mySpec.class2_drill_pipe_design_updated(choice_2)

        Sys_Alt_1.append(Alternative1)
        DSys_Load.append(Alternative1[7])
        ESys_Load.append(Alternative1[8])
        # more of the alternative grades can be added
        coll_plot.append(Alternative1[3])
        coll_plot.append(Alternative1[4])

        Wght_dp = Alternative1[1]
        OD = Alternative1[0]
        ID = Alternative1[2]
        DYSmin = Alternative1[7]
        EYSmin = Alternative1[8]
        DCol_Pres=Alternative1[3]
        ECol_Pres=Alternative1[4]
        Torque=Alternative1[9]
        Torsion=Alternative1[10]

        Load.append(mySpec.Total_Load)
        Load.append(mySpec.Act_Load_Top)
        Load.append(mySpec.Max_Allw_Load)
        # mySpec.printer()

        # "Alternative 2 for drill pipe"
        if brand == 'new':
            Alternative2 = mySpec.new_drill_pipe_design_updated(choice_3)
        elif brand == 'premium':
            Alternative2 = mySpec.premium_drill_pipe_design_updated(choice_3)
        else:
            Alternative2 = mySpec.class2_drill_pipe_design_updated(choice_3)

        Sys_Alt_2.append(Alternative2)
        DSys_Load.append(Alternative2[7])
        ESys_Load.append(Alternative2[8])
        coll_plot.append(Alternative2[3])
        coll_plot.append(Alternative2[4])
        coll_plot.append(mySpec.Col_Pres)
        Wght_dp = Alternative2[1]
        OD = Alternative2[0]
        ID = Alternative2[2]
        DYSmin = Alternative2[7]
        EYSmin = Alternative2[8]
        DCol_Pres=Alternative2[3]
        ECol_Pres=Alternative2[4]
        Torque=Alternative2[9]
        Torsion=Alternative2[10]

        Load.append(mySpec.Total_Load)
        Load.append(mySpec.Act_Load_Top)
        Load.append(mySpec.Max_Allw_Load)
        # # mySpec.printer()

        ######################################################### Alternatives for collars #####################################
        # "Alternative 1 for drill collar"
        Alternative1 = mySpec.drill_collar_design(choice_2)
        Sys_Alt_1_dc.append(Alternative1)
        dc_DSys_Load.append(Alternative1[7])
        dc_ESys_Load.append(Alternative1[8])
        dc_coll_plot.append(Alternative1[3])
        dc_coll_plot.append(Alternative1[4])

        Wght_dc = Alternative1[1]
        ODc = Alternative1[0]
        IDc = Alternative1[2]
        DYSminC = Alternative1[7]
        EYSminC = Alternative1[8]
        DCol_PresC = Alternative1[3]
        ECol_PresC = Alternative1[4]
        TorqueC = Alternative1[9]
        TorsionC = Alternative1[10]

        dc_Load.append(mySpec.Total_Load)
        dc_Load.append(mySpec.Act_Load_Top)
        dc_Load.append(mySpec.Max_Allw_Load)
        # # mySpec.printer()

        # "Alternative 2 for drill collar"
        Alternative2 = mySpec.drill_collar_design(choice_3)
        Sys_Alt_2_dc.append(Alternative2)
        dc_DSys_Load.append(Alternative2[7])
        dc_ESys_Load.append(Alternative2[8])
        dc_coll_plot.append(Alternative2[3])
        dc_coll_plot.append(Alternative2[4])
        dc_coll_plot.append(mySpec.Col_Pres)

        Wght_dc = Alternative2[1]
        ODc = Alternative2[0]
        IDc = Alternative2[2]
        DYSminC = Alternative2[7]
        EYSminC = Alternative2[8]
        DCol_PresC = Alternative2[3]
        ECol_PresC = Alternative2[4]
        TorqueC = Alternative2[9]
        TorsionC = Alternative2[10]

        dc_Load.append(mySpec.Total_Load)
        dc_Load.append(mySpec.Act_Load_Top)
        dc_Load.append(mySpec.Max_Allw_Load)

        st.markdown("<h1 style='text-align: center;'>Drill Pipes Graph</h1>", unsafe_allow_html=True)

        # Create two columns
        col1, col2, col3 = st.columns(3)
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Display Plot 1 in the first column
        with col1:
            collapse_pressure(coll_plot)
            plt.title(" COLLAPSE PRESSURES OF PIPE CATEGORIES  ")
            plt.xlabel(" CATEGORIES OF PIPES ")
            st.pyplot()

        # Display Plot 2 in the second column
        with col2:
            tensile_loading_sel(DSys_Load, ESys_Load, Load)
            plt.title(" TENSILE LOADING OF SELECTED PIPE   ")
            st.pyplot()

        with col3:
            tensile_loading_alt(DSys_Load, ESys_Load, Load)
            st.pyplot()

        st.markdown("<h1 style='text-align: center;'>Drill Collars Graph</h1>", unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)

        with col4:
            collapse_pressure(dc_coll_plot)
            plt.title(" COLLAPSE PRESSURES OF COLLARS CATEGORIES  ")
            plt.xlabel(" CATEGORIES OF COLLARS ")
            st.pyplot()

        with col5:
            tensile_loading_sel(DSys_Load, ESys_Load, Load)
            plt.title(" TENSILE LOADING OF SELECTED COLLAR   ")
            st.pyplot()

        with col6:
            tensile_loading_alt(DSys_Load, ESys_Load, Load)
            st.pyplot()
