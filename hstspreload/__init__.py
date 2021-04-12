"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2021.4.12"
__checksum__ = "1fbde4dc9e159125aa92e8bbeaaf9ce1224fa68213b627ac1240c1fe91746714"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), (16, 9), (25, 61), (86, 26), (112, 12), None, (124, 19), (143, 22), (165, 7), (172, 20), (192, 18), None, (210, 29), (239, 45), (284, 7), (291, 9), (300, 36), (336, 10), (346, 10), (356, 28), None, (384, 54), (438, 8), (446, 18), (464, 19), (483, 13), (496, 14), (510, 14), None, None, (524, 29), (553, 20), (573, 35), (608, 14), (622, 24), (646, 9), None, (655, 25), (680, 27), (707, 8), (715, 13), None, None, (728, 17), (745, 6), (751, 26), (777, 5), (782, 5), (787, 10), (797, 14), (811, 11), (822, 12), (834, 27), None, (861, 11), (872, 11), (883, 7), (890, 29), (919, 18), (937, 27), (964, 46), (1010, 25), (1035, 16), (1051, 8), (1059, 5), (1064, 22), (1086, 18), None, (1104, 36), (1140, 15), (1155, 8), (1163, 11), None, (1174, 5), (1179, 16), (1195, 14), (1209, 18), None, (1227, 14), (1241, 26), (1267, 48), (1315, 19), (1334, 5), (1339, 46), (1385, 14), (1399, 14), (1413, 20), None, (1433, 10), (1443, 13), (1456, 15), (1471, 19), None, (1490, 13), (1503, 19), (1522, 11), (1533, 4), (1537, 22), (1559, 10), (1569, 7), (1576, 14), (1590, 21), (1611, 11), (1622, 21), (1643, 12), (1655, 32), None, (1687, 10), (1697, 14), (1711, 12), (1723, 45), (1768, 15), None, (1783, 11), (1794, 23), (1817, 21), (1838, 26), (1864, 6), (1870, 6), (1876, 7), (1883, 5), (1888, 20), (1908, 23), (1931, 24), (1955, 13), (1968, 15), (1983, 19), (2002, 6), (2008, 61), (2069, 44), (2113, 12), (2125, 23), (2148, 16), (2164, 38), (2202, 6), (2208, 12), (2220, 44), (2264, 6), (2270, 41), (2311, 13), (2324, 23), (2347, 30), (2377, 16), (2393, 8), (2401, 15), (2416, 12), (2428, 19), (2447, 21), (2468, 15), None, (2483, 35), (2518, 21), (2539, 17), (2556, 19), (2575, 26), (2601, 5), (2606, 37), (2643, 26), (2669, 16), (2685, 10), (2695, 17), (2712, 23), (2735, 14), (2749, 17), (2766, 8), (2774, 4), (2778, 7), (2785, 29), (2814, 6), (2820, 18), (2838, 27), (2865, 20), (2885, 17), (2902, 19), (2921, 12), (2933, 40), (2973, 40), (3013, 12), (3025, 48), (3073, 25), (3098, 12), None, (3110, 8), (3118, 25), (3143, 19), (3162, 6), (3168, 23), None, (3191, 30), (3221, 33), (3254, 14), (3268, 12), (3280, 27), None, (3307, 26), (3333, 41), (3374, 50), (3424, 15), (3439, 20), (3459, 15), (3474, 21), (3495, 32), (3527, 24), (3551, 20), (3571, 17), (3588, 60), (3648, 19), (3667, 9), (3676, 12), (3688, 12), (3700, 11), (3711, 10), (3721, 48), (3769, 32), None, (3801, 25), (3826, 23), None, (3849, 8), (3857, 8), (3865, 7), None, (3872, 25), (3897, 17), None, (3914, 21), (3935, 35), (3970, 21), (3991, 10), (4001, 36), (4037, 20), (4057, 22), (4079, 23), (4102, 19), (4121, 12), (4133, 5), (4138, 30), (4168, 24), (4192, 14), (4206, 14), (4220, 47), (4267, 46), None, None, (4313, 51), (4364, 42), None, (4406, 14), None, (4420, 15), (4435, 8), (4443, 21), (4464, 6), (4470, 16), (4486, 17)], [(4503, 7571), (12074, 8080), (20154, 8376), (28530, 7251), (35781, 7673), (43454, 7189), (50643, 8304), (58947, 7097), (66044, 8186), (74230, 7478), (81708, 8788), (90496, 7393), (97889, 7969), (105858, 9104), (114962, 7725), (122687, 7811), (130498, 8318), (138816, 7237), (146053, 7642), (153695, 7417), (161112, 8165), (169277, 7867), (177144, 8270), (185414, 7394), (192808, 7799), (200607, 7720), (208327, 8241), (216568, 8236), (224804, 7495), (232299, 7752), (240051, 8097), (248148, 7709), (255857, 7789), (263646, 8070), (271716, 7331), (279047, 7827), (286874, 7780), (294654, 8408), (303062, 8014), (311076, 8156), (319232, 8777), (328009, 7477), (335486, 7593), (343079, 7387), (350466, 7585), (358051, 7584), (365635, 7843), (373478, 8566), (382044, 7690), (389734, 7155), (396889, 7618), (404507, 8157), (412664, 8162), (420826, 8207), (429033, 8344), (437377, 7902), (445279, 8263), (453542, 7749), (461291, 8327), (469618, 6828), (476446, 7877), (484323, 7891), (492214, 7767), (499981, 8276), (508257, 8124), (516381, 8317), (524698, 7508), (532206, 8431), (540637, 8264), (548901, 8027), (556928, 7598), (564526, 7596), (572122, 7141), (579263, 8281), (587544, 8098), (595642, 8464), (604106, 7385), (611491, 8418), (619909, 8266), (628175, 7484), (635659, 8220), (643879, 6929), (650808, 7830), (658638, 7979), (666617, 7528), (674145, 7741), (681886, 8251), (690137, 7986), (698123, 8118), (706241, 8058), (714299, 8845), (723144, 7161), (730305, 7737), (738042, 7861), (745903, 8078), (753981, 8484), (762465, 8396), (770861, 7537), (778398, 7669), (786067, 7556), (793623, 7611), (801234, 7896), (809130, 7732), (816862, 7694), (824556, 7520), (832076, 8311), (840387, 8246), (848633, 8235), (856868, 9086), (865954, 8364), (874318, 8047), (882365, 8170), (890535, 7638), (898173, 7726), (905899, 8021), (913920, 8138), (922058, 7728), (929786, 7525), (937311, 7730), (945041, 8563), (953604, 8237), (961841, 8288), (970129, 7967), (978096, 8333), (986429, 9148), (995577, 7758), (1003335, 7159), (1010494, 8360), (1018854, 7897), (1026751, 9579), (1036330, 8452), (1044782, 7513), (1052295, 8115), (1060410, 7958), (1068368, 7544), (1075912, 8265), (1084177, 7604), (1091781, 8162), (1099943, 7654), (1107597, 7927), (1115524, 8031), (1123555, 8361), (1131916, 7371), (1139287, 7653), (1146940, 7923), (1154863, 7642), (1162505, 7679), (1170184, 7805), (1177989, 7485), (1185474, 8428), (1193902, 8056), (1201958, 8133), (1210091, 8290), (1218381, 7623), (1226004, 8018), (1234022, 7907), (1241929, 7760), (1249689, 7960), (1257649, 7580), (1265229, 7135), (1272364, 7323), (1279687, 8142), (1287829, 8475), (1296304, 7431), (1303735, 7626), (1311361, 8607), (1319968, 7767), (1327735, 7322), (1335057, 8362), (1343419, 8007), (1351426, 6941), (1358367, 7848), (1366215, 9251), (1375466, 7326), (1382792, 7465), (1390257, 8151), (1398408, 7745), (1406153, 8098), (1414251, 7700), (1421951, 7353), (1429304, 8776), (1438080, 8274), (1446354, 7694), (1454048, 8371), (1462419, 8813), (1471232, 8624), (1479856, 7339), (1487195, 8318), (1495513, 7689), (1503202, 7933), (1511135, 8375), (1519510, 7668), (1527178, 8243), (1535421, 8228), (1543649, 7757), (1551406, 7764), (1559170, 7588), (1566758, 7913), (1574671, 7762), (1582433, 7525), (1589958, 8217), (1598175, 7452), (1605627, 8410), (1614037, 8022), (1622059, 8459), (1630518, 8269), (1638787, 7066), (1645853, 8143), (1653996, 7640), (1661636, 8062), (1669698, 8140), (1677838, 8217), (1686055, 7914), (1693969, 8277), (1702246, 8167), (1710413, 7729), (1718142, 7941), (1726083, 7670), (1733753, 8022), (1741775, 8223), (1749998, 7981), (1757979, 7377), (1765356, 8801), (1774157, 7855), (1782012, 7649), (1789661, 7838), (1797499, 7853), (1805352, 7209), (1812561, 8207), (1820768, 7952), (1828720, 8600), (1837320, 8034), (1845354, 7541), (1852895, 8274), (1861169, 7857), (1869026, 8705), (1877731, 7591), (1885322, 7576), (1892898, 6888), (1899786, 8293), (1908079, 8037), (1916116, 8352), (1924468, 7736), (1932204, 8025), (1940229, 7687), (1947916, 8404), (1956320, 7690), (1964010, 7218), (1971228, 7745), (1978973, 7467), (1986440, 8088), (1994528, 8472), (2003000, 8313), (2011313, 7589), (2018902, 7670), (2026572, 7959)], [(2034531, 933), (2035464, 715), (2036179, 754), (2036933, 918), (2037851, 638), (2038489, 785), (2039274, 671), (2039945, 970), (2040915, 721), (2041636, 729), (2042365, 580), (2042945, 660), (2043605, 827), (2044432, 885), (2045317, 1022), (2046339, 924), (2047263, 1336), (2048599, 736), (2049335, 960), (2050295, 836), (2051131, 779), (2051910, 811), (2052721, 946), (2053667, 765), (2054432, 799), (2055231, 715), (2055946, 1050), (2056996, 1266), (2058262, 797), (2059059, 853), (2059912, 1037), (2060949, 880), (2061829, 673), (2062502, 773), (2063275, 864), (2064139, 867), (2065006, 822), (2065828, 799), (2066627, 777), (2067404, 1087), (2068491, 713), (2069204, 866), (2070070, 816), (2070886, 784), (2071670, 785), (2072455, 522), (2072977, 1086), (2074063, 1027), (2075090, 847), (2075937, 619), (2076556, 882), (2077438, 706), (2078144, 762), (2078906, 1065), (2079971, 1046), (2081017, 572), (2081589, 729), (2082318, 697), (2083015, 683), (2083698, 888), (2084586, 850), (2085436, 832), (2086268, 1135), (2087403, 1038), (2088441, 793), (2089234, 793), (2090027, 790), (2090817, 495), (2091312, 679), (2091991, 633), (2092624, 803), (2093427, 985), (2094412, 675), (2095087, 859), (2095946, 664), (2096610, 786), (2097396, 705), (2098101, 725), (2098826, 843), (2099669, 553), (2100222, 875), (2101097, 724), (2101821, 929), (2102750, 700), (2103450, 739), (2104189, 482), (2104671, 669), (2105340, 817), (2106157, 929), (2107086, 833), (2107919, 1024), (2108943, 1220), (2110163, 919), (2111082, 941), (2112023, 817), (2112840, 476), (2113316, 996), (2114312, 871), (2115183, 675), (2115858, 721), (2116579, 800), (2117379, 934), (2118313, 966), (2119279, 619), (2119898, 652), (2120550, 913), (2121463, 533), (2121996, 541), (2122537, 1018), (2123555, 1032), (2124587, 802), (2125389, 836), (2126225, 803), (2127028, 780), (2127808, 767), (2128575, 753), (2129328, 696), (2130024, 597), (2130621, 787), (2131408, 707), (2132115, 1115), (2133230, 772), (2134002, 871), (2134873, 502), (2135375, 741), (2136116, 868), (2136984, 880), (2137864, 1026), (2138890, 767), (2139657, 1017), (2140674, 873), (2141547, 635), (2142182, 939), (2143121, 712), (2143833, 903), (2144736, 795), (2145531, 720), (2146251, 690), (2146941, 765), (2147706, 649), (2148355, 723), (2149078, 701), (2149779, 824), (2150603, 651), (2151254, 545), (2151799, 620), (2152419, 731), (2153150, 650), (2153800, 790), (2154590, 702), (2155292, 823), (2156115, 601), (2156716, 659), (2157375, 789), (2158164, 723), (2158887, 713), (2159600, 784), (2160384, 1010), (2161394, 760), (2162154, 636), (2162790, 1044), (2163834, 892), (2164726, 716), (2165442, 765), (2166207, 938), (2167145, 736), (2167881, 745), (2168626, 623), (2169249, 770), (2170019, 769), (2170788, 882), (2171670, 677), (2172347, 950), (2173297, 819), (2174116, 904), (2175020, 833), (2175853, 737), (2176590, 630), (2177220, 792), (2178012, 840), (2178852, 1552), (2180404, 594), (2180998, 837), (2181835, 710), (2182545, 1025), (2183570, 888), (2184458, 870), (2185328, 653), (2185981, 674), (2186655, 925), (2187580, 638), (2188218, 603), (2188821, 873), (2189694, 784), (2190478, 948), (2191426, 825), (2192251, 810), (2193061, 781), (2193842, 915), (2194757, 731), (2195488, 982), (2196470, 737), (2197207, 879), (2198086, 618), (2198704, 823), (2199527, 605), (2200132, 946), (2201078, 914), (2201992, 772), (2202764, 1036), (2203800, 761), (2204561, 906), (2205467, 999), (2206466, 1131), (2207597, 973), (2208570, 788), (2209358, 1020), (2210378, 830), (2211208, 589), (2211797, 495), (2212292, 893), (2213185, 794), (2213979, 572), (2214551, 1102), (2215653, 556), (2216209, 819), (2217028, 953), (2217981, 916), (2218897, 908), (2219805, 746), (2220551, 933), (2221484, 763), (2222247, 913), (2223160, 619), (2223779, 700), (2224479, 519), (2224998, 703), (2225701, 486), (2226187, 878), (2227065, 962), (2228027, 881), (2228908, 751), (2229659, 675), (2230334, 696), (2231030, 995), (2232025, 538), (2232563, 638), (2233201, 935), (2234136, 519), (2234655, 976), (2235631, 2165), (2237796, 714), (2238510, 749), (2239259, 975), (2240234, 1094), (2241328, 515)], [(2241843, 48), None, (2241891, 35), (2241926, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (2241968, 42), None, (2242010, 25), (2242035, 44), (2242079, 22), (2242101, 18), None, None, None, None, (2242119, 26), None, None, None, None, (2242145, 21), (2242166, 25), None, None, (2242191, 26), None, None, None, None, (2242217, 71), (2242288, 21), (2242309, 23), None, None, None, None, (2242332, 48), None, None, None, None, None, (2242380, 31), None, None, None, None, (2242411, 42), None, (2242453, 22), None, (2242475, 21), None, (2242496, 26), (2242522, 42), None, None, (2242564, 77), None, None, None, None, None, (2242641, 21), (2242662, 21), None, None, (2242683, 34), (2242717, 42), None, None, None, (2242759, 25), None, None, (2242784, 21), None, None, None, None, None, (2242805, 24), (2242829, 21), None, None, (2242850, 26), None, (2242876, 18), None, (2242894, 54), None, None, None, None, None, None, (2242948, 26), None, None, None, (2242974, 20), None, None, (2242994, 42), (2243036, 42), (2243078, 17), (2243095, 17), (2243112, 26), None, (2243138, 26), None, None, None, (2243164, 26), (2243190, 20), (2243210, 26), None, (2243236, 42), (2243278, 63), None, None, None, (2243341, 40), (2243381, 48), None, None, None, (2243429, 47), None, None, None, None, None, None, None, (2243476, 42), None, (2243518, 80), None, (2243598, 9), None, (2243607, 21), (2243628, 42), None, None, (2243670, 65), (2243735, 82), None, None, (2243817, 42), None, None, None, (2243859, 21), None, None, None, None, None, (2243880, 42), (2243922, 21), (2243943, 21), None, (2243964, 42), (2244006, 25), None, (2244031, 16), (2244047, 21), (2244068, 56), None, None, (2244124, 21), (2244145, 19), (2244164, 26), None, (2244190, 16), None, (2244206, 21), None, None, (2244227, 38), None, (2244265, 22), (2244287, 21), (2244308, 21), (2244329, 21), None, (2244350, 63), None, (2244413, 21), (2244434, 42), None, (2244476, 17), None, None, None, None, (2244493, 21), (2244514, 21), None, None, (2244535, 21), None, None, (2244556, 21), None, (2244577, 26), None, (2244603, 50), None, None, None, (2244653, 50), (2244703, 26), (2244729, 21), (2244750, 21), (2244771, 19), None, (2244790, 35), (2244825, 26), (2244851, 23), (2244874, 39), (2244913, 42), None, None, None, None, None, None, (2244955, 21), None, None, None, (2244976, 21), None, None, (2244997, 90), None, (2245087, 239), (2245326, 38), None, None, None, None]]  # noqa: E501
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
