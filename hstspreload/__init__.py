"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2021.6.21"
__checksum__ = "fbcf47d7968dfe4992fa4b64e95092cdf810111da89a6ac40c9fdd14fc8d6293"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), (16, 9), (25, 61), (86, 26), (112, 12), None, (124, 19), (143, 22), (165, 7), (172, 20), (192, 18), None, (210, 29), (239, 45), (284, 7), (291, 9), (300, 36), (336, 16), (352, 10), (362, 28), None, (390, 54), (444, 8), (452, 18), (470, 19), (489, 13), (502, 14), (516, 14), None, None, (530, 29), (559, 20), (579, 35), (614, 14), (628, 24), (652, 9), None, (661, 25), (686, 27), (713, 8), (721, 13), None, None, (734, 17), (751, 6), (757, 26), (783, 5), (788, 5), (793, 19), (812, 14), (826, 11), (837, 12), (849, 27), None, (876, 11), (887, 11), (898, 7), (905, 29), (934, 18), (952, 27), (979, 46), (1025, 25), (1050, 16), (1066, 8), (1074, 5), (1079, 22), (1101, 18), None, (1119, 36), (1155, 15), (1170, 8), (1178, 11), None, (1189, 5), (1194, 16), (1210, 14), (1224, 18), None, (1242, 14), (1256, 18), (1274, 48), (1322, 19), (1341, 5), (1346, 59), (1405, 14), (1419, 14), (1433, 20), None, (1453, 10), (1463, 13), (1476, 15), (1491, 19), None, (1510, 13), (1523, 19), (1542, 11), (1553, 4), (1557, 22), (1579, 10), (1589, 7), (1596, 14), (1610, 21), (1631, 11), (1642, 21), (1663, 12), (1675, 32), None, (1707, 10), (1717, 14), (1731, 12), (1743, 45), (1788, 15), None, (1803, 11), (1814, 23), (1837, 21), (1858, 26), (1884, 6), (1890, 6), (1896, 7), (1903, 5), (1908, 20), (1928, 23), (1951, 24), (1975, 13), (1988, 15), (2003, 19), (2022, 6), (2028, 61), (2089, 44), (2133, 12), (2145, 23), (2168, 16), (2184, 38), (2222, 6), (2228, 12), (2240, 44), (2284, 6), (2290, 41), (2331, 13), (2344, 23), (2367, 30), (2397, 16), (2413, 8), (2421, 15), (2436, 12), (2448, 19), (2467, 21), (2488, 15), None, (2503, 35), (2538, 21), (2559, 17), (2576, 19), (2595, 26), (2621, 5), (2626, 37), (2663, 26), (2689, 16), (2705, 10), (2715, 17), (2732, 23), (2755, 14), (2769, 17), (2786, 8), (2794, 8), (2802, 7), (2809, 29), (2838, 6), (2844, 18), (2862, 27), (2889, 20), (2909, 17), (2926, 19), (2945, 12), (2957, 40), (2997, 40), (3037, 12), (3049, 48), (3097, 25), (3122, 12), None, (3134, 8), (3142, 25), (3167, 19), (3186, 6), (3192, 23), None, (3215, 30), (3245, 33), (3278, 14), (3292, 12), (3304, 27), None, (3331, 26), (3357, 41), (3398, 50), (3448, 15), (3463, 20), (3483, 15), (3498, 21), (3519, 32), (3551, 24), (3575, 20), (3595, 17), (3612, 60), (3672, 19), (3691, 9), (3700, 12), (3712, 12), (3724, 11), (3735, 10), (3745, 48), (3793, 32), None, (3825, 25), (3850, 23), None, (3873, 8), (3881, 8), (3889, 7), None, (3896, 25), (3921, 17), None, (3938, 21), (3959, 35), (3994, 21), (4015, 10), (4025, 36), (4061, 20), (4081, 22), (4103, 23), (4126, 19), (4145, 12), (4157, 5), (4162, 30), (4192, 24), (4216, 14), (4230, 14), (4244, 47), (4291, 52), None, None, (4343, 51), (4394, 42), None, (4436, 14), None, (4450, 15), (4465, 8), (4473, 21), (4494, 6), (4500, 16), (4516, 17)], [(4533, 8024), (12557, 8617), (21174, 9054), (30228, 7688), (37916, 8117), (46033, 7920), (53953, 8781), (62734, 7741), (70475, 8706), (79181, 7956), (87137, 9309), (96446, 7829), (104275, 8567), (112842, 9788), (122630, 8246), (130876, 8569), (139445, 8927), (148372, 7908), (156280, 8202), (164482, 7931), (172413, 8670), (181083, 8318), (189401, 8784), (198185, 8081), (206266, 8575), (214841, 8198), (223039, 8660), (231699, 8829), (240528, 7945), (248473, 8375), (256848, 8625), (265473, 8166), (273639, 8332), (281971, 8788), (290759, 7675), (298434, 8574), (307008, 8294), (315302, 8961), (324263, 8607), (332870, 8687), (341557, 9319), (350876, 7920), (358796, 8005), (366801, 8079), (374880, 8190), (383070, 8160), (391230, 8270), (399500, 9156), (408656, 8145), (416801, 7814), (424615, 8166), (432781, 8638), (441419, 8727), (450146, 8620), (458766, 8752), (467518, 8371), (475889, 8745), (484634, 8239), (492873, 8743), (501616, 7369), (508985, 8349), (517334, 8434), (525768, 8353), (534121, 8679), (542800, 8513), (551313, 8778), (560091, 8080), (568171, 9018), (577189, 8853), (586042, 8535), (594577, 8323), (602900, 7994), (610894, 7565), (618459, 8727), (627186, 8485), (635671, 9036), (644707, 7801), (652508, 8904), (661412, 8710), (670122, 7868), (677990, 8779), (686769, 7212), (693981, 8293), (702274, 8703), (710977, 8057), (719034, 8438), (727472, 9021), (736493, 8371), (744864, 8679), (753543, 8539), (762082, 9457), (771539, 7866), (779405, 8271), (787676, 8276), (795952, 8302), (804254, 8987), (813241, 8709), (821950, 8105), (830055, 8166), (838221, 7945), (846166, 7985), (854151, 8501), (862652, 8216), (870868, 8112), (878980, 7936), (886916, 8901), (895817, 8980), (904797, 8829), (913626, 9560), (923186, 8821), (932007, 8723), (940730, 8774), (949504, 8416), (957920, 8273), (966193, 8645), (974838, 8720), (983558, 8330), (991888, 8021), (999909, 8167), (1008076, 9053), (1017129, 8839), (1025968, 8846), (1034814, 8485), (1043299, 8707), (1052006, 9479), (1061485, 8197), (1069682, 7609), (1077291, 9012), (1086303, 8377), (1094680, 10068), (1104748, 8959), (1113707, 7952), (1121659, 8630), (1130289, 8391), (1138680, 8137), (1146817, 8560), (1155377, 8035), (1163412, 8890), (1172302, 8048), (1180350, 8282), (1188632, 8619), (1197251, 8646), (1205897, 7720), (1213617, 8160), (1221777, 8866), (1230643, 8143), (1238786, 8320), (1247106, 8313), (1255419, 8052), (1263471, 8801), (1272272, 8570), (1280842, 8592), (1289434, 8805), (1298239, 8073), (1306312, 8455), (1314767, 8602), (1323369, 8188), (1331557, 8453), (1340010, 8059), (1348069, 7563), (1355632, 7767), (1363399, 8662), (1372061, 9150), (1381211, 8185), (1389396, 8171), (1397567, 9096), (1406663, 8325), (1414988, 7984), (1422972, 8804), (1431776, 8401), (1440177, 7427), (1447604, 8371), (1455975, 9728), (1465703, 7860), (1473563, 7952), (1481515, 8868), (1490383, 8334), (1498717, 8865), (1507582, 8167), (1515749, 7903), (1523652, 10455), (1534107, 8763), (1542870, 8272), (1551142, 8626), (1559768, 9364), (1569132, 9370), (1578502, 7771), (1586273, 8632), (1594905, 8011), (1602916, 8381), (1611297, 9125), (1620422, 8080), (1628502, 8684), (1637186, 8619), (1645805, 8352), (1654157, 8382), (1662539, 8164), (1670703, 8216), (1678919, 8537), (1687456, 8137), (1695593, 8579), (1704172, 7945), (1712117, 8901), (1721018, 8444), (1729462, 9046), (1738508, 8856), (1747364, 7556), (1754920, 8859), (1763779, 8179), (1771958, 8578), (1780536, 8662), (1789198, 8825), (1798023, 8434), (1806457, 8751), (1815208, 8590), (1823798, 8277), (1832075, 8424), (1840499, 8146), (1848645, 8567), (1857212, 8739), (1865951, 8526), (1874477, 7790), (1882267, 9438), (1891705, 8314), (1900019, 8368), (1908387, 8367), (1916754, 8329), (1925083, 7786), (1932869, 8763), (1941632, 8451), (1950083, 9051), (1959134, 8399), (1967533, 7973), (1975506, 8957), (1984463, 8421), (1992884, 9256), (2002140, 7998), (2010138, 8142), (2018280, 7507), (2025787, 8787), (2034574, 8798), (2043372, 8978), (2052350, 8160), (2060510, 8528), (2069038, 8174), (2077212, 8899), (2086111, 8174), (2094285, 7788), (2102073, 8293), (2110366, 7884), (2118250, 8642), (2126892, 8958), (2135850, 8830), (2144680, 8078), (2152758, 8340), (2161098, 8467)], [(2169565, 933), (2170498, 734), (2171232, 811), (2172043, 1010), (2173053, 660), (2173713, 838), (2174551, 694), (2175245, 1000), (2176245, 721), (2176966, 789), (2177755, 656), (2178411, 660), (2179071, 827), (2179898, 885), (2180783, 1067), (2181850, 1021), (2182871, 1363), (2184234, 736), (2184970, 1008), (2185978, 873), (2186851, 791), (2187642, 916), (2188558, 1017), (2189575, 811), (2190386, 811), (2191197, 716), (2191913, 1099), (2193012, 1327), (2194339, 818), (2195157, 869), (2196026, 1095), (2197121, 892), (2198013, 697), (2198710, 842), (2199552, 997), (2200549, 985), (2201534, 847), (2202381, 891), (2203272, 832), (2204104, 1207), (2205311, 726), (2206037, 963), (2207000, 807), (2207807, 784), (2208591, 780), (2209371, 561), (2209932, 1086), (2211018, 1027), (2212045, 919), (2212964, 619), (2213583, 937), (2214520, 734), (2215254, 855), (2216109, 1109), (2217218, 1094), (2218312, 593), (2218905, 767), (2219672, 680), (2220352, 728), (2221080, 892), (2221972, 915), (2222887, 859), (2223746, 1159), (2224905, 1078), (2225983, 857), (2226840, 810), (2227650, 809), (2228459, 511), (2228970, 719), (2229689, 640), (2230329, 826), (2231155, 1001), (2232156, 689), (2232845, 880), (2233725, 700), (2234425, 797), (2235222, 735), (2235957, 775), (2236732, 882), (2237614, 586), (2238200, 919), (2239119, 724), (2239843, 991), (2240834, 701), (2241535, 804), (2242339, 568), (2242907, 778), (2243685, 859), (2244544, 943), (2245487, 875), (2246362, 1092), (2247454, 1262), (2248716, 919), (2249635, 943), (2250578, 865), (2251443, 554), (2251997, 996), (2252993, 906), (2253899, 675), (2254574, 738), (2255312, 848), (2256160, 1042), (2257202, 980), (2258182, 608), (2258790, 696), (2259486, 940), (2260426, 533), (2260959, 589), (2261548, 1060), (2262608, 1032), (2263640, 821), (2264461, 852), (2265313, 803), (2266116, 801), (2266917, 880), (2267797, 856), (2268653, 731), (2269384, 627), (2270011, 801), (2270812, 744), (2271556, 1153), (2272709, 757), (2273466, 904), (2274370, 568), (2274938, 801), (2275739, 914), (2276653, 931), (2277584, 1072), (2278656, 767), (2279423, 1079), (2280502, 925), (2281427, 653), (2282080, 939), (2283019, 787), (2283806, 990), (2284796, 828), (2285624, 777), (2286401, 776), (2287177, 814), (2287991, 706), (2288697, 760), (2289457, 744), (2290201, 824), (2291025, 651), (2291676, 605), (2292281, 637), (2292918, 750), (2293668, 701), (2294369, 824), (2295193, 715), (2295908, 815), (2296723, 602), (2297325, 618), (2297943, 893), (2298836, 789), (2299625, 761), (2300386, 818), (2301204, 1084), (2302288, 847), (2303135, 664), (2303799, 1096), (2304895, 903), (2305798, 720), (2306518, 840), (2307358, 993), (2308351, 719), (2309070, 745), (2309815, 706), (2310521, 756), (2311277, 799), (2312076, 900), (2312976, 677), (2313653, 993), (2314646, 825), (2315471, 939), (2316410, 897), (2317307, 793), (2318100, 630), (2318730, 792), (2319522, 802), (2320324, 2005), (2322329, 626), (2322955, 843), (2323798, 751), (2324549, 1088), (2325637, 913), (2326550, 863), (2327413, 666), (2328079, 704), (2328783, 947), (2329730, 638), (2330368, 637), (2331005, 902), (2331907, 814), (2332721, 985), (2333706, 854), (2334560, 810), (2335370, 763), (2336133, 908), (2337041, 781), (2337822, 961), (2338783, 757), (2339540, 896), (2340436, 688), (2341124, 846), (2341970, 675), (2342645, 981), (2343626, 992), (2344618, 768), (2345386, 1080), (2346466, 780), (2347246, 933), (2348179, 1006), (2349185, 1146), (2350331, 945), (2351276, 866), (2352142, 1006), (2353148, 810), (2353958, 633), (2354591, 490), (2355081, 908), (2355989, 827), (2356816, 618), (2357434, 1117), (2358551, 623), (2359174, 824), (2359998, 969), (2360967, 997), (2361964, 925), (2362889, 746), (2363635, 962), (2364597, 797), (2365394, 971), (2366365, 674), (2367039, 700), (2367739, 619), (2368358, 698), (2369056, 486), (2369542, 900), (2370442, 1067), (2371509, 926), (2372435, 751), (2373186, 724), (2373910, 709), (2374619, 1046), (2375665, 616), (2376281, 625), (2376906, 1007), (2377913, 497), (2378410, 990), (2379400, 2201), (2381601, 727), (2382328, 785), (2383113, 1003), (2384116, 1151), (2385267, 515)], [(2385782, 48), None, (2385830, 35), (2385865, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (2385907, 42), None, (2385949, 25), (2385974, 44), (2386018, 22), (2386040, 18), None, None, None, None, (2386058, 26), None, None, None, None, (2386084, 21), (2386105, 25), None, None, (2386130, 26), None, None, None, None, (2386156, 71), (2386227, 21), (2386248, 23), None, None, None, None, (2386271, 48), None, None, None, None, None, (2386319, 31), None, None, None, None, (2386350, 42), None, (2386392, 22), None, (2386414, 21), None, (2386435, 26), (2386461, 42), None, None, (2386503, 77), (2386580, 27), None, None, None, None, (2386607, 21), (2386628, 21), None, None, (2386649, 34), (2386683, 42), None, None, None, (2386725, 25), None, None, (2386750, 21), None, None, None, None, None, (2386771, 24), (2386795, 21), None, None, (2386816, 26), None, (2386842, 18), None, (2386860, 54), None, None, None, None, None, None, (2386914, 26), None, None, None, (2386940, 20), None, None, (2386960, 64), (2387024, 42), (2387066, 17), (2387083, 17), (2387100, 26), None, (2387126, 26), None, None, None, (2387152, 26), (2387178, 20), (2387198, 26), None, (2387224, 42), (2387266, 63), None, None, None, (2387329, 40), (2387369, 48), None, None, None, (2387417, 47), None, None, None, None, None, None, None, (2387464, 42), None, (2387506, 80), None, (2387586, 9), None, (2387595, 21), (2387616, 42), None, None, (2387658, 65), (2387723, 82), None, None, (2387805, 42), None, None, (2387847, 24), (2387871, 21), None, None, None, None, None, (2387892, 42), (2387934, 21), (2387955, 21), None, (2387976, 42), (2388018, 25), None, (2388043, 38), (2388081, 21), (2388102, 56), None, None, (2388158, 21), (2388179, 19), (2388198, 26), None, (2388224, 16), None, (2388240, 21), None, None, (2388261, 38), None, (2388299, 22), (2388321, 21), (2388342, 21), (2388363, 21), None, (2388384, 63), None, (2388447, 21), (2388468, 42), None, (2388510, 17), None, None, None, None, (2388527, 21), (2388548, 21), None, None, (2388569, 21), None, None, (2388590, 21), None, (2388611, 26), None, (2388637, 50), None, None, None, (2388687, 50), (2388737, 26), (2388763, 21), (2388784, 21), (2388805, 19), None, (2388824, 35), (2388859, 26), (2388885, 23), (2388908, 39), (2388947, 42), None, None, None, None, None, None, (2388989, 21), None, None, None, (2389010, 21), None, None, (2389031, 90), None, (2389121, 239), (2389360, 38), None, None, None, None]]  # noqa: E501
_CRC8_TABLE = [
    0x00, 0x07, 0x0e, 0x09, 0x1c, 0x1b, 0x12, 0x15,
    0x38, 0x3f, 0x36, 0x31, 0x24, 0x23, 0x2a, 0x2d,
    0x70, 0x77, 0x7e, 0x79, 0x6c, 0x6b, 0x62, 0x65,
    0x48, 0x4f, 0x46, 0x41, 0x54, 0x53, 0x5a, 0x5d,
    0xe0, 0xe7, 0xee, 0xe9, 0xfc, 0xfb, 0xf2, 0xf5,
    0xd8, 0xdf, 0xd6, 0xd1, 0xc4, 0xc3, 0xca, 0xcd,
    0x90, 0x97, 0x9e, 0x99, 0x8c, 0x8b, 0x82, 0x85,
    0xa8, 0xaf, 0xa6, 0xa1, 0xb4, 0xb3, 0xba, 0xbd,
    0xc7, 0xc0, 0xc9, 0xce, 0xdb, 0xdc, 0xd5, 0xd2,
    0xff, 0xf8, 0xf1, 0xf6, 0xe3, 0xe4, 0xed, 0xea,
    0xb7, 0xb0, 0xb9, 0xbe, 0xab, 0xac, 0xa5, 0xa2,
    0x8f, 0x88, 0x81, 0x86, 0x93, 0x94, 0x9d, 0x9a,
    0x27, 0x20, 0x29, 0x2e, 0x3b, 0x3c, 0x35, 0x32,
    0x1f, 0x18, 0x11, 0x16, 0x03, 0x04, 0x0d, 0x0a,
    0x57, 0x50, 0x59, 0x5e, 0x4b, 0x4c, 0x45, 0x42,
    0x6f, 0x68, 0x61, 0x66, 0x73, 0x74, 0x7d, 0x7a,
    0x89, 0x8e, 0x87, 0x80, 0x95, 0x92, 0x9b, 0x9c,
    0xb1, 0xb6, 0xbf, 0xb8, 0xad, 0xaa, 0xa3, 0xa4,
    0xf9, 0xfe, 0xf7, 0xf0, 0xe5, 0xe2, 0xeb, 0xec,
    0xc1, 0xc6, 0xcf, 0xc8, 0xdd, 0xda, 0xd3, 0xd4,
    0x69, 0x6e, 0x67, 0x60, 0x75, 0x72, 0x7b, 0x7c,
    0x51, 0x56, 0x5f, 0x58, 0x4d, 0x4a, 0x43, 0x44,
    0x19, 0x1e, 0x17, 0x10, 0x05, 0x02, 0x0b, 0x0c,
    0x21, 0x26, 0x2f, 0x28, 0x3d, 0x3a, 0x33, 0x34,
    0x4e, 0x49, 0x40, 0x47, 0x52, 0x55, 0x5c, 0x5b,
    0x76, 0x71, 0x78, 0x7f, 0x6a, 0x6d, 0x64, 0x63,
    0x3e, 0x39, 0x30, 0x37, 0x22, 0x25, 0x2c, 0x2b,
    0x06, 0x01, 0x08, 0x0f, 0x1a, 0x1d, 0x14, 0x13,
    0xae, 0xa9, 0xa0, 0xa7, 0xb2, 0xb5, 0xbc, 0xbb,
    0x96, 0x91, 0x98, 0x9f, 0x8a, 0x8d, 0x84, 0x83,
    0xde, 0xd9, 0xd0, 0xd7, 0xc2, 0xc5, 0xcc, 0xcb,
    0xe6, 0xe1, 0xe8, 0xef, 0xfa, 0xfd, 0xf4, 0xf3
]
# fmt: on

_IS_LEAF = 0x80
_INCLUDE_SUBDOMAINS = 0x40


try:
    from importlib.resources import open_binary

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open_binary("hstspreload", path)


except ImportError:

    def open_pkg_binary(path: str) -> typing.BinaryIO:
        return open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
            "rb",
        )


@functools.lru_cache(maxsize=1024)
def in_hsts_preload(host: typing.AnyStr) -> bool:
    """Determines if an IDNA-encoded host is on the HSTS preload list"""

    if isinstance(host, str):
        host = host.encode("ascii")
    labels = host.lower().split(b".")

    # Fast-branch for gTLDs that are registered to preload all sub-domains.
    if labels[-1] in _GTLD_INCLUDE_SUBDOMAINS:
        return True

    with open_pkg_binary("hstspreload.bin") as f:
        for layer, label in enumerate(labels[::-1]):
            # None of our layers are greater than 4 deep.
            if layer > 3:
                return False

            # Read the jump table for the layer and label
            jump_info = _JUMPTABLE[layer][_crc8(label)]
            if jump_info is None:
                # No entry: host is not preloaded
                return False

            # Read the set of entries for that layer and label
            f.seek(jump_info[0])
            data = bytearray(jump_info[1])
            f.readinto(data)

            for is_leaf, include_subdomains, ent_label in _iter_entries(data):
                # We found a potential leaf
                if is_leaf:
                    if ent_label == host:
                        return True
                    if include_subdomains and host.endswith(b"." + ent_label):
                        return True

                # Continue traversing as we're not at a leaf.
                elif label == ent_label:
                    break
            else:
                return False
    return False


def _iter_entries(data: bytes) -> typing.Iterable[typing.Tuple[int, int, bytes]]:
    while data:
        flags = data[0]
        size = data[1]
        label = bytes(data[2 : 2 + size])
        yield (flags & _IS_LEAF, flags & _INCLUDE_SUBDOMAINS, label)
        data = data[2 + size :]


def _crc8(value: bytes) -> int:
    # CRC8 reference implementation: https://github.com/niccokunzmann/crc8
    checksum = 0x00
    for byte in value:
        checksum = _CRC8_TABLE[checksum ^ byte]
    return checksum
