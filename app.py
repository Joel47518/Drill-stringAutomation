import streamlit as st
from specifications import specification
from Tracjectory import trajectory
import numpy as np
import matplotlib.pyplot as plt


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


# st.sidebar.divider()

# Create a sidebar
st.sidebar.title('Input Options')

st.sidebar.divider()
# Select box input
brand = st.sidebar.selectbox('Brand selection', ["new pipe", 'premium', 'class 2'])

# divider
st.sidebar.divider()

# header for pipe column
st.sidebar.markdown('<h3 style="text-align: center;">Pipe Properties</h3>', unsafe_allow_html=True)

# splitting the sidebar into two columns for selection of pipe properties
left_column, right_column = st.sidebar.columns(2)

# using radio instead of checkbox
if brand == 'new pipe':
    choice_1 = left_column.radio('(Outer diameter and Inn', [(4.0, 3.476), (4.0, 3.340), (4.5, 3.826), (4.5, 3.640), (5.0, 4.408), (5.0, 4.276), (5.5, 4.778), (5.5, 4.670), (6.625, 5.965)])
    # choice_1 = right_column.radio('er diameter)', ['(5, 6)', '(6, 7)', '(7, 8)'])
elif brand == 'premium':
    choice_1 = left_column.radio('(Outer diameter and Inn', [(4.0, 3.476), (4.0, 3.340), (4.5, 3.826), (4.5, 3.640), (5.0, 4.408), (5.0, 4.276), (5.5, 4.778), (5.5, 4.670), (6.625, 5.965)])
    # choice_1 = right_column.radio('er diameter)', ['(15, 16)', '(16, 17)', '(17, 18)'])
else:
    choice_1 = left_column.radio('(Outer diameter and Inn', [(4.0, 3.476), (4.0, 3.340), (4.5, 3.826), (4.5, 3.640), (5.0, 4.408), (5.0, 4.276), (5.5, 4.778), (5.5, 4.670), (6.625, 5.965)])
    # choice_1 = right_column.radio('er diameter)', ['(51, 61)', '(61, 71)', '(71, 81)'])

# Getting the choice as numbers so logic doesn't change
# creating an object of the specification class
mySpec = specification()
choice_1 = mySpec.choice_numbers(choice_1[1])
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
    Selected_nom = mySpec.new_drill_pipe_design(choice_1)[1]
    Alt1_nom = mySpec.new_drill_pipe_design(choice_2)[1]
    Alt2_nom = mySpec.new_drill_pipe_design(choice_3)[1]

elif brand == 'premium':
    Selected_nom = mySpec.premium_drill_pipe_design(choice_1)[1]
    Alt1_nom = mySpec.premium_drill_pipe_design(choice_2)[1]
    Alt2_nom = mySpec.premium_drill_pipe_design(choice_3)[1]

elif brand == 'regular':
    Selected_nom = mySpec.regular_drill_pipe_design(choice_1)[1]
    Alt1_nom = mySpec.regular_drill_pipe_design(choice_2)[1]
    Alt2_nom = mySpec.regular_drill_pipe_design(choice_3)[1]

# divider
st.sidebar.divider()

# header for collar column
st.sidebar.markdown('<h3 style="text-align: center;">Collar Properties</h3>', unsafe_allow_html=True)

# splitting the sidebar into two columns for selection of pipe properties
left_col, right_col = st.sidebar.columns(2)

# using radio instead of checkbox
if brand == 'new pipe':
    dc_choice_1 = left_col.radio('(OD, ID)', [(4, 3.476), '(20, 30)', '(30, 40)'])
    # dc_choice_1 = right_col.radio('', ['(50, 60)', '(60, 70)', '(70, 80)'])
elif brand == 'premium': # 18/01/2024 -> Update this section with correct parameters
    # dc_choice_1 = left_col.radio('(OD, ID)', [(4, 3.476), '(20, 30)', '(30, 40)'])
    dc_choice_1 = left_col.radio('(OD, ID)', ['(010, 020)', '(020, 030)', '(030, 040)'])
    # dc_choice_1 = right_col.radio('', ['(050, 060)', '(060, 070)', '(070, 080)'])
else:
    # dc_choice_1 = left_col.radio('(OD, ID)', ['(100, 200)', '(200, 300)', '(300, 400)'])
    dc_choice_1 = left_col.radio('(OD, ID)', [(4, 3.476), '(20, 30)', '(30, 40)'])
    # dc_choice_1 = right_col.radio('', ['(500, 600)', '(600, 700)', '(700, 800)'])

st.write("premium properties need to be updated to make premium selection work")

# Getting the choice as numbers so logic doesn't change
dc_choice_1 = mySpec.dc_choice_numbers(dc_choice_1[1])
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

########################################################################################################################
# Trajectory
########################################################################################################################
# Calling trajectory class to extract
My_traj = trajectory(KOP=1500.0,inc=20.0,bur=1.10,Target_TVD=6000.0,Target_East=1600.0,\
                     Target_North=1400.0,RTable=100)

Total_MD = My_traj.Total_MD

Selected_dp_len = Total_MD - Selected_dc_len
Alt1_dp_len = Total_MD - Alt1_dc_len
Alt2_dp_len = Total_MD - Alt2_dc_len

# Initial conditions
EAST =[]
NORTH =[]
VERT = []
MD_init=0.0

MD= 10.0          # Define the parameters again to declare the condition for the while loop
I1=0.0
I2=0.0
bur = 0.0
Cumm_Vert =0.0
Cumm_East =0.0
Cumm_North =0.0

init_Vert = 0.0
init_East = My_traj.Rig_East * 1.25
init_North =My_traj.Rig_North
Total_MD = My_traj.Total_MD

while MD_init < Total_MD :
    My_traj.cordinates(MD=MD, init_MD=MD_init, I1=I1, I2=I2, Cumm_Vert=Cumm_Vert, \
                       Cumm_East=Cumm_East, Cumm_North=Cumm_North, Bearing=30.0, inc=20.0, \
                       init_East=init_East, init_North=init_North, init_Vert=init_Vert)

    init_East = round(My_traj.init_East,2)
    init_North = round(My_traj.init_North,2)
    init_Vert = round(My_traj.init_Vert,2)
    MD_init= round(My_traj.init_MD,2)
    EAST.append(init_East)
    NORTH.append(init_North)
    VERT.append(init_Vert)
    I1=My_traj.I2

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
    Selected = mySpec.new_drill_pipe_design(choice_1)
elif brand == 'premium':
    Selected = mySpec.premium_drill_pipe_design(choice_1)
else:
    Selected = mySpec.class2_drill_pipe_design_updated(choice_1)

# "Extract individual properties"
# 'DP'
Sys_Sel.append(Selected)
# DSys_Load.append(Selected[7])  # D_Torsion
# ESys_Load.append(Selected[8])  # E_Torsion
# coll_plot.append(Selected[3])  # DCol_Pres
# coll_plot.append(Selected[4])  # ECol_Pres
# updated!!!!!!!
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

# # User information
# print("\n\n\n       Drill Pipe Selected ","\n \n","DCol_Pres : ",DCol_Pres, "    ","ECol_Pres : ",\
#       ECol_Pres, "    ","Nominal_weight : ", Wght_dp, "    ","OD : ",OD,"    ","ID : ",ID,"    ","DYSim : ",DYSmin,\
#       "    ","EYSin : ",EYSmin,"Torq  : ",Torque,"   Tors  : ",Torsion)


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
#
# print("\n\n\n       Drill Collar Selected ","\n \n","DCol_Pres : ",DCol_PresC, "    ","ECol_Pres : ",\
#       ECol_PresC, "    ","Nominal_weight : ", Wght_dc, "    ","OD : ",ODc,"    ","ID : ",IDc,"    ","DYSim : ",DYSminC,\
#       "    ","EYSin : ",EYSminC,"Torq  : ",TorqueC,"   Tors  : ",TorsionC)


# "Dysfunction determination for DP and DC"
# mySpec.collapse_pressure(TVD=init_Vert ,Mud_W=12) # have not appended collapse pressure
mySpec.loads(MD=MD_init,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=Wght_dc,Mud_W=10.0,MOP=100000.0)  # Making adjustment to arguments to factor DP length, consider selected and alternative pipes
mySpec.Torque(RPM=100.0,OD=OD,ID=ID,YSmin= EYSmin)
Load.append(mySpec.Total_Load)
Load.append(mySpec.Act_Load_Top)
Load.append(mySpec.Max_Allw_Load)
# mySpec.printer()

# DC
mySpec.loads(MD=MD_init,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=Wght_dc,Mud_W=10.0,MOP=100000.0)  # Making adjustment to arguments to factor DP length, consider selected and alternative pipes
mySpec.Torque(RPM=100.0,OD=ODc,ID=IDc,YSmin= EYSminC)
dc_Load.append(mySpec.Total_Load)
dc_Load.append(mySpec.Act_Load_Top)
dc_Load.append(mySpec.Max_Allw_Load)
# mySpec.printer()

############################################## Alternatives for pipes ##################################################
# "Alternative1 for drill pipe"
if brand == 'new':
    Alternative1 = mySpec.new_drill_pipe_design(choice_2)
elif brand == 'premium':
    Alternative1 = mySpec.premium_drill_pipe_design(choice_2)
else:
    Alternative1 = mySpec.class2_drill_pipe_design_updated(choice_2)

Sys_Alt_1.append(Alternative1)
DSys_Load.append(Alternative1[7])
ESys_Load.append(Alternative1[8])
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

# print("\n\n\n       Drill String Alternative_1 ","\n \n","D : ",DCol_Pres, "    ","E : ",ECol_Pres, "    ",Wght_dp, "    ",OD,"    ",ID,"    ","D : ",DYSmin,"    ","E : ",EYSmin,"Torq  : ",Torque,"   Tors  : ",Torsion)
# mySpec.collapse_pressure(TVD=init_Vert ,Mud_W=12)
# mySpec.loads(MD=MD_init,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=103.0,Mud_W=10.0,MOP=100000.0)
# mySpec.Torque(RPM=100.0,OD=OD,ID=ID,YSmin= EYSmin)
Load.append(mySpec.Total_Load)
Load.append(mySpec.Act_Load_Top)
Load.append(mySpec.Max_Allw_Load)
# mySpec.printer()

# "Alternative 2 for drill pipe"
if brand == 'new':
    Alternative2 = mySpec.new_drill_pipe_design(choice_3)
elif brand == 'premium':
    Alternative2 = mySpec.premium_drill_pipe_design(choice_3)
else:
    Alternative2 = mySpec.regular_drill_pipe_design(choice_3)

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

# print("\n\n\n       Drill String Alternative_2 ","\n \n","D : ",DCol_Pres, "    ","E : ",ECol_Pres, "    ",Wght_dp, "    ",OD,"    ",ID,"    ","D : ",DYSmin,"    ","E : ",EYSmin,"Torq  : ",Torque,"   Tors  : ",Torsion)
# mySpec.collapse_pressure(TVD=init_Vert ,Mud_W=12)
# mySpec.loads(MD=MD_init,Wght_dp=Wght_dp,Len_dc=780,Wght_dc=103.0,Mud_W=10.0,MOP=100000.0)
# mySpec.Torque(RPM=100.0,OD=OD,ID=ID,YSmin= EYSmin)
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

# print("\n\n\n       Drill Collar Selected ","\n \n","DCol_Pres : ",DCol_PresC, "    ","ECol_Pres : ",\
#       ECol_PresC, "    ","Nominal_weight : ", Wght_dc, "    ","OD : ",ODc,"    ","ID : ",IDc,"    ","DYSim : ",DYSminC,\
#       "    ","EYSin : ",EYSminC,"Torq  : ",TorqueC,"   Tors  : ",TorsionC)
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

# print("\n\n\n       Drill Collar Selected ","\n \n","DCol_Pres : ",DCol_PresC, "    ","ECol_Pres : ",\
#       ECol_PresC, "    ","Nominal_weight : ", Wght_dc, "    ","OD : ",ODc,"    ","ID : ",IDc,"    ","DYSim : ",DYSminC,\
#       "    ","EYSin : ",EYSminC,"Torq  : ",TorqueC,"   Tors  : ",TorsionC)
dc_Load.append(mySpec.Total_Load)
dc_Load.append(mySpec.Act_Load_Top)
dc_Load.append(mySpec.Max_Allw_Load)


# East = [1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.2, 1517.21, 1517.22, 1517.23, 1517.24, 1517.25, 1517.26, 1517.28, 1517.3, 1517.32, 1517.34, 1517.36, 1517.38, 1517.41, 1517.44, 1517.47, 1517.5, 1517.53, 1517.57, 1517.61, 1517.65, 1517.69, 1517.73, 1517.77, 1517.82, 1517.87, 1517.92, 1517.97, 1518.02, 1518.07, 1518.13, 1518.19, 1518.25, 1518.31, 1518.37, 1518.44, 1518.51, 1518.58, 1518.65, 1518.72, 1518.79, 1518.87, 1518.95, 1519.03, 1519.11, 1519.19, 1519.27, 1519.36, 1519.45, 1519.54, 1519.63, 1519.72, 1519.81, 1519.91, 1520.01, 1520.11, 1520.21, 1520.31, 1520.42, 1520.53, 1520.64, 1520.75, 1520.86, 1520.97, 1521.09, 1521.21, 1521.33, 1521.45, 1521.57, 1521.69, 1521.82, 1521.95, 1522.08, 1522.21, 1522.34, 1522.47, 1522.61, 1522.75, 1522.89, 1523.03, 1523.17, 1523.32, 1523.47, 1523.62, 1523.77, 1523.92, 1524.07, 1524.23, 1524.39, 1524.55, 1524.71, 1524.87, 1525.03, 1525.2, 1525.37, 1525.54, 1525.71, 1525.88, 1526.05, 1526.23, 1526.41, 1526.59, 1526.77, 1526.95, 1527.14, 1527.33, 1527.52, 1527.71, 1527.9, 1528.09, 1528.29, 1528.49, 1528.69, 1528.89, 1529.09, 1529.29, 1529.5, 1529.71, 1529.92, 1530.13, 1530.34, 1530.55, 1530.77, 1530.99, 1531.21, 1531.43, 1531.65, 1531.87, 1532.1, 1532.33, 1532.56, 1532.79, 1533.02, 1533.25, 1533.49, 1533.73, 1533.97, 1534.21, 1534.45, 1534.69, 1534.94, 1535.19, 1535.44, 1535.69, 1535.94, 1536.19, 1536.45, 1536.71, 1536.97, 1537.23, 1537.49, 1537.76, 1538.03, 1538.3, 1538.57, 1538.84, 1539.11, 1539.39, 1539.67, 1539.95, 1540.23, 1540.51, 1540.79, 1541.08, 1541.37, 1541.66, 1541.95, 1542.24, 1542.53, 1542.83, 1543.13, 1543.43, 1543.73, 1544.03, 1544.33, 1544.64, 1544.95, 1545.26, 1545.57, 1545.88, 1546.19, 1546.5, 1546.81, 1547.12, 1547.43, 1547.74, 1548.05, 1548.36, 1548.67, 1548.98, 1549.29, 1549.6, 1549.91, 1550.22, 1550.53, 1550.84, 1551.15, 1551.46, 1551.77, 1552.08, 1552.39, 1552.7, 1553.01, 1553.32, 1553.63, 1553.94, 1554.25, 1554.56, 1554.87, 1555.18, 1555.49, 1555.8, 1556.11, 1556.42, 1556.73, 1557.04, 1557.35, 1557.66, 1557.97, 1558.28, 1558.59, 1558.9, 1559.21, 1559.52, 1559.83, 1560.14, 1560.45, 1560.76, 1561.07, 1561.38, 1561.69, 1562.0, 1562.31, 1562.62, 1562.93, 1563.24, 1563.55, 1563.86, 1564.17, 1564.48, 1564.79, 1565.1, 1565.41, 1565.72, 1566.03, 1566.34, 1566.65, 1566.96, 1567.27, 1567.58, 1567.89, 1568.2, 1568.51, 1568.82, 1569.13, 1569.44, 1569.75, 1570.06, 1570.37, 1570.68, 1570.99, 1571.3, 1571.61, 1571.92, 1572.23, 1572.54, 1572.85, 1573.16, 1573.47, 1573.78, 1574.09, 1574.4, 1574.71, 1575.02, 1575.33, 1575.64, 1575.95, 1576.26, 1576.57, 1576.88, 1577.19, 1577.5, 1577.81, 1578.12, 1578.43, 1578.74, 1579.05, 1579.36, 1579.67, 1579.98, 1580.29, 1580.6, 1580.91, 1581.22, 1581.53, 1581.84, 1582.15, 1582.46, 1582.77, 1583.08, 1583.39, 1583.7, 1584.01, 1584.32, 1584.63, 1584.94, 1585.25, 1585.56, 1585.87, 1586.18, 1586.49, 1586.8, 1587.11, 1587.42, 1587.73, 1588.04, 1588.35, 1588.66, 1588.97, 1589.28, 1589.59, 1589.9, 1590.21, 1590.52, 1590.83, 1591.14, 1591.45, 1591.76, 1592.07, 1592.38, 1592.69, 1593.0, 1593.31, 1593.62, 1593.93, 1594.24, 1594.55, 1594.86, 1595.17, 1595.48, 1595.79, 1596.1, 1596.41, 1596.72, 1597.03, 1597.34, 1597.65, 1597.96, 1598.27, 1598.58, 1598.89, 1599.2, 1599.51, 1599.82, 1600.13, 1600.44, 1600.75, 1601.06, 1601.37, 1601.68, 1601.99, 1602.3, 1602.61, 1602.92, 1603.23, 1603.54, 1603.85, 1604.16, 1604.47, 1604.78, 1605.09, 1605.4, 1605.71, 1606.02, 1606.33, 1606.64, 1606.95, 1607.26, 1607.57, 1607.88, 1608.19, 1608.5, 1608.81, 1609.12, 1609.43, 1609.74, 1610.05, 1610.36, 1610.67, 1610.98, 1611.29, 1611.6, 1611.91, 1612.22, 1612.53, 1612.84, 1613.15, 1613.46, 1613.77, 1614.08, 1614.39, 1614.7, 1615.01, 1615.32, 1615.63, 1615.94, 1616.25, 1616.56, 1616.87, 1617.18, 1617.49, 1617.8, 1618.11, 1618.42, 1618.73, 1619.04, 1619.35, 1619.66, 1619.97, 1620.28, 1620.59, 1620.9, 1621.21, 1621.52, 1621.83, 1622.14, 1622.45, 1622.76, 1623.07, 1623.38, 1623.69, 1624.0, 1624.31, 1624.62, 1624.93, 1625.24, 1625.55, 1625.86, 1626.17, 1626.48, 1626.79, 1627.1, 1627.41, 1627.72, 1628.03, 1628.34, 1628.65, 1628.96, 1629.27, 1629.58, 1629.89, 1630.2, 1630.51, 1630.82, 1631.13, 1631.44, 1631.75, 1632.06, 1632.37]
# North = [1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.0, 1400.01, 1400.02, 1400.04, 1400.06, 1400.09, 1400.12, 1400.16, 1400.2, 1400.25, 1400.3, 1400.36, 1400.42, 1400.49, 1400.56, 1400.64, 1400.72, 1400.81, 1400.9, 1401.0, 1401.1, 1401.21, 1401.32, 1401.44, 1401.56, 1401.69, 1401.82, 1401.96, 1402.1, 1402.25, 1402.4, 1402.56, 1402.72, 1402.89, 1403.06, 1403.24, 1403.42, 1403.61, 1403.8, 1404.0, 1404.21, 1404.42, 1404.64, 1404.86, 1405.09, 1405.32, 1405.56, 1405.8, 1406.05, 1406.3, 1406.56, 1406.82, 1407.09, 1407.36, 1407.64, 1407.92, 1408.21, 1408.5, 1408.8, 1409.1, 1409.41, 1409.72, 1410.04, 1410.36, 1410.69, 1411.02, 1411.36, 1411.7, 1412.05, 1412.4, 1412.76, 1413.12, 1413.49, 1413.86, 1414.24, 1414.62, 1415.01, 1415.4, 1415.8, 1416.2, 1416.61, 1417.02, 1417.44, 1417.86, 1418.29, 1418.72, 1419.16, 1419.6, 1420.05, 1420.5, 1420.96, 1421.42, 1421.89, 1422.36, 1422.84, 1423.32, 1423.81, 1424.3, 1424.8, 1425.3, 1425.81, 1426.32, 1426.84, 1427.36, 1427.89, 1428.42, 1428.96, 1429.5, 1430.05, 1430.6, 1431.16, 1431.72, 1432.29, 1432.86, 1433.44, 1434.02, 1434.61, 1435.2, 1435.8, 1436.4, 1437.01, 1437.62, 1438.24, 1438.86, 1439.48, 1440.11, 1440.74, 1441.38, 1442.02, 1442.67, 1443.32, 1443.98, 1444.64, 1445.31, 1445.98, 1446.66, 1447.34, 1448.03, 1448.72, 1449.42, 1450.12, 1450.83, 1451.54, 1452.26, 1452.98, 1453.71, 1454.44, 1455.18, 1455.92, 1456.67, 1457.42, 1458.18, 1458.94, 1459.71, 1460.48, 1461.26, 1462.04, 1462.83, 1463.62, 1464.42, 1465.22, 1466.03, 1466.84, 1467.66, 1468.48, 1469.3, 1470.13, 1470.96, 1471.8, 1472.64, 1473.49, 1474.34, 1475.2, 1476.06, 1476.93, 1477.8, 1478.68, 1479.56, 1480.45, 1481.34, 1482.24, 1483.14, 1484.04, 1484.94, 1485.84, 1486.74, 1487.64, 1488.54, 1489.44, 1490.34, 1491.24, 1492.14, 1493.04, 1493.94, 1494.84, 1495.74, 1496.64, 1497.54, 1498.44, 1499.34, 1500.24, 1501.14, 1502.04, 1502.94, 1503.84, 1504.74, 1505.64, 1506.54, 1507.44, 1508.34, 1509.24, 1510.14, 1511.04, 1511.94, 1512.84, 1513.74, 1514.64, 1515.54, 1516.44, 1517.34, 1518.24, 1519.14, 1520.04, 1520.94, 1521.84, 1522.74, 1523.64, 1524.54, 1525.44, 1526.34, 1527.24, 1528.14, 1529.04, 1529.94, 1530.84, 1531.74, 1532.64, 1533.54, 1534.44, 1535.34, 1536.24, 1537.14, 1538.04, 1538.94, 1539.84, 1540.74, 1541.64, 1542.54, 1543.44, 1544.34, 1545.24, 1546.14, 1547.04, 1547.94, 1548.84, 1549.74, 1550.64, 1551.54, 1552.44, 1553.34, 1554.24, 1555.14, 1556.04, 1556.94, 1557.84, 1558.74, 1559.64, 1560.54, 1561.44, 1562.34, 1563.24, 1564.14, 1565.04, 1565.94, 1566.84, 1567.74, 1568.64, 1569.54, 1570.44, 1571.34, 1572.24, 1573.14, 1574.04, 1574.94, 1575.84, 1576.74, 1577.64, 1578.54, 1579.44, 1580.34, 1581.24, 1582.14, 1583.04, 1583.94, 1584.84, 1585.74, 1586.64, 1587.54, 1588.44, 1589.34, 1590.24, 1591.14, 1592.04, 1592.94, 1593.84, 1594.74, 1595.64, 1596.54, 1597.44, 1598.34, 1599.24, 1600.14, 1601.04, 1601.94, 1602.84, 1603.74, 1604.64, 1605.54, 1606.44, 1607.34, 1608.24, 1609.14, 1610.04, 1610.94, 1611.84, 1612.74, 1613.64, 1614.54, 1615.44, 1616.34, 1617.24, 1618.14, 1619.04, 1619.94, 1620.84, 1621.74, 1622.64, 1623.54, 1624.44, 1625.34, 1626.24, 1627.14, 1628.04, 1628.94, 1629.84, 1630.74, 1631.64, 1632.54, 1633.44, 1634.34, 1635.24, 1636.14, 1637.04, 1637.94, 1638.84, 1639.74, 1640.64, 1641.54, 1642.44, 1643.34, 1644.24, 1645.14, 1646.04, 1646.94, 1647.84, 1648.74, 1649.64, 1650.54, 1651.44, 1652.34, 1653.24, 1654.14, 1655.04, 1655.94, 1656.84, 1657.74, 1658.64, 1659.54, 1660.44, 1661.34, 1662.24, 1663.14, 1664.04, 1664.94, 1665.84, 1666.74, 1667.64, 1668.54, 1669.44, 1670.34, 1671.24, 1672.14, 1673.04, 1673.94, 1674.84, 1675.74, 1676.64, 1677.54, 1678.44, 1679.34, 1680.24, 1681.14, 1682.04, 1682.94, 1683.84, 1684.74, 1685.64, 1686.54, 1687.44, 1688.34, 1689.24, 1690.14, 1691.04, 1691.94, 1692.84, 1693.74, 1694.64, 1695.54, 1696.44, 1697.34, 1698.24, 1699.14, 1700.04, 1700.94, 1701.84, 1702.74, 1703.64, 1704.54, 1705.44, 1706.34, 1707.24, 1708.14, 1709.04, 1709.94, 1710.84, 1711.74, 1712.64, 1713.54, 1714.44, 1715.34, 1716.24, 1717.14, 1718.04, 1718.94, 1719.84, 1720.74, 1721.64, 1722.54, 1723.44, 1724.34, 1725.24, 1726.14, 1727.04, 1727.94, 1728.84, 1729.74, 1730.64, 1731.54, 1732.44, 1733.34, 1734.24]
# Vert = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0, 170.0, 180.0, 190.0, 200.0, 210.0, 220.0, 230.0, 240.0, 250.0, 260.0, 270.0, 280.0, 290.0, 300.0, 310.0, 320.0, 330.0, 340.0, 350.0, 360.0, 370.0, 380.0, 390.0, 400.0, 410.0, 420.0, 430.0, 440.0, 450.0, 460.0, 470.0, 480.0, 490.0, 500.0, 510.0, 520.0, 530.0, 540.0, 550.0, 560.0, 570.0, 580.0, 590.0, 600.0, 610.0, 620.0, 630.0, 640.0, 650.0, 660.0, 670.0, 680.0, 690.0, 700.0, 710.0, 720.0, 730.0, 740.0, 750.0, 760.0, 770.0, 780.0, 790.0, 800.0, 810.0, 820.0, 830.0, 840.0, 850.0, 860.0, 870.0, 880.0, 890.0, 900.0, 910.0, 920.0, 930.0, 940.0, 950.0, 960.0, 970.0, 980.0, 990.0, 1000.0, 1010.0, 1020.0, 1030.0, 1040.0, 1050.0, 1060.0, 1070.0, 1080.0, 1090.0, 1100.0, 1110.0, 1120.0, 1130.0, 1140.0, 1150.0, 1160.0, 1170.0, 1180.0, 1190.0, 1200.0, 1210.0, 1220.0, 1230.0, 1240.0, 1250.0, 1260.0, 1270.0, 1280.0, 1290.0, 1300.0, 1310.0, 1320.0, 1330.0, 1340.0, 1350.0, 1360.0, 1370.0, 1380.0, 1390.0, 1400.0, 1410.0, 1420.0, 1430.0, 1440.0, 1450.0, 1460.0, 1470.0, 1480.0, 1490.0, 1500.0, 1510.0, 1520.0, 1530.0, 1540.0, 1550.0, 1560.0, 1570.0, 1580.0, 1590.0, 1600.0, 1610.0, 1620.0, 1630.0, 1640.0, 1650.0, 1660.0, 1670.0, 1680.0, 1690.0, 1700.0, 1710.0, 1720.0, 1730.0, 1740.0, 1750.0, 1760.0, 1769.99, 1779.98, 1789.97, 1799.96, 1809.95, 1819.94, 1829.93, 1839.92, 1849.91, 1859.9, 1869.89, 1879.88, 1889.87, 1899.85, 1909.83, 1919.81, 1929.79, 1939.77, 1949.75, 1959.73, 1969.71, 1979.68, 1989.65, 1999.62, 2009.59, 2019.56, 2029.53, 2039.5, 2049.46, 2059.42, 2069.38, 2079.34, 2089.3, 2099.25, 2109.2, 2119.15, 2129.1, 2139.05, 2149.0, 2158.94, 2168.88, 2178.82, 2188.76, 2198.69, 2208.62, 2218.55, 2228.48, 2238.41, 2248.33, 2258.25, 2268.17, 2278.09, 2288.0, 2297.91, 2307.82, 2317.73, 2327.63, 2337.53, 2347.43, 2357.33, 2367.22, 2377.11, 2387.0, 2396.88, 2406.76, 2416.64, 2426.51, 2436.38, 2446.25, 2456.12, 2465.98, 2475.84, 2485.7, 2495.55, 2505.4, 2515.25, 2525.09, 2534.93, 2544.77, 2554.6, 2564.43, 2574.26, 2584.08, 2593.9, 2603.71, 2613.52, 2623.33, 2633.13, 2642.93, 2652.73, 2662.52, 2672.31, 2682.09, 2691.87, 2701.65, 2711.42, 2721.19, 2730.95, 2740.71, 2750.47, 2760.22, 2769.97, 2779.71, 2789.45, 2799.18, 2808.91, 2818.63, 2828.35, 2838.07, 2847.78, 2857.49, 2867.19, 2876.89, 2886.58, 2896.27, 2905.95, 2915.63, 2925.3, 2934.97, 2944.63, 2954.29, 2963.94, 2973.59, 2983.23, 2992.87, 3002.5, 3012.13, 3021.75, 3031.37, 3040.98, 3050.59, 3060.19, 3069.79, 3079.38, 3088.97, 3098.55, 3108.12, 3117.69, 3127.25, 3136.81, 3146.36, 3155.91, 3165.45, 3174.98, 3184.51, 3194.03, 3203.55, 3213.06, 3222.57, 3232.07, 3241.56, 3251.05, 3260.53, 3270.01, 3279.48, 3288.94, 3298.4, 3307.85, 3317.29, 3326.73, 3336.16, 3345.58, 3355.0, 3364.41, 3373.82, 3383.22, 3392.62, 3402.02, 3411.42, 3420.82, 3430.22, 3439.62, 3449.02, 3458.42, 3467.82, 3477.22, 3486.62, 3496.02, 3505.42, 3514.82, 3524.22, 3533.62, 3543.02, 3552.42, 3561.82, 3571.22, 3580.62, 3590.02, 3599.42, 3608.82, 3618.22, 3627.62, 3637.02, 3646.42, 3655.82, 3665.22, 3674.62, 3684.02, 3693.42, 3702.82, 3712.22, 3721.62, 3731.02, 3740.42, 3749.82, 3759.22, 3768.62, 3778.02, 3787.42, 3796.82, 3806.22, 3815.62, 3825.02, 3834.42, 3843.82, 3853.22, 3862.62, 3872.02, 3881.42, 3890.82, 3900.22, 3909.62, 3919.02, 3928.42, 3937.82, 3947.22, 3956.62, 3966.02, 3975.42, 3984.82, 3994.22, 4003.62, 4013.02, 4022.42, 4031.82, 4041.22, 4050.62, 4060.02, 4069.42, 4078.82, 4088.22, 4097.62, 4107.02, 4116.42, 4125.82, 4135.22, 4144.62, 4154.02, 4163.42, 4172.82, 4182.22, 4191.62, 4201.02, 4210.42, 4219.82, 4229.22, 4238.62, 4248.02, 4257.42, 4266.82, 4276.22, 4285.62, 4295.02, 4304.42, 4313.82, 4323.22, 4332.62, 4342.02, 4351.42, 4360.82, 4370.22, 4379.62, 4389.02, 4398.42, 4407.82, 4417.22, 4426.62, 4436.02, 4445.42, 4454.82, 4464.22, 4473.62, 4483.02, 4492.42, 4501.82, 4511.22, 4520.62, 4530.02, 4539.42, 4548.82, 4558.22, 4567.62, 4577.02, 4586.42, 4595.82, 4605.22, 4614.62, 4624.02, 4633.42, 4642.82, 4652.22, 4661.62, 4671.02, 4680.42, 4689.82, 4699.22, 4708.62, 4718.02, 4727.42, 4736.82, 4746.22, 4755.62, 4765.02, 4774.42, 4783.82, 4793.22, 4802.62, 4812.02, 4821.42, 4830.82, 4840.22, 4849.62, 4859.02, 4868.42, 4877.82, 4887.22, 4896.62, 4906.02, 4915.42, 4924.82, 4934.22, 4943.62, 4953.02, 4962.42, 4971.82, 4981.22, 4990.62, 5000.02, 5009.42, 5018.82, 5028.22, 5037.62, 5047.02, 5056.42, 5065.82, 5075.22, 5084.62, 5094.02, 5103.42, 5112.82, 5122.22, 5131.62, 5141.02, 5150.42, 5159.82, 5169.22, 5178.62, 5188.02, 5197.42, 5206.82, 5216.22, 5225.62, 5235.02, 5244.42, 5253.82, 5263.22, 5272.62, 5282.02, 5291.42, 5300.82, 5310.22, 5319.62, 5329.02, 5338.42, 5347.82, 5357.22, 5366.62, 5376.02, 5385.42, 5394.82, 5404.22, 5413.62, 5423.02, 5432.42, 5441.82, 5451.22, 5460.62, 5470.02, 5479.42, 5488.82, 5498.22, 5507.62, 5517.02, 5526.42, 5535.82, 5545.22, 5554.62, 5564.02, 5573.42, 5582.82, 5592.22, 5601.62, 5611.02, 5620.42, 5629.82, 5639.22, 5648.62, 5658.02, 5667.42, 5676.82, 5686.22, 5695.62, 5705.02, 5714.42, 5723.82, 5733.22, 5742.62, 5752.02, 5761.42, 5770.82, 5780.22, 5789.62, 5799.02, 5808.42, 5817.82, 5827.22, 5836.62, 5846.02, 5855.42, 5864.82, 5874.22, 5883.62, 5893.02, 5902.42, 5911.82, 5921.22, 5930.62, 5940.02, 5949.42, 5958.82, 5968.22, 5977.62, 5987.02, 5996.42, 6005.82]
#
# coll_plot = [8330, 11350, 0.0, 8410, 0.0, 8410, 4216.08564]
# dc_coll_plot = [7620, 10390, 0.0, 8410, 7620, 10390, 4216.08564]
# coll_plotx = [1, 1, 2, 2, 3, 3]
#
# DSys_Load = [209000, 0.0, 0.0]
# ESys_Load = [285000, 231000, 231000]
# Load = [88968.0, 193416.4, 164403.94, 144685.5, 251919.775, 214131.80875, 144685.5, 251919.775, 214131.80875]
# DC_DSys_Load = [242000, 0.0, 242000]
# DC_ESys_Load = [331000, 231000, 331000]
# DC_Load = [88968.0, 193416.4, 164403.94, 144685.5, 251919.775, 214131.80875, 144685.5, 251919.775, 214131.80875]


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

st.markdown("<h1 style='text-align: center;'>Well Trajectory Graph</h1>", unsafe_allow_html=True)
col7, col8 = st.columns(2)

with col7:
    well_trajectory_3D(EAST, NORTH, VERT)
    st.pyplot()

# Display Plot 2 in the second column
with col8:
    well_trajectory_2D(EAST, VERT)
    st.pyplot()