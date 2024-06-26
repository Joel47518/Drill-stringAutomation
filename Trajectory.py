import math
import matplotlib.pyplot as plt

cos = math.cos
sin = math.sin
tan = math.tan
atan = math.atan
asin = math.asin
acos = math.acos
degree = math.degrees
radian = math.radians
pi = math.pi




def build_and_hold(bur_, kop_, northings, eastings, tvd_target_):
    bur = float(bur_)
    KOP = float(kop_)
    TVD_target = float(tvd_target_)
    northings = float(northings)
    eastings = float(eastings)

    # Horizontal displacement to target
    Ht = (northings ** 2 + eastings ** 2) ** 0.5
    # print(f'Ht: {Ht}')

    # Calculation of Radius of curvature
    R = 18000 / (pi * bur)
    # print(f'R: {R}')

    # Calculation of maximum inclination
    x = degree(atan((Ht - R) / (TVD_target - KOP)))
    # print(f'x: {x}')

    y = degree(asin((R * cos(radian(x))) / (TVD_target - KOP)))
    # print(f'y: {y}')

    max_inclination = x + y
    # print(f'Max inclination: {max_inclination}')

    # Calculating the TVD at the build up section (BE)
    BE = R * sin(radian(max_inclination))
    # print(f'BE: {BE}')

    # Calculating the horizontal displacement to EOB
    Horizontal_displacement_EOB = R * (1 - cos(radian(max_inclination)))
    # print(f'HD_EOB: {Horizontal_displacement_EOB}')

    # Calculating the TVD at EOB
    TVD_EOB = KOP + BE
    # print(f'TVD_EOB: {TVD_EOB}')

    # Calculating the measured depth at EOB
    MD_EOB = KOP + 100 * max_inclination / bur
    # print(f'MD_EOB: {MD_EOB}')

    # Calculating the measured depth at tangent section
    MD_tangent = (TVD_target - TVD_EOB) / cos(radian(max_inclination))
    # print(f'MD_tangent: {MD_tangent}')

    # Calculating the measured depth at target
    MD_target = MD_EOB + MD_tangent
    # print(f'MD_target: {MD_target}')

    TVD = []
    HD = []

    for tvd in range(0, int(TVD_target + 1), 10):
        incremental_tvd = 0
        incremental_hd = 0
        if tvd < KOP:
            incremental_tvd = tvd
            incremental_hd = 0
        elif tvd >= KOP and tvd < TVD_EOB:
            inclination = degree(asin((tvd - KOP) / R))
            incremental_hd = R * (1 - cos(radian(inclination)))
            incremental_tvd = tvd
        elif tvd >= TVD_EOB:
            incremental_hd = incremental_hd = R * (1 - cos(radian(inclination))) + (tvd - TVD_EOB) * tan(
                radian(max_inclination))
            incremental_tvd = tvd
        TVD.append(incremental_tvd)
        HD.append(incremental_hd)

    return HD, TVD, MD_target


def build_hold_and_drop(tvd_target_, kop_, bur_, tvd_eod_, dor_, a2_, hd_):
    Ht = float(hd_) # do the calculation of Ht here
    Vt = float(tvd_target_)
    Vb = float(kop_)
    Ve = float(tvd_eod_)
    bur = float(bur_)
    dor = float(dor_)
    a2 = float(a2_)

    # Calculating the Radius of Curvatures
    R1 = 18000 / (pi * bur)
    R2 = 18000 / (pi * dor)

    # Calculating the unknown vertical and horizontal distances OQ, OP, QS, PQ and PS
    OQ = Ht - R1 - (R2 * cos(radian(a2))) - ((Vt - Ve) * tan(radian(a2)))

    OP = Ve - Vb + R2 * sin(radian(a2))

    QS = R1 + R2

    PQ = (OP ** 2 + OQ ** 2) ** 0.5

    PS = (PQ ** 2 - QS ** 2) ** 0.5

    # Calculating  the angles x, y and a1
    x = degree(atan(OQ / OP))

    y = degree(atan(QS / PS))

    a1 = x + y

    # Calculating the distances and displacements at point C
    Vc = Vb + R1 * sin(radian(a1))

    Hc = R1 * (1 - cos(radian(a1)))

    MDc = Vb + (100 * a1 / bur)

    # Calculating the distances and displacements at point D
    Vd = Vc + PS * cos(radian(a1))

    Hd = Hc + PS * sin(radian(a1))

    MDd = MDc + PS

    # Calculating the distances and displacements at point E
    He = Hd + (R2 * (cos(radian(a2)) - cos(radian(a1))))

    MDe = MDd + (100 * (a1 - a2) / dor)

    # Calculating the measured displacement to target, T
    MD_target = MDe + ((Vt - Ve) / cos(radian(a2)))

    TVD = []
    HD = []

    for tvd in range(0, int(Vt + 1), 10):
        incremental_tvd = 0
        incremental_hd = 0
        if tvd < Vb:  # straight section            Vb = tvd at kop
            incremental_tvd = tvd
            incremental_hd = 0
        elif tvd >= Vb and tvd < Vc:  # build section       Vc = TVD at EOB
            inclination = degree(asin((tvd - Vb) / R1))
            incremental_hd = R1 * (1 - cos(radian(inclination)))
            # incremental_hd = R1 * (1 - cos(radian(a1)))
            incremental_tvd = tvd
        elif tvd >= Vc and tvd < Vd:  # hold or tangent section
            incremental_hd = incremental_hd = R1 * (1 - cos(radian(inclination))) + (tvd - Vc) * tan(radian(a1))
            incremental_tvd = tvd
        elif tvd >= Vd and tvd <= Ve:  # drop build
            incremental_tvd = tvd
            incremental_hd = (R1 + OQ) + math.sqrt((R2 ** 2) - (((Vb + OP) - tvd) ** 2))
            # find the horizontal displacement for the drop
        else:  # drop tangent
            TVD.append(Vt)
            HD.append(Ht)
            break
        TVD.append(incremental_tvd)
        HD.append(incremental_hd)

    return HD, TVD, MD_target


def deep_kick_off(tvd_target_, kop_, hd_):
    Ht = float(hd_)
    TVD_target = float(tvd_target_)
    KOP = float(kop_)
    a1 = 0

    # Calculating the final inclination, a2
    a2 = 2 * degree(atan(Ht / (TVD_target - KOP)))
    # print(f'a2: {a2}')

    # Calculating the Radius of the Curvature
    R = (TVD_target - KOP) / (sin(radian(a2)))
    # print(f'R: {R}')

    # Calculating the displacement BT
    BT = (2 * pi * (TVD_target - KOP) / sin(radian(a2))) * (a2 / 360)
    # print(f'BT: {BT}')

    # Calculating the build up rate, bur
    bur = 18000 / (pi * R)
    # print(f'bur: {bur}')

    # Calculating the measured displacement to target, MDt
    MDt = KOP + (a2 / bur) * 100
    # print(f'MDt: {MDt}')

    TVD = []
    HD = []

    for tvd in range(0, int(TVD_target + 1), 10):
        incremental_tvd = 0
        incremental_hd = 0
        if tvd < KOP:
            incremental_tvd = tvd
            incremental_hd = 0
        elif tvd >= KOP:
            inclination = degree(asin((tvd - KOP) / R))
            incremental_hd = R * (1 - cos(radian(inclination)))
            incremental_tvd = tvd
        HD.append(incremental_hd)
        TVD.append(incremental_tvd)

    plt.plot(HD, TVD)
    plt.gca().invert_yaxis()
    plt.show()

#
# print("The Optimal Profile Is:: ")
# if bur.lower() == "n":
#     print("DEEP KICK-OFF")
#     deep_kick_off(tvd_target, kop, hd)
#     print("The Optimal Profile Is:: ")
#     print("DEEP KICK-OFF")
# elif tc.lower() == "n":
#     print("BUILD_HOLD AND DROP")
#     build_hold_and_drop(tvd_target, kop, bur, tvd_eod, dor, a2, hd)
#     print("The Optimal Profile Is:: ")
#     print("BUILD_HOLD AND DROP")
# else:
#     print("BUILD AND HOLD")
#     build_and_hold(bur, kop, tc, tvd_target)
#     print("The Optimal Profile Is:: ")
#     print("BUILD AND HOLD")
