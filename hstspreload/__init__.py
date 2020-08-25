"""Check if a host is in the Google Chrome HSTS Preload list"""

import functools
import os
import typing

__version__ = "2020.8.25"
__checksum__ = "f139ceecb429706aaafd39f1b17309b93a17a144b3e543b19309a658d88cac6d"
__all__ = ["in_hsts_preload"]

# fmt: off
_GTLD_INCLUDE_SUBDOMAINS = {b'android', b'app', b'bank', b'chrome', b'dev', b'foo', b'gle', b'gmail', b'google', b'hangout', b'insurance', b'meet', b'new', b'page', b'play', b'search', b'youtube'}  # noqa: E501
_JUMPTABLE = [[(0, 11), (11, 5), None, (16, 57), (73, 26), (99, 12), None, (111, 19), (130, 22), (152, 7), (159, 20), (179, 18), None, (197, 22), (219, 45), (264, 7), (271, 9), (280, 36), (316, 10), (326, 10), (336, 21), None, (357, 50), (407, 8), (415, 9), (424, 19), (443, 13), (456, 14), (470, 14), None, None, (484, 29), (513, 16), (529, 35), (564, 14), (578, 24), (602, 9), None, (611, 25), (636, 20), (656, 8), (664, 13), (677, 10), None, (687, 17), (704, 6), (710, 26), (736, 5), (741, 5), (746, 10), (756, 10), (766, 11), (777, 12), (789, 27), None, (816, 11), (827, 11), (838, 7), (845, 29), (874, 18), (892, 27), (919, 46), (965, 25), (990, 16), (1006, 8), (1014, 5), (1019, 22), (1041, 18), None, (1059, 36), (1095, 15), (1110, 8), (1118, 5), None, (1123, 5), (1128, 16), (1144, 14), (1158, 18), None, (1176, 14), (1190, 18), (1208, 48), (1256, 19), (1275, 5), (1280, 46), (1326, 14), (1340, 14), (1354, 20), None, (1374, 10), (1384, 13), (1397, 10), (1407, 19), None, (1426, 13), (1439, 19), (1458, 5), (1463, 4), (1467, 22), (1489, 10), (1499, 7), (1506, 14), (1520, 21), (1541, 11), (1552, 10), (1562, 12), (1574, 32), None, (1606, 10), (1616, 14), (1630, 12), (1642, 45), (1687, 15), None, (1702, 11), (1713, 23), (1736, 21), (1757, 26), (1783, 6), (1789, 6), (1795, 7), (1802, 5), (1807, 20), (1827, 23), (1850, 24), (1874, 13), (1887, 15), (1902, 19), (1921, 6), (1927, 61), (1988, 44), (2032, 12), (2044, 23), (2067, 16), (2083, 38), (2121, 6), (2127, 12), (2139, 44), (2183, 6), (2189, 41), (2230, 13), (2243, 23), (2266, 30), (2296, 16), (2312, 8), (2320, 15), (2335, 12), (2347, 19), (2366, 21), (2387, 15), None, (2402, 35), (2437, 21), (2458, 17), (2475, 19), (2494, 26), (2520, 5), (2525, 37), (2562, 30), (2592, 16), (2608, 10), (2618, 17), (2635, 23), (2658, 14), (2672, 17), (2689, 8), (2697, 4), (2701, 7), (2708, 29), (2737, 6), (2743, 18), (2761, 27), (2788, 20), (2808, 17), (2825, 19), (2844, 12), (2856, 40), (2896, 40), (2936, 12), (2948, 48), (2996, 25), (3021, 12), None, (3033, 8), (3041, 20), (3061, 19), (3080, 6), (3086, 23), None, (3109, 30), (3139, 33), (3172, 14), (3186, 12), (3198, 27), None, (3225, 26), (3251, 31), (3282, 50), (3332, 15), (3347, 20), (3367, 15), (3382, 21), (3403, 32), (3435, 24), (3459, 20), (3479, 13), (3492, 60), (3552, 19), (3571, 9), (3580, 12), (3592, 12), (3604, 11), (3615, 10), (3625, 48), (3673, 32), None, (3705, 25), (3730, 12), None, (3742, 8), (3750, 8), (3758, 7), None, (3765, 25), (3790, 17), None, (3807, 21), (3828, 35), (3863, 12), (3875, 10), (3885, 36), (3921, 20), (3941, 22), (3963, 23), (3986, 19), (4005, 12), (4017, 5), (4022, 30), (4052, 24), (4076, 14), (4090, 14), (4104, 47), (4151, 46), None, None, (4197, 51), (4248, 42), None, (4290, 14), None, (4304, 15), (4319, 8), (4327, 21), (4348, 6), (4354, 16), (4370, 17)], [(4387, 6232), (10619, 6743), (17362, 7147), (24509, 5973), (30482, 6383), (36865, 6121), (42986, 6923), (49909, 6259), (56168, 6849), (63017, 6120), (69137, 7113), (76250, 6546), (82796, 6743), (89539, 7189), (96728, 6537), (103265, 6506), (109771, 7062), (116833, 6011), (122844, 6290), (129134, 6592), (135726, 6979), (142705, 6608), (149313, 6893), (156206, 6181), (162387, 6391), (168778, 6619), (175397, 6640), (182037, 6950), (188987, 6363), (195350, 6722), (202072, 6894), (208966, 6540), (215506, 6491), (221997, 7082), (229079, 6204), (235283, 6869), (242152, 6235), (248387, 7023), (255410, 6829), (262239, 6990), (269229, 7553), (276782, 6481), (283263, 6311), (289574, 6212), (295786, 6376), (302162, 6143), (308305, 6434), (314739, 7069), (321808, 6478), (328286, 5863), (334149, 6471), (340620, 6661), (347281, 6596), (353877, 6800), (360677, 6872), (367549, 6857), (374406, 6902), (381308, 5947), (387255, 6970), (394225, 5865), (400090, 6703), (406793, 6428), (413221, 6414), (419635, 6899), (426534, 6672), (433206, 6616), (439822, 6247), (446069, 7111), (453180, 6769), (459949, 6820), (466769, 6607), (473376, 6608), (479984, 5737), (485721, 7042), (492763, 7150), (499913, 7100), (507013, 6166), (513179, 7254), (520433, 7111), (527544, 6091), (533635, 6766), (540401, 5764), (546165, 6444), (552609, 6655), (559264, 6527), (565791, 6466), (572257, 6632), (578889, 6673), (585562, 6837), (592399, 6590), (598989, 7271), (606260, 6010), (612270, 6368), (618638, 6632), (625270, 6538), (631808, 7151), (638959, 6953), (645912, 6539), (652451, 6262), (658713, 6183), (664896, 6273), (671169, 6779), (677948, 6207), (684155, 6504), (690659, 6184), (696843, 6913), (703756, 6711), (710467, 7052), (717519, 8047), (725566, 7148), (732714, 6995), (739709, 6497), (746206, 6325), (752531, 6707), (759238, 6913), (766151, 6711), (772862, 6304), (779166, 6395), (785561, 6405), (791966, 7110), (799076, 6845), (805921, 6912), (812833, 7036), (819869, 6955), (826824, 7847), (834671, 6442), (841113, 5823), (846936, 6944), (853880, 6623), (860503, 8053), (868556, 7096), (875652, 6170), (881822, 6849), (888671, 6836), (895507, 6345), (901852, 6768), (908620, 6220), (914840, 6848), (921688, 6500), (928188, 6565), (934753, 6624), (941377, 7272), (948649, 6297), (954946, 6295), (961241, 6600), (967841, 6595), (974436, 6563), (980999, 6926), (987925, 6209), (994134, 7209), (1001343, 6684), (1008027, 6751), (1014778, 6901), (1021679, 6483), (1028162, 6594), (1034756, 6623), (1041379, 6395), (1047774, 6489), (1054263, 6322), (1060585, 5991), (1066576, 6225), (1072801, 6697), (1079498, 7292), (1086790, 6175), (1092965, 6662), (1099627, 6948), (1106575, 6403), (1112978, 6178), (1119156, 6967), (1126123, 6565), (1132688, 5984), (1138672, 6528), (1145200, 7726), (1152926, 6113), (1159039, 6274), (1165313, 6777), (1172090, 6286), (1178376, 6725), (1185101, 6410), (1191511, 6025), (1197536, 7498), (1205034, 6839), (1211873, 6500), (1218373, 7056), (1225429, 7442), (1232871, 7344), (1240215, 6195), (1246410, 7020), (1253430, 6329), (1259759, 6625), (1266384, 6799), (1273183, 6193), (1279376, 6943), (1286319, 7036), (1293355, 6597), (1299952, 6735), (1306687, 6472), (1313159, 6553), (1319712, 6808), (1326520, 6372), (1332892, 6733), (1339625, 6023), (1345648, 7175), (1352823, 6906), (1359729, 6700), (1366429, 7002), (1373431, 5801), (1379232, 6757), (1385989, 6514), (1392503, 6865), (1399368, 6848), (1406216, 7207), (1413423, 6708), (1420131, 6885), (1427016, 6946), (1433962, 6382), (1440344, 6497), (1446841, 6544), (1453385, 6588), (1459973, 6452), (1466425, 6542), (1472967, 6047), (1479014, 7597), (1486611, 6715), (1493326, 6360), (1499686, 6664), (1506350, 6803), (1513153, 5931), (1519084, 6749), (1525833, 6634), (1532467, 7573), (1540040, 6560), (1546600, 6059), (1552659, 7072), (1559731, 6411), (1566142, 7220), (1573362, 6223), (1579585, 6270), (1585855, 5836), (1591691, 6678), (1598369, 6489), (1604858, 6899), (1611757, 6354), (1618111, 6622), (1624733, 6553), (1631286, 7113), (1638399, 6423), (1644822, 5900), (1650722, 6620), (1657342, 6233), (1663575, 6844), (1670419, 6934), (1677353, 7127), (1684480, 6308), (1690788, 6331), (1697119, 6743)], [(1703862, 722), (1704584, 625), (1705209, 665), (1705874, 703), (1706577, 537), (1707114, 649), (1707763, 644), (1708407, 836), (1709243, 640), (1709883, 645), (1710528, 536), (1711064, 574), (1711638, 758), (1712396, 866), (1713262, 987), (1714249, 731), (1714980, 1224), (1716204, 606), (1716810, 875), (1717685, 673), (1718358, 745), (1719103, 746), (1719849, 853), (1720702, 731), (1721433, 703), (1722136, 646), (1722782, 955), (1723737, 1131), (1724868, 807), (1725675, 734), (1726409, 922), (1727331, 787), (1728118, 568), (1728686, 691), (1729377, 748), (1730125, 789), (1730914, 619), (1731533, 688), (1732221, 692), (1732913, 1042), (1733955, 695), (1734650, 812), (1735462, 705), (1736167, 719), (1736886, 728), (1737614, 378), (1737992, 908), (1738900, 857), (1739757, 721), (1740478, 568), (1741046, 821), (1741867, 671), (1742538, 780), (1743318, 1012), (1744330, 917), (1745247, 558), (1745805, 661), (1746466, 527), (1746993, 578), (1747571, 751), (1748322, 772), (1749094, 776), (1749870, 1041), (1750911, 915), (1751826, 706), (1752532, 719), (1753251, 767), (1754018, 456), (1754474, 561), (1755035, 556), (1755591, 692), (1756283, 877), (1757160, 536), (1757696, 725), (1758421, 650), (1759071, 684), (1759755, 552), (1760307, 672), (1760979, 785), (1761764, 428), (1762192, 754), (1762946, 629), (1763575, 828), (1764403, 623), (1765026, 607), (1765633, 425), (1766058, 597), (1766655, 725), (1767380, 781), (1768161, 730), (1768891, 853), (1769744, 1074), (1770818, 826), (1771644, 833), (1772477, 725), (1773202, 436), (1773638, 984), (1774622, 878), (1775500, 580), (1776080, 647), (1776727, 710), (1777437, 854), (1778291, 855), (1779146, 571), (1779717, 632), (1780349, 740), (1781089, 395), (1781484, 479), (1781963, 924), (1782887, 897), (1783784, 831), (1784615, 774), (1785389, 632), (1786021, 771), (1786792, 659), (1787451, 699), (1788150, 709), (1788859, 433), (1789292, 667), (1789959, 669), (1790628, 914), (1791542, 653), (1792195, 804), (1792999, 461), (1793460, 703), (1794163, 755), (1794918, 835), (1795753, 908), (1796661, 781), (1797442, 904), (1798346, 791), (1799137, 524), (1799661, 795), (1800456, 597), (1801053, 758), (1801811, 747), (1802558, 676), (1803234, 700), (1803934, 635), (1804569, 673), (1805242, 594), (1805836, 674), (1806510, 715), (1807225, 632), (1807857, 473), (1808330, 587), (1808917, 661), (1809578, 577), (1810155, 717), (1810872, 594), (1811466, 773), (1812239, 532), (1812771, 510), (1813281, 656), (1813937, 612), (1814549, 642), (1815191, 639), (1815830, 836), (1816666, 610), (1817276, 622), (1817898, 874), (1818772, 867), (1819639, 543), (1820182, 695), (1820877, 854), (1821731, 632), (1822363, 675), (1823038, 455), (1823493, 609), (1824102, 660), (1824762, 754), (1825516, 598), (1826114, 932), (1827046, 708), (1827754, 807), (1828561, 721), (1829282, 668), (1829950, 586), (1830536, 664), (1831200, 720), (1831920, 1353), (1833273, 533), (1833806, 643), (1834449, 608), (1835057, 1001), (1836058, 771), (1836829, 764), (1837593, 546), (1838139, 587), (1838726, 823), (1839549, 601), (1840150, 569), (1840719, 847), (1841566, 650), (1842216, 895), (1843111, 810), (1843921, 692), (1844613, 710), (1845323, 868), (1846191, 637), (1846828, 909), (1847737, 631), (1848368, 762), (1849130, 570), (1849700, 742), (1850442, 483), (1850925, 818), (1851743, 823), (1852566, 665), (1853231, 916), (1854147, 775), (1854922, 849), (1855771, 920), (1856691, 1077), (1857768, 863), (1858631, 648), (1859279, 877), (1860156, 702), (1860858, 508), (1861366, 443), (1861809, 740), (1862549, 762), (1863311, 394), (1863705, 1001), (1864706, 488), (1865194, 758), (1865952, 863), (1866815, 792), (1867607, 784), (1868391, 658), (1869049, 788), (1869837, 728), (1870565, 784), (1871349, 628), (1871977, 579), (1872556, 408), (1872964, 666), (1873630, 456), (1874086, 782), (1874868, 855), (1875723, 764), (1876487, 718), (1877205, 645), (1877850, 589), (1878439, 848), (1879287, 529), (1879816, 606), (1880422, 780), (1881202, 494), (1881696, 870), (1882566, 2119), (1884685, 548), (1885233, 707), (1885940, 890), (1886830, 900), (1887730, 510)], [(1888240, 48), None, (1888288, 35), (1888323, 42), None, None, None, None, None, None, None, None, None, None, None, None, None, (1888365, 42), None, (1888407, 25), (1888432, 16), None, (1888448, 18), None, None, None, None, (1888466, 26), None, None, None, None, (1888492, 21), (1888513, 25), None, None, (1888538, 26), None, None, None, None, (1888564, 44), (1888608, 21), (1888629, 23), None, None, None, None, (1888652, 48), None, None, None, None, None, (1888700, 31), None, None, None, None, (1888731, 42), None, (1888773, 22), None, (1888795, 21), None, (1888816, 26), (1888842, 42), None, None, (1888884, 77), None, None, None, None, None, (1888961, 21), (1888982, 21), None, None, (1889003, 34), (1889037, 42), None, None, None, (1889079, 25), None, None, (1889104, 21), None, None, None, None, None, (1889125, 24), (1889149, 21), None, None, (1889170, 26), None, (1889196, 18), None, (1889214, 54), None, None, None, None, None, None, (1889268, 26), None, (1889294, 19), None, (1889313, 20), None, None, (1889333, 42), (1889375, 42), (1889417, 17), None, (1889434, 26), None, (1889460, 26), None, None, None, (1889486, 26), (1889512, 20), (1889532, 26), None, (1889558, 42), (1889600, 63), None, None, None, (1889663, 40), (1889703, 48), None, None, None, (1889751, 47), None, None, None, None, None, None, None, (1889798, 42), None, (1889840, 55), None, (1889895, 9), None, (1889904, 21), (1889925, 42), None, None, (1889967, 42), (1890009, 82), None, None, (1890091, 42), None, None, None, None, None, None, None, None, None, (1890133, 42), (1890175, 21), (1890196, 21), None, (1890217, 42), (1890259, 25), None, None, (1890284, 21), (1890305, 42), None, None, (1890347, 21), (1890368, 19), (1890387, 26), None, None, None, (1890413, 21), None, None, (1890434, 38), None, (1890472, 22), (1890494, 21), (1890515, 21), None, None, (1890536, 63), None, (1890599, 21), (1890620, 42), None, (1890662, 17), None, None, None, None, (1890679, 21), (1890700, 21), None, None, (1890721, 21), None, None, (1890742, 21), None, (1890763, 26), None, (1890789, 50), None, None, None, (1890839, 50), (1890889, 26), (1890915, 21), (1890936, 21), (1890957, 19), None, (1890976, 35), (1891011, 26), (1891037, 23), (1891060, 21), (1891081, 42), None, None, None, None, None, None, (1891123, 21), None, None, None, (1891144, 21), None, None, (1891165, 90), None, (1891255, 239), (1891494, 38), None, None, None, None]]  # noqa: E501
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
            os.path.join(os.path.dirname(os.path.abspath(__file__)), path), "rb",
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
