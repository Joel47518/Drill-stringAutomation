import math

pi = math.pi
rad = math.radians
cos = math.cos
sin = math.sin

# contructor consists of non mandatory parameters

class specification:

    # def __init__(self, Crit_Vibr=0.0, Stretch=0.0, Shear_Stress=0.0, Max_Shear_Stress=0.0, Len_dp=1.0, \
    #              HP=0.0, Min_Tors_Yd_UnTen=0.0, Ipolar=0.0, CS_Area=0.0, Torq=0.0, SG_Mud=0.0, \
    #              Max_Allw_Load=0.0, Act_Load_Top=0.0, BF=0.0, Total_Load=0.0, Col_Pres=0.0, \
    #              TVD=0.0, Mud_W=0.0, MD=2.0, Wght_dp=0.0, Len_dc=1.0, inc=0.0, \
    #              Wght_dc=0.0, MOP=100000, Cd=0.000005, RPM=50.0, OD=5.5, ID=4.670, YSmin=0.0):
    def __init__(self, Crit_Vibr=0.0, Stretch=0.0, Shear_Stress=0.0, Max_Shear_Stress=0.0, Len_dp=0.0, \
                 HP=0.0, Min_Tors_Yd_UnTen=0.0, Ipolar=0.0, CS_Area=0.0, Torq=0.0, SG_Mud=0.0, \
                 Max_Allw_Load=0.0, Act_Load_Top=0.0, BF=0.0, Total_Load=0.0, Col_Pres=0.0, \
                 TVD=0.0, Mud_W=0.0, MD=2.0, Wght_dp=0.0, Len_dc=0.0, inc=0.0, \
                 Wght_dc=0.0, MOP=100000, Cd=0.000005, RPM=50.0, YSmin=0.0):

        self.Col_Pres = Col_Pres
        self.inc = inc
        self.TVD = TVD
        self.Cd = Cd
        self.Mud_W = Mud_W
        self.Wght_dp = Wght_dp
        self.Len_dc = Len_dc
        self.Wght_dc = Wght_dc
        self.Mud_W = Mud_W
        self.MD = MD
        self.MOP = MOP
        self.Len_dp = self.MD - self.Len_dc
        self.Total_Load = Total_Load
        self.BF = BF
        self.Act_Load_Top = Act_Load_Top
        self.Max_Allw_Load = Max_Allw_Load
        self.SG_Mud = SG_Mud
        self.HP = HP
        self.Torq = Torq
        self.CS_Area = CS_Area
        self.Ipolar = Ipolar
        self.Min_Tors_Yd_UnTen = Min_Tors_Yd_UnTen
        self.Stretch = Stretch
        self.Shear_Stress = Shear_Stress
        self.Max_Shear_Stress = Max_Shear_Stress
        self.Crit_Vibr = Crit_Vibr

    def collapse_pressure(self, TVD, Mud_W):
        try:
            self.TVD = TVD
            self.Mud_W = Mud_W
            self.Col_Pres = 0.052 * self.TVD * self.Mud_W * 1.125
        except:
            print("A error Occured Please enter TVD and Mud_W")
        '''Collapse Safety Factor of 1.125     *0.00004823 '''

        '''Compare the Calc Collapse, Col_Pres with the Collapse pressure from the Pipe '''

    def loads(self, MD, Wght_dp, Len_dc, Wght_dc, Mud_W, MOP):

        self.Wght_dp = Wght_dp
        self.Len_dc = Len_dc
        self.Wght_dc = Wght_dc
        self.Mud_W = Mud_W
        self.MD = MD
        self.MOP = MOP
        self.Len_dp = self.MD - self.Len_dc
        self.DC_Weight = self.Len_dc * self.Wght_dc
        self.DC_Weight_use = (self.Len_dc * self.Wght_dc) * 0.75  # Factor to ensure Lnp in DC
        self.Total_Load = ((self.Len_dc * self.Wght_dc) + (self.Wght_dp * self.Len_dp))
        self.BF = 1 - (self.Mud_W / 62.5)
        self.Lnp = self.DC_Weight_use / (self.Wght_dc * self.BF)

        self.Act_Load_Top = self.MOP + ((self.MD - self.Len_dc) * \
                                        self.Wght_dp + (self.Len_dc * self.Wght_dc)) * self.BF * 1.25

        ''' Compare Act_Load_Top to the tensile Strength of the Drill Pipe'''

        self.Max_Allw_Load = 0.85 * self.Act_Load_Top

    def Torque(self, OD, ID, YSmin, RPM=50):
        self.RPM = RPM
        self.YSmin = YSmin
        self.OD = OD
        self.ID = ID
        self.SG_Mud = self.Mud_W / 8.33
        self.HP = self.Cd * (self.OD ** 2) * self.RPM * self.MD * self.SG_Mud
        self.Torq = 5252 * self.HP / self.RPM
        self.CS_Area = (pi / 4) * ((self.OD ** 2) - (self.ID ** 2))
        self.Ipolar = (pi / 32) * ((self.OD ** 4) - (self.ID ** 4))
        self.Min_Tors_Yd_UnTen = (((0.096167 * self.Ipolar) / (self.OD)) * (
                    (self.YSmin ** 2) - ((self.Total_Load) ** 2 / (self.CS_Area ** 2))) ** (1 / 2)) * 0.0833
        self.Stretch = ((self.Len_dp ** 2) * (65.44 - 1.44 * self.Mud_W)) / (96250000)
        self.Shear_Stress = (self.Torq * 5.124) / self.Ipolar
        self.Max_Shear_Stress = 64 * self.OD * self.Torq / (pi * (self.OD ** 4) - (self.ID ** 4))
        self.Crit_Vibr = (4760000 / self.Len_dp) * (((self.OD ** 2) - (self.ID ** 2)) ** (1 / 2))
        self.annulus = 7.5 - self.OD  # 7.5 Hole diameter

        self.E = 23  # Young's modulus
        self.I = (pi / 64) * ((self.OD ** 4) - (self.ID ** 4))
        self.W = self.Wght_dp * self.BF

        ########## CRITICAL BUCKLING ##########

        self.Fcr = 2 * (
                    (self.E * self.I * self.W * sin(rad(self.inc)) / self.annulus) ** 0.5) * 1000  # critical buckling
        # Wbit = Wbha*BF* cos(rad(dta))+(0.8*Fcr)
        self.NB_Wbit = self.Total_Load * self.BF * cos(rad(self.inc)) - (0.8 * self.Fcr)  # allowable non buckling WOB

# TODO delete choice_numbers
#     def choice_numbers(self, choice_1):  # temporary
#         self.choice = choice_1
#         x = self.choice
#         return {choice_1 == 3.476: 1,
#                 choice_1 == 3.340: 2,
#                 choice_1 == 3.826: 3,
#                 choice_1 == 3.640: 4,
#                 choice_1 == 4.408: 5,
#                 choice_1 == 4.276: 6,
#                 choice_1 == 4.778: 7,
#                 choice_1 == 4.670: 8,
#                 choice_1 == 5.965: 9}[1]

# TODO delete dc_choice_numbers
    # def dc_choice_numbers(self, choice_1):  # temporary
    #     self.choice = choice_1
    #     x = self.choice
    #     return {choice_1 == 3.476: 1,
    #             choice_1 == 3.340: 2,
    #             choice_1 == 3.826: 3,
    #             choice_1 == 3.640: 4,
    #             choice_1 == 4.408: 5,
    #             choice_1 == 4.276: 6,
    #             choice_1 == 4.778: 7,
    #             choice_1 == 4.670: 8,
    #             choice_1 == 5.965: 9}[1]

    # def design(self, choice):  # temporary
    #     self.choice = choice
    #     x = self.choice
    #     '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
    #     return {x == 1: [4.0, 11.85, 3.476, 0.0, 8410, 0.0, 8600, 0.0, 231000, 17285, 33625],
    #             x == 2: [4.0, 14.0, 3.340, 8330, 11350, 7940, 10830, 209000, 285000, 20175, 33625],
    #             x == 3: [4.5, 16.6, 3.826, 7620, 10390, 7210, 9830, 242000, 331000, 22836, 37676],
    #             x == 4: [4.5, 20.0, 3.640, 9510, 12960, 9200, 12540, 302000, 412000, 27076, 44673],
    #             x == 5: [5.0, 16.25, 4.408, 0.0, 6970, 0.0, 7770, 0.0, 328000, 0, 0],
    #             x == 6: [5.0, 19.50, 4.276, 7390, 10000, 6970, 9500, 9000, 396000, 31084, 60338],
    #             x == 7: [5.5, 21.90, 4.778, 6610, 8440, 6320, 8610, 321000, 437000, 33560, 59091],
    #             x == 8: [5.5, 24.70, 4.670, 7670, 10460, 7260, 9900, 365000, 497000, 43490, 60338],
    #             x == 9: [6.625, 25.20, 5.965, 4010, 4810, 4790, 6540, 359000, 489000, 44196, 73661]}[1]

    # TODO delete new_drill_pipe_design
    # def new_drill_pipe_design(self, choice):
    #     self.choice = choice
    #     x = self.choice
    #     # '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
    #     # return {x == 1: [4.0, 11.85, 3.476, 0.0, 8410, 0.0, 8600, 0.0, 231000, 17285, 33625],
    #     #         x == 2: [4.0, 14.0, 3.340, 8330, 11350, 7940, 10830, 209000, 285000, 20175, 33625],
    #     #         x == 3: [4.5, 16.6, 3.826, 7620, 10390, 7210, 9830, 242000, 331000, 22836, 37676],
    #     #         x == 4: [4.5, 20.0, 3.640, 9510, 12960, 9200, 12540, 302000, 412000, 27076, 44673],
    #     #         x == 5: [5.0, 16.25, 4.408, 0.0, 6970, 0.0, 7770, 0.0, 328000, 0, 0],
    #     #         x == 6: [5.0, 19.50, 4.276, 7390, 10000, 6970, 9500, 9000, 396000, 31084, 60338],
    #     #         x == 7: [5.5, 21.90, 4.778, 6610, 8440, 6320, 8610, 321000, 437000, 33560, 59091],
    #     #         x == 8: [5.5, 24.70, 4.670, 7670, 10460, 7260, 9900, 365000, 497000, 43490, 60338],
    #     #         x == 9: [6.625, 25.20, 5.965, 4010, 4810, 4790, 6540, 359000, 489000, 44196, 73661]}[1]
    #     '''              OD      Wpf    ID    DCol  ECol     XCol  GCol   SCol  DYSmin EYSmin XYSmin GYSmin SYSmin  D_Torsion E_Torsion X_Torsion G_Torsion S_Torsion D_Torque E_Torque '''
    #     return {x == 1: [4.0,   11.85, 3.476, 0.0,  8410,  9978,  10708, 12618,  0.0,   8600,  10889, 12036, 15474,   0.0,      231000,  292290,   323057,   415360,   17285,   33625],
    #             x == 2: [4.0,   14.0,  3.340, 8330, 11350, 14382, 15896, 20141,  7940,  10830, 13716, 15159, 19491,   209000,   285000,  361454,   399502,   513646,   20175,   33625],
    #             x == 3: [4.5,   16.6,  3.826, 7620, 10390, 12765, 13825, 16773,  7210,  9830,  12450, 13761, 17693,   242000,   331000,  418707,   462781,   595004,   22836,   37676],
    #             x == 4: [4.5,   20.0,  3.640, 9510, 12960, 16421, 18149, 23333,  9200,  12540, 15886, 17558, 22575,   302000,   412000,  522320,   577301,   742244,   27076,   44673],
    #             x == 5: [5.0,   16.25, 4.408, 0.0,  6970,  8108,  8616,  9831,   0.0,   7770,  9842,  10878, 13986,   0.0,      328000,  415559,   459302,   590531,   0,       0],
    #             x == 6: [5.0,   19.50, 4.276, 7390, 10000, 12026, 12999, 15672,  6970,  9500,  12037, 13304, 17105,   9000,     396000,  501087,   553833,   712070,   31084,   60338],
    #             x == 7: [5.5,   21.90, 4.778, 6610, 8440,  10019, 10753, 12679,  6320,  8610,  10912, 12061, 15507,   321000,   437000,  553681,   611963,   786809,   33560,   59091],
    #             x == 8: [5.5,   24.70, 4.670, 7670, 10460, 12933, 14013, 17023,  7260,  9900,  12544, 13865, 17826,   365000,   497000,  629814,   696111,   894999,   43490,   60338],
    #             x == 9: [6.625, 25.20, 5.965, 4010, 4810,  5321,  5500,  6036,   4790,  6540,  8281,  9153,  11768,   359000,   489000,  619988,   685250,   881035,   44196,   73661]}[1]

    def new_drill_pipe_design_updated(self, choice):
        self.choice = choice
        x = self.choice
        '''              OD      Wpf    ID    DCol  ECol     XCol  GCol   SCol  DYSmin EYSmin XYSmin GYSmin SYSmin  D_Torsion E_Torsion X_Torsion G_Torsion S_Torsion D_Torque E_Torque '''
        return {x == 1: [4.0,   11.85, 3.476, 0.0,  8410,  9978,  10708, 12618,  0.0,   8600,  10889, 12036, 15474,   0.0,      231000,  292290,   323057,   415360,   17285,   33625],
                x == 2: [4.0,   14.0,  3.340, 8330, 11350, 14382, 15896, 20141,  7940,  10830, 13716, 15159, 19491,   209000,   285000,  361454,   399502,   513646,   20175,   33625],
                x == 3: [4.5,   16.6,  3.826, 7620, 10390, 12765, 13825, 16773,  7210,  9830,  12450, 13761, 17693,   242000,   331000,  418707,   462781,   595004,   22836,   37676],
                x == 4: [4.5,   20.0,  3.640, 9510, 12960, 16421, 18149, 23333,  9200,  12540, 15886, 17558, 22575,   302000,   412000,  522320,   577301,   742244,   27076,   44673],
                x == 5: [5.0,   16.25, 4.408, 0.0,  6970,  8108,  8616,  9831,   0.0,   7770,  9842,  10878, 13986,   0.0,      328000,  415559,   459302,   590531,   0,       0],
                x == 6: [5.0,   19.50, 4.276, 7390, 10000, 12026, 12999, 15672,  6970,  9500,  12037, 13304, 17105,   9000,     396000,  501087,   553833,   712070,   31084,   60338],
                x == 7: [5.5,   21.90, 4.778, 6610, 8440,  10019, 10753, 12679,  6320,  8610,  10912, 12061, 15507,   321000,   437000,  553681,   611963,   786809,   33560,   59091],
                x == 8: [5.5,   24.70, 4.670, 7670, 10460, 12933, 14013, 17023,  7260,  9900,  12544, 13865, 17826,   365000,   497000,  629814,   696111,   894999,   43490,   60338],
                x == 9: [6.625, 25.20, 5.965, 4010, 4810,  5321,  5500,  6036,   4790,  6540,  8281,  9153,  11768,   359000,   489000,  619988,   685250,   881035,   44196,   73661]}[1]
    # add the torque properties for X, G and S

# TODO premium_drill_pipe_design
    # def premium_drill_pipe_design(self, choice):
    #     self.choice = choice
    #     x = self.choice
    #     '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
    #     return {x == 1: [4.0, 11.85, 3.476, 0.0, 8410, 0.0, 8600, 0.0, 231000, 17285, 33625],
    #             x == 2: [4.0, 14.0, 3.340, 8330, 11350, 7940, 10830, 209000, 285000, 20175, 33625],
    #             x == 3: [4.5, 16.6, 3.826, 7620, 10390, 7210, 9830, 242000, 331000, 22836, 37676],
    #             x == 4: [4.5, 20.0, 3.640, 9510, 12960, 9200, 12540, 302000, 412000, 27076, 44673],
    #             x == 5: [5.0, 16.25, 4.408, 0.0, 6970, 0.0, 7770, 0.0, 328000, 0, 0],
    #             x == 6: [5.0, 19.50, 4.276, 7390, 10000, 6970, 9500, 9000, 396000, 31084, 60338],
    #             x == 7: [5.5, 21.90, 4.778, 6610, 8440, 6320, 8610, 321000, 437000, 33560, 59091],
    #             x == 8: [5.5, 24.70, 4.670, 7670, 10460, 7260, 9900, 365000, 497000, 43490, 60338],
    #             x == 9: [6.625, 25.20, 5.965, 4010, 4810, 4790, 6540, 359000, 489000, 44196, 73661]}[1]

    def premium_drill_pipe_design_updated(self, choice):
        self.choice = choice
        x = self.choice

        '''          OD      Wpf    ID    DCol  ECol   XCol   GCol   SCol  DYSmin EYSmin  XYSmin GYSmin  SYSmin D_Torsion E_Torsion X_Torsion G_Torsion S_Torsion D_Torque E_Torque '''
        return {
            x == 1: [4.0,   11.85, 3.476, 0.0,  8410,  6508,  6827,  7445,  0.0,  8600,   9956,   11004, 14148,   0.0,      231000,    230554,   254823,   327630,  17285, 33625],
            x == 2: [4.0,   14.0,  3.340, 8330, 11350, 10795, 11622, 13836, 7940, 10830,  12540,  13860, 17820,   209000,   285000,    283963,   313854,   403527,  20175, 33625],
            x == 3: [4.5,   16.6,  3.826, 7620, 10390, 8868,  9467,  10964, 7210, 9830,   11383,  12581, 16176,   242000,   331000,    329542,   364231,   468297,  22836, 37676],
            x == 4: [4.5,   20.0,  3.640, 9510, 12960, 13901, 15350, 18806, 9200, 12540,  14524,  16053, 20640,   302000,   412000,    409026,   452082,   581248,  27076, 44673],
            x == 5: [5.0,   16.25, 4.408, 0.0,  6970,  4935,  5067,  5661,  0.0,  7770,   8998,   9946,  12787,   0.0,      328000,    328263,   362817,   466479,  0,     0],
            x == 6: [5.0,   19.50, 4.276, 7390, 10000, 8241,  8765,  10029, 6970, 9500,   11005,  12163, 15638,   9000,     396000,    394612,   436150,   560764,  31084, 60338],
            x == 7: [5.5,   21.90, 4.778, 6610, 8440,  6542,  6865,  7496,  6320, 8610,   9977,   11027, 14177,   321000,   437000,    436721,   482692,   620604,  33560, 59091],
            x == 8: [5.5,   24.70, 4.670, 7670, 10460, 9011,  9626,  11177, 7260, 9900,   11469,  12676, 16298,   365000,   497000,    495627,   547799,   704313,  43490, 60338],
            x == 9: [6.625, 25.20, 5.965, 4010, 4810,  3252,  3353,  3429,  4790, 6540,   7571,   8368,  10759,   359000,   489000,    490790,   542452,   697438,  44196, 73661]}[1]

        # update D and E parameters for premium design and add torque properties for X, G, and S

# TODO delete regular_drill_pipe_design
    # def regular_drill_pipe_design(self, choice):
    #     self.choice = choice
    #     x = self.choice
    #     '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
    #     return {x == 1: [4.0, 11.85, 3.476, 0.0, 8410, 0.0, 8600, 0.0, 231000, 17285, 33625],
    #             x == 2: [4.0, 14.0, 3.340, 8330, 11350, 7940, 10830, 209000, 285000, 20175, 33625],
    #             x == 3: [4.5, 16.6, 3.826, 7620, 10390, 7210, 9830, 242000, 331000, 22836, 37676],
    #             x == 4: [4.5, 20.0, 3.640, 9510, 12960, 9200, 12540, 302000, 412000, 27076, 44673],
    #             x == 5: [5.0, 16.25, 4.408, 0.0, 6970, 0.0, 7770, 0.0, 328000, 0, 0],
    #             x == 6: [5.0, 19.50, 4.276, 7390, 10000, 6970, 9500, 9000, 396000, 31084, 60338],
    #             x == 7: [5.5, 21.90, 4.778, 6610, 8440, 6320, 8610, 321000, 437000, 33560, 59091],
    #             x == 8: [5.5, 24.70, 4.670, 7670, 10460, 7260, 9900, 365000, 497000, 43490, 60338],
    #             x == 9: [6.625, 25.20, 5.965, 4010, 4810, 4790, 6540, 359000, 489000, 44196, 73661]}[1]

    def class2_drill_pipe_design_updated(self, choice):
        self.choice = choice
        x = self.choice

        '''          OD      Wpf    ID    DCol  ECol   XCol   GCol   SCol  DYSmin EYSmin  XYSmin GYSmin  SYSmin  D_Torsion E_Torsion X_Torsion G_Torsion S_Torsion D_Torque E_Torque '''
        return {
            x == 1: [4.0,   11.85, 3.476, 0.0,  4311,  4702,  4876,  5436,  0.0,   6878,  8712,   9629,   12380,  0.0,      158132,    200301,   221385,   284638,  17285, 33625],
            x == 2: [4.0,   14.0,  3.340, 8330, 7295,  8570,  9134,  10520, 7940,  8663,  10973,  12128,  15593,  209000,   194363,    246193,   272108,   349852,  20175, 33625],
            x == 3: [4.5,   16.6,  3.826, 7620, 5951,  6828,  7185,  7923,  7210,  7863,  9960,   11009,  14154,  242000,   225771,    285977,   316080,   406388,  22836, 37676],
            x == 4: [4.5,   20.0,  3.640, 9510, 9631,  11598, 12520, 15033, 9200,  10033, 12709,  14047,  18060,  302000,   279502,    354035,   391302,   503103,  27076, 44673],
            x == 5: [5.0,   16.25, 4.408, 0.0,  3275,  3696,  3850,  4065,  0.0,   6216,  7874,   8702,   11189,  0.0,      225316,    285400,   315442,   405568,  0,     0],
            x == 6: [5.0,   19.50, 4.276, 7390, 5514,  6262,  6552,  7079,  6970,  7602,  9629,   10643,  13684,  9000,     270432,    342548,   378605,   486778,  31084, 60338],
            x == 7: [5.5,   21.90, 4.778, 6610, 4334,  4733,  4899,  5465,  6320,  6892,  8730,   9649,   12405,  321000,   299533,    379409,   419346,   539160,  33560, 59091],
            x == 8: [5.5,   24.70, 4.670, 7670, 6050,  6957,  7329,  8115,  7260,  7923,  10035,  11092,  14261,  365000,   339533,    430076,   475347,   611160,  43490, 60338],
            x == 9: [6.625, 25.20, 5.965, 4010, 2227,  2343,  2346,  2346,  4790,  5230,  6625,   7322,   9414,   359000,   337236,    427166,   472131,   607026,  44196, 73661]}[1]
        # update D parameters for class 2 design and add torque properties for X, G, and S

    def drill_collar_design(self, choice):
        self.choice = choice
        x = self.choice
        '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
        return {x == 1: [4.0, 11.85, 3.476, 0.0, 8410, 0.0, 8600, 0.0, 231000, 17285, 33625],
                x == 2: [4.0, 14.0, 3.340, 8330, 11350, 7940, 10830, 209000, 285000, 20175, 33625],
                x == 3: [4.5, 16.6, 3.826, 7620, 10390, 7210, 9830, 242000, 331000, 22836, 37676],
                x == 4: [4.5, 20.0, 3.640, 9510, 12960, 9200, 12540, 302000, 412000, 27076, 44673],
                x == 5: [5.0, 16.25, 4.408, 0.0, 6970, 0.0, 7770, 0.0, 328000, 0, 0],
                x == 6: [5.0, 19.50, 4.276, 7390, 10000, 6970, 9500, 9000, 396000, 31084, 60338],
                x == 7: [5.5, 21.90, 4.778, 6610, 8440, 6320, 8610, 321000, 437000, 33560, 59091],
                x == 8: [5.5, 24.70, 4.670, 7670, 10460, 7260, 9900, 365000, 497000, 43490, 60338],
                x == 9: [6.625, 25.20, 5.965, 4010, 4810, 4790, 6540, 359000, 489000, 44196, 73661]}[1]

    def drill_collar_design_updated(self, choice):
        self.choice = choice
        x = self.choice
        '''                     OD    Wpf   ID  DCol_Pres  ECol_Pres DYSmin EYSmin D_Torsion E_Torsion D_Torque E_Torque '''
        return {x == 1: [4.0, 32.0, 2.0],
                x == 2: [4.0, 29.0, 2.25],
                x == 3: [4.5, 43.0, 2.0],
                x == 4: [4.5, 41.0, 2.25],
                x == 5: [5.0, 53, 2.25],
                x == 6: [5.0, 50, 2.5],
                x == 7: [5.5, 67, 2.25],
                x == 8: [5.5, 64, 2.5],
                x == 9: [6.0, 72.0, 3.0]}[1]

    def nominal(self, choice):
        self.choice = choice
        x = self.choice
        return {x == 1: [11.85],
                x == 2: [14.0],
                x == 3: [16.6],
                x == 4: [20.0],
                x == 5: [16.25],
                x == 6: [19.50],
                x == 7: [21.90],
                x == 8: [24.70],
                x == 9: [25.20]}[1]

    def printer(self):
        print("Collapse Pressure  :           ", self.Col_Pres, "  psi \n")
        print("Measured Depth  :              ", self.MD, "  ft\n")
        print("Margin of Overpull  :          ", self.MOP, "lbf \n")
        print("Total_Load  :                  ", self.Total_Load, "  lbf \n")
        print("Load @ Surface  :              ", self.Act_Load_Top, "   lbf \n")
        print("Bouyancy Factor  :             ", self.BF, "\n")
        print("Max Allowable Load  :          ", self.Max_Allw_Load, "   lbf\n")
        print("Horse Power (Rotation)  :      ", self.HP, "  hp \n")
        print("Torque  :                      ", self.Torq, "  ft-lbf \n")
        print("Torsion Yield (Tension)  :     ", self.Min_Tors_Yd_UnTen, "  ft-lbf  \n")
        print("Pipe Stretch (Own Wgt)         ", self.Stretch, " inches \n")
        print("Shear_Stress  :                ", self.Shear_Stress, "  psi  \n")
        print("Max_Shear_Stress  :            ", self.Max_Shear_Stress, "  psi \n")
        print("Crit_Vibr (Whirl)              ", self.Crit_Vibr, "  rpm \n")
        print("Crit_Buckling Compresv_Load :  ", self.Fcr, "  lbf \n")
        print("Max_Non-Buckling WOB:          ", self.NB_Wbit, "  lbf \n")
        print("Planned Max WOB_Use:           ", self.DC_Weight_use, "  lbf \n")
        print("Len of Drill Colar :           ", self.Len_dc, "  ft \n")
        if self.Lnp < self.Len_dc:
            print("Len of Neutral point:          ", self.Lnp, "  ft   PASSED \n")
        elif self.Lnp > self.Len_dc:
            print("Len of Neutral point:          ", self.Lnp, "  ft   FAILED \n")

        if (self.Len_dc * self.Wght_dc) * self.BF > (self.Wght_dp * self.Len_dp) * self.BF:
            print("     TENSION TEST PASSED ")
            print("BOUYED DC_Weight :          ", (self.Len_dc * self.Wght_dc) * self.BF, "  lb \n")
            print("BOUYED DP_Weight :          ", (self.Wght_dp * self.Len_dp) * self.BF, "  lb \n")
        else:
            print("     TENSION TEST FAILED ")
            print("BOUYED DC_Weight :          ", (self.Len_dc * self.Wght_dc) * self.BF, "  lb \n")
            print("BOUYED DP_Weight :          ", (self.Wght_dp * self.Len_dp) * self.BF, "  lb \n")