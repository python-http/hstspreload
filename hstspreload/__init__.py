"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2021.6.28"
__checksum__ = "3a0790befd4ff71f49f63b93d742015770f8ee30b9c13ef070b58a9a25fb0107"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), (16, 9), (25, 61), (86, 26), (112, 12), None, (124, 19), (143, 22), (165, 7), (172, 20), (192, 18), None, (210, 29), (239, 45), (284, 7), (291, 9), (300, 36), (336, 16), (352, 10), (362, 28), None, (390, 54), (444, 8), (452, 18), (470, 19), (489, 13), (502, 14), (516, 14), None, None, (530, 29), (559, 20), (579, 35), (614, 14), (628, 24), (652, 9), None, (661, 25), (686, 27), (713, 8), (721, 13), None, None, (734, 17), (751, 6), (757, 26), (783, 5), (788, 5), (793, 19), (812, 14), (826, 11), (837, 12), (849, 27), None, (876, 11), (887, 11), (898, 7), (905, 29), (934, 18), (952, 27), (979, 46), (1025, 25), (1050, 16), (1066, 8), (1074, 5), (1079, 22), (1101, 18), None, (1119, 36), (1155, 15), (1170, 8), (1178, 11), None, (1189, 5), (1194, 16), (1210, 14), (1224, 18), None, (1242, 14), (1256, 18), (1274, 48), (1322, 19), (1341, 5), (1346, 59), (1405, 14), (1419, 14), (1433, 20), None, (1453, 10), (1463, 13), (1476, 15), (1491, 19), None, (1510, 13), (1523, 19), (1542, 11), (1553, 4), (1557, 22), (1579, 10), (1589, 7), (1596, 14), (1610, 21), (1631, 11), (1642, 21), (1663, 12), (1675, 32), None, (1707, 10), (1717, 14), (1731, 12), (1743, 45), (1788, 15), None, (1803, 11), (1814, 23), (1837, 21), (1858, 26), (1884, 6), (1890, 6), (1896, 7), (1903, 5), (1908, 20), (1928, 23), (1951, 24), (1975, 13), (1988, 15), (2003, 19), (2022, 6), (2028, 61), (2089, 44), (2133, 12), (2145, 23), (2168, 16), (2184, 38), (2222, 6), (2228, 12), (2240, 44), (2284, 6), (2290, 41), (2331, 13), (2344, 23), (2367, 30), (2397, 16), (2413, 8), (2421, 15), (2436, 12), (2448, 19), (2467, 21), (2488, 15), None, (2503, 35), (2538, 21), (2559, 17), (2576, 19), (2595, 26), (2621, 5), (2626, 37), (2663, 26), (2689, 16), (2705, 10), (2715, 17), (2732, 23), (2755, 14), (2769, 17), (2786, 8), (2794, 8), (2802, 7), (2809, 29), (2838, 6), (2844, 18), (2862, 27), (2889, 20), (2909, 17), (2926, 19), (2945, 12), (2957, 40), (2997, 40), (3037, 12), (3049, 48), (3097, 25), (3122, 12), None, (3134, 8), (3142, 25), (3167, 19), (3186, 6), (3192, 23), None, (3215, 30), (3245, 33), (3278, 14), (3292, 12), (3304, 27), None, (3331, 26), (3357, 41), (3398, 50), (3448, 15), (3463, 20), (3483, 15), (3498, 21), (3519, 32), (3551, 24), (3575, 20), (3595, 17), (3612, 60), (3672, 19), (3691, 9), (3700, 12), (3712, 12), (3724, 11), (3735, 10), (3745, 48), (3793, 32), None, (3825, 25), (3850, 23), None, (3873, 8), (3881, 8), (3889, 7), None, (3896, 25), (3921, 17), None, (3938, 21), (3959, 35), (3994, 21), (4015, 10), (4025, 36), (4061, 20), (4081, 22), (4103, 23), (4126, 19), (4145, 12), (4157, 5), (4162, 30), (4192, 24), (4216, 14), (4230, 14), (4244, 47), (4291, 52), None, None, (4343, 51), (4394, 42), None, (4436, 14), None, (4450, 15), (4465, 8), (4473, 21), (4494, 6), (4500, 16), (4516, 17)], [(4533, 8190), (12723, 8882), (21605, 9190), (30795, 7781), (38576, 8255), (46831, 8029), (54860, 8934), (63794, 7875), (71669, 8820), (80489, 8082), (88571, 9388), (97959, 7949), (105908, 8642), (114550, 9958), (124508, 8431), (132939, 8673), (141612, 9110), (150722, 8044), (158766, 8341), (167107, 8078), (175185, 8805), (183990, 8609), (192599, 8887), (201486, 8332), (209818, 8798), (218616, 8343), (226959, 8834), (235793, 9034), (244827, 8022), (252849, 8514), (261363, 8761), (270124, 8239), (278363, 8528), (286891, 8851), (295742, 7781), (303523, 8709), (312232, 8453), (320685, 9146), (329831, 8730), (338561, 8782), (347343, 9432), (356775, 8029), (364804, 8149), (372953, 8248), (381201, 8404), (389605, 8345), (397950, 8379), (406329, 9486), (415815, 8300), (424115, 7979), (432094, 8332), (440426, 8761), (449187, 8875), (458062, 8706), (466768, 8854), (475622, 8456), (484078, 8890), (492968, 8426), (501394, 8916), (510310, 7528), (517838, 8469), (526307, 8526), (534833, 8465), (543298, 8836), (552134, 8672), (560806, 8872), (569678, 8174), (577852, 9152), (587004, 9002), (596006, 8676), (604682, 8603), (613285, 8066), (621351, 7708), (629059, 8829), (637888, 8577), (646465, 9090), (655555, 7957), (663512, 9111), (672623, 8828), (681451, 8099), (689550, 8911), (698461, 7319), (705780, 8328), (714108, 8804), (722912, 8167), (731079, 8554), (739633, 9186), (748819, 8547), (757366, 8799), (766165, 8714), (774879, 9571), (784450, 7982), (792432, 8411), (800843, 8463), (809306, 8450), (817756, 9090), (826846, 8738), (835584, 8326), (843910, 8259), (852169, 8107), (860276, 8117), (868393, 8681), (877074, 8292), (885366, 8300), (893666, 8166), (901832, 9083), (910915, 9067), (919982, 9003), (928985, 9696), (938681, 8973), (947654, 8830), (956484, 8935), (965419, 8561), (973980, 8398), (982378, 8778), (991156, 8842), (999998, 8508), (1008506, 8152), (1016658, 8312), (1024970, 9260), (1034230, 9055), (1043285, 9009), (1052294, 8582), (1060876, 8821), (1069697, 9675), (1079372, 8253), (1087625, 7747), (1095372, 9155), (1104527, 8578), (1113105, 10119), (1123224, 9052), (1132276, 8103), (1140379, 8807), (1149186, 8548), (1157734, 8318), (1166052, 8621), (1174673, 8154), (1182827, 9055), (1191882, 8209), (1200091, 8371), (1208462, 8844), (1217306, 8789), (1226095, 7856), (1233951, 8271), (1242222, 9025), (1251247, 8332), (1259579, 8447), (1268026, 8497), (1276523, 8213), (1284736, 8943), (1293679, 8723), (1302402, 8695), (1311097, 8971), (1320068, 8204), (1328272, 8618), (1336890, 8683), (1345573, 8279), (1353852, 8637), (1362489, 8138), (1370627, 7673), (1378300, 7767), (1386067, 8795), (1394862, 9219), (1404081, 8295), (1412376, 8269), (1420645, 9297), (1429942, 8477), (1438419, 8061), (1446480, 9003), (1455483, 8599), (1464082, 7627), (1471709, 8449), (1480158, 9939), (1490097, 8035), (1498132, 8059), (1506191, 9012), (1515203, 8517), (1523720, 9025), (1532745, 8290), (1541035, 8083), (1549118, 10631), (1559749, 8865), (1568614, 8573), (1577187, 8791), (1585978, 9457), (1595435, 9565), (1605000, 7898), (1612898, 8730), (1621628, 8150), (1629778, 8565), (1638343, 9311), (1647654, 8137), (1655791, 8891), (1664682, 8754), (1673436, 8387), (1681823, 8564), (1690387, 8358), (1698745, 8387), (1707132, 8673), (1715805, 8348), (1724153, 8648), (1732801, 8067), (1740868, 9001), (1749869, 8526), (1758395, 9249), (1767644, 9034), (1776678, 7634), (1784312, 9014), (1793326, 8374), (1801700, 8802), (1810502, 8807), (1819309, 8992), (1828301, 8574), (1836875, 8859), (1845734, 8716), (1854450, 8490), (1862940, 8544), (1871484, 8240), (1879724, 8671), (1888395, 9012), (1897407, 8717), (1906124, 8007), (1914131, 9605), (1923736, 8489), (1932225, 8510), (1940735, 8470), (1949205, 8515), (1957720, 7896), (1965616, 8875), (1974491, 8678), (1983169, 9265), (1992434, 8658), (2001092, 8089), (2009181, 9065), (2018246, 8521), (2026767, 9474), (2036241, 8230), (2044471, 8234), (2052705, 7582), (2060287, 9021), (2069308, 8860), (2078168, 9139), (2087307, 8292), (2095599, 8696), (2104295, 8329), (2112624, 9050), (2121674, 8329), (2130003, 7911), (2137914, 8425), (2146339, 7974), (2154313, 8800), (2163113, 9108), (2172221, 9026), (2181247, 8243), (2189490, 8475), (2197965, 8557)], [(2206522, 933), (2207455, 760), (2208215, 811), (2209026, 1010), (2210036, 660), (2210696, 861), (2211557, 694), (2212251, 1000), (2213251, 721), (2213972, 789), (2214761, 656), (2215417, 678), (2216095, 827), (2216922, 885), (2217807, 1067), (2218874, 1021), (2219895, 1384), (2221279, 747), (2222026, 1008), (2223034, 873), (2223907, 791), (2224698, 929), (2225627, 1017), (2226644, 811), (2227455, 843), (2228298, 699), (2228997, 1099), (2230096, 1327), (2231423, 818), (2232241, 869), (2233110, 1095), (2234205, 892), (2235097, 697), (2235794, 842), (2236636, 997), (2237633, 985), (2238618, 847), (2239465, 891), (2240356, 832), (2241188, 1225), (2242413, 726), (2243139, 989), (2244128, 807), (2244935, 784), (2245719, 780), (2246499, 561), (2247060, 1086), (2248146, 1045), (2249191, 919), (2250110, 619), (2250729, 937), (2251666, 734), (2252400, 855), (2253255, 1109), (2254364, 1094), (2255458, 593), (2256051, 782), (2256833, 693), (2257526, 728), (2258254, 892), (2259146, 915), (2260061, 859), (2260920, 1159), (2262079, 1078), (2263157, 857), (2264014, 810), (2264824, 809), (2265633, 511), (2266144, 719), (2266863, 640), (2267503, 826), (2268329, 1001), (2269330, 689), (2270019, 880), (2270899, 700), (2271599, 797), (2272396, 735), (2273131, 775), (2273906, 882), (2274788, 586), (2275374, 919), (2276293, 724), (2277017, 991), (2278008, 701), (2278709, 804), (2279513, 568), (2280081, 778), (2280859, 859), (2281718, 943), (2282661, 875), (2283536, 1092), (2284628, 1262), (2285890, 919), (2286809, 943), (2287752, 846), (2288598, 554), (2289152, 1009), (2290161, 906), (2291067, 675), (2291742, 763), (2292505, 848), (2293353, 1042), (2294395, 980), (2295375, 608), (2295983, 706), (2296689, 940), (2297629, 533), (2298162, 589), (2298751, 1060), (2299811, 1032), (2300843, 821), (2301664, 852), (2302516, 803), (2303319, 801), (2304120, 896), (2305016, 873), (2305889, 731), (2306620, 627), (2307247, 801), (2308048, 744), (2308792, 1153), (2309945, 757), (2310702, 904), (2311606, 568), (2312174, 821), (2312995, 914), (2313909, 931), (2314840, 1072), (2315912, 767), (2316679, 1079), (2317758, 925), (2318683, 653), (2319336, 939), (2320275, 787), (2321062, 990), (2322052, 828), (2322880, 777), (2323657, 776), (2324433, 828), (2325261, 706), (2325967, 760), (2326727, 744), (2327471, 824), (2328295, 651), (2328946, 605), (2329551, 637), (2330188, 750), (2330938, 701), (2331639, 824), (2332463, 715), (2333178, 824), (2334002, 631), (2334633, 618), (2335251, 893), (2336144, 789), (2336933, 778), (2337711, 818), (2338529, 1084), (2339613, 880), (2340493, 664), (2341157, 1096), (2342253, 903), (2343156, 720), (2343876, 858), (2344734, 993), (2345727, 719), (2346446, 745), (2347191, 730), (2347921, 756), (2348677, 799), (2349476, 900), (2350376, 677), (2351053, 993), (2352046, 825), (2352871, 939), (2353810, 897), (2354707, 821), (2355528, 630), (2356158, 792), (2356950, 802), (2357752, 2027), (2359779, 626), (2360405, 843), (2361248, 777), (2362025, 1088), (2363113, 913), (2364026, 863), (2364889, 666), (2365555, 704), (2366259, 994), (2367253, 638), (2367891, 651), (2368542, 884), (2369426, 814), (2370240, 985), (2371225, 854), (2372079, 810), (2372889, 763), (2373652, 908), (2374560, 781), (2375341, 961), (2376302, 785), (2377087, 896), (2377983, 688), (2378671, 846), (2379517, 675), (2380192, 981), (2381173, 992), (2382165, 768), (2382933, 1080), (2384013, 780), (2384793, 933), (2385726, 1006), (2386732, 1146), (2387878, 945), (2388823, 846), (2389669, 1006), (2390675, 791), (2391466, 633), (2392099, 490), (2392589, 908), (2393497, 852), (2394349, 618), (2394967, 1117), (2396084, 623), (2396707, 824), (2397531, 969), (2398500, 997), (2399497, 925), (2400422, 746), (2401168, 962), (2402130, 819), (2402949, 971), (2403920, 674), (2404594, 700), (2405294, 619), (2405913, 698), (2406611, 486), (2407097, 900), (2407997, 1067), (2409064, 926), (2409990, 751), (2410741, 724), (2411465, 709), (2412174, 1046), (2413220, 616), (2413836, 625), (2414461, 1007), (2415468, 497), (2415965, 990), (2416955, 2201), (2419156, 727), (2419883, 785), (2420668, 1003), (2421671, 1151), (2422822, 515)], [(2423337, 48), None, (2423385, 35), (2423420, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (2423462, 42), None, (2423504, 25), (2423529, 44), (2423573, 22), (2423595, 18), None, None, None, None, (2423613, 26), None, None, None, None, (2423639, 21), (2423660, 25), None, None, (2423685, 26), None, None, None, None, (2423711, 71), (2423782, 21), (2423803, 23), None, None, None, None, (2423826, 48), None, None, None, None, None, (2423874, 31), None, None, None, None, (2423905, 42), None, (2423947, 22), None, (2423969, 21), None, (2423990, 26), (2424016, 42), None, None, (2424058, 77), (2424135, 27), None, None, None, None, (2424162, 21), (2424183, 21), None, None, (2424204, 34), (2424238, 42), None, None, None, (2424280, 25), None, None, (2424305, 21), None, None, None, None, None, (2424326, 24), (2424350, 21), None, None, (2424371, 26), None, (2424397, 18), None, (2424415, 54), None, None, None, None, None, None, (2424469, 26), None, None, None, (2424495, 20), None, None, (2424515, 64), (2424579, 42), (2424621, 17), (2424638, 17), (2424655, 26), None, (2424681, 26), None, None, None, (2424707, 26), (2424733, 20), (2424753, 26), None, (2424779, 42), (2424821, 63), None, None, None, (2424884, 40), (2424924, 48), None, None, None, (2424972, 47), None, None, None, None, None, None, None, (2425019, 42), None, (2425061, 80), None, (2425141, 9), None, (2425150, 21), (2425171, 42), None, None, (2425213, 65), (2425278, 82), None, None, (2425360, 72), None, None, (2425432, 24), (2425456, 21), None, None, None, None, None, (2425477, 42), (2425519, 21), (2425540, 21), None, (2425561, 42), (2425603, 25), None, (2425628, 38), (2425666, 21), (2425687, 56), None, None, (2425743, 21), (2425764, 19), (2425783, 26), None, (2425809, 16), None, (2425825, 21), None, None, (2425846, 38), None, (2425884, 22), (2425906, 21), (2425927, 21), (2425948, 21), None, (2425969, 63), None, (2426032, 21), (2426053, 42), None, (2426095, 17), None, None, None, None, (2426112, 21), (2426133, 21), None, None, (2426154, 21), None, None, (2426175, 21), None, (2426196, 26), None, (2426222, 50), None, None, None, (2426272, 50), (2426322, 26), (2426348, 21), (2426369, 21), (2426390, 19), None, (2426409, 35), (2426444, 26), (2426470, 23), (2426493, 39), (2426532, 42), None, None, None, None, None, None, (2426574, 21), None, None, None, (2426595, 21), None, None, (2426616, 90), None, (2426706, 239), (2426945, 38), None, None, None, None]]  # noqa: E501
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
