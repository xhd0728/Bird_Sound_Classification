ACCURACY = 1.0

MODEL_PATH = 'val_TimmClassifier_efficientnet_b4_0_f1_score_v2'

NAME_CN_LIST = ['非洲裸眼鸫', '东非黑头黄鹂', '阿比西尼亞鶇', '蓝凤头鹟', '暗鹟', '黄腹金鹃', '吼海雕', '非洲灰鹟',
                '黑嘴弯嘴犀鸟', '哀斑鸠', '非洲寿带', '粉颊小翠鸟', '非洲斑鹡鸰', '非洲鹰', '非洲绿鸠', '非洲雉鸻',
                '非洲鸫', '艾米花蜜鸟', '棕鵟', '黄腹织雀', '家燕', '黑白噪犀鸟', '黑白文鸟', '蓝颊蜂虎', '丽色花蜜鸟',
                '黑头红翅伯劳', '黑脸棕莺', '黑苦恶鸟', '黑杜鹃', '黄嘴鸢', '黑背麦鸡', '鹊形松背伯劳', '黑领娇莺',
                '黑额丛鵙', '黑头黑鵙', '黑头鹭', '蓝锯翅燕', '蓝枕鼠鸟', '黑颈织雀', '黑喉娇莺', '黑喉拟䴕', '山鹂',
                '黑翅麦鸡', '褐胸鸲鸫', '须冠栗翅椋鸟', '褐冠红翅鵙', '褐顶织雀', '硫黄丝雀', '非洲褐鸫鹛', '铜色文鸟',
                '长尾铜花蜜鸟', '基库尤绣眼鸟', '褐尾岩䳭', '非洲伯劳', '褐林柳莺', '蓝斑森鸠', '眼瘤鹟', '黄腹莺',
                '棕喉娇莺', '橄榄绿旋木鹎', '黄喉歌䳭', '暗红啄木鸟', '西方牛背鹭', '桂胸蜂虎', '栗麻雀', '栗织雀',
                '点颏蓬背鹟', '栗喉娇莺', '查氏扇尾莺', '桂红短翅莺', '白腹毛脚燕', '环颈直嘴太阳鸟', '黑眼鹎',
                '欧亚鵟', '矶鹬', '凤头鹧鸪', '非洲冠雕', '冕弯嘴犀鸟', '东非拟啄木', '红蛇鹈', '白眉金鹃', '双齿拟䴕',
                '粉胸斑鸠', '橄榄胸绿鹎', '西黄鹡鸰', '东非双领花蜜鸟', '埃及雁', '杰氏阿卡拉鸲', '绿点森鸠',
                '黄喉蜂虎', '扇尾渡鸦', '扇尾巧织雀', '费沙氏情侣鹦鹉', '叉尾卷尾', '红脸歌鹰', '白眉鸭', '蓝耳丽椋鸟',
                '灰背拱翅莺', '绿头花蜜鸟', '金胸鹀', '金胸丽椋鸟', '苏丹金背织雀', '巨鹭', '绿背拱翅莺', '灰冕鹤',
                '普通鸬鹚', '大白鹭', '绿林戴胜', '绿翅斑腹雀', '灰娇莺', '灰拱翅莺', '灰背长尾伯劳', '灰顶莺',
                '灰头丛鵙', '灰头翡翠', '灰冠黑雀', '灰头麻雀', '灰喉拟䴕', '凤头鹮', '锤头鹳', '蓝冠蕉鹃', '珠鸡',
                '海氏斑鸫鹛', '戴胜', '亨氏扇尾莺', '亨氏花蜜鸟', '娇绿鸫鹎', '肯尼亚麻雀', '白腹金鹃', '东紫背食蜜鸟',
                '棕斑鸠', '加州金翅雀', '黑脸织雀', '小纹燕', '小蜂虎', '白鹭', '小雨燕', '小织雀', '长冠鹰雕',
                '长尾鸬鹚', '长趾麦鸡', '卢氏黑鵙', '马岛蜂虎', '麦氏伯劳', '冠翠鸟', '非洲秃鹳', '马里基花蜜鸟',
                '灰攀雀', '麦耶氏鹦鹉', '桂红蚁䳭', '非洲山鹡鸰', '北非双领花蜜鸟', '黑鹟', '锯齿旋木鹎', '短尾森莺',
                '北领伯劳', '蓬背鵙', '东非啄木', '鹦嘴麻雀', '苍色鹟', '淡山鹪莺', '非洲白颈鸦', '斑鱼狗',
                '针尾维达雀', '紫蓝饰雀', '侏蓬背鹟', '黑领鹑雀', '巧扇尾莺', '红黄拟䴕', '白眉薮鸲', '红嘴火雀',
                '红嘴弯嘴犀鸟', '红嘴牛椋鸟', '红颊蓝饰雀', '赤胸杜鹃', '红眼斑鸠', '红额拟䴕', '红脸森莺',
                '红额钟声拟䴕', '红脸娇莺', '红头蓝嘴雀', '红头编织雀', '肯尼亚黄腰丝雀', '金腰燕', '红翅椋鸟',
                '环颈斑鸠', '灰喉燕', '短冠紫蕉鹃', '卢氏丽椋鸟', '棕红鸫鹛', '埃及圣鹮', '赤胸花蜜鸟', '白冠歌䳭',
                '鳞喉响蜜䴕', '谢氏丽椋鸟', '银颊噪犀鸟', '歌扇尾莺', '细嘴绿鹎', '暗灰黑伯劳', '细尾夜鹰', '南非黑鹟',
                '黄腹绿鹎', '索马里山雀', '东非丝雀', '领伯劳', '斑鼠鸟', '斑鸽', '眼斑织巢鸟', '斑肋拟䴕',
                '点额织布鸟', '斑晨鸫', '黑胸麦鸡', '白翅黄池鹭', '绿鹭', '条纹丝雀', '斯氏狭尾椋鸟', '橙胸丛林伯劳',
                '栗头丽椋鸟', '塔卡花蜜鸟', '褐胁鹪莺', '白胸森鸠', '欧歌鸲', '热带黑鵙', '杂色花蜜鸟', '白腹紫椋鸟',
                '黑头织巢鸟', '蛋黄黑脸织雀', '高山栗翅椋鸟', '白腹灰蕉鹃', '白眉歌䳭', '纹胸织布鸟', '白额蜂虎',
                '白腹丝雀', '白眉鸦鹃', '白眉森莺', '白胸山雀', '白头牛文鸟', '灰白绣眼鸟', '白额山鹪莺', '白冠蕉鹃',
                '白眼黑鹟', '白头锯翅燕', '长冠盔鵙', '罗伯氏林鵙/白腰林鵙', '线尾燕', '欧柳莺', '林地翡翠', '林鹬',
                '白喉蜂虎', '黄胸娇莺', '黄嘴拟䴕', '非洲黄嘴鸭', '黄嘴孤莺', '黄腹绿鸫鹎', '黄嘴鹮鹳', '黄顶丝雀',
                '黄额丝雀', '黄巧织雀', '黄颈裸喉鹧鸪', '金腰钟声拟䴕', '黄斑拟䴕', '黄斑石雀', '黄喉绿鸫鹎',
                '黄须绿鹎']

NAME_EN_LIST = ["abethr1", "abhori1", "abythr1", "afbfly1", "afdfly1", "afecuc1", "affeag1", "afgfly1", "afghor1",
                "afmdov1", "afpfly1", "afpkin1", "afpwag1", "afrgos1", "afrgrp1", "afrjac1", "afrthr1", "amesun2",
                "augbuz1", "bagwea1", "barswa", "bawhor2", "bawman1", "bcbeat1", "beasun2", "bkctch1", "bkfruw1",
                "blacra1", "blacuc1", "blakit1", "blaplo1", "blbpuf2", "blcapa2", "blfbus1", "blhgon1", "blhher1",
                "blksaw1", "blnmou1", "blnwea1", "bltapa1", "bltbar1", "bltori1", "blwlap1", "brcale1", "brcsta1",
                "brctch1", "brcwea1", "brican1", "brobab1", "broman1", "brosun1", "brrwhe3", "brtcha1", "brubru1",
                "brwwar1", "bswdov1", "btweye2", "bubwar2", "butapa1", "cabgre1", "carcha1", "carwoo1", "categr",
                "ccbeat1", "chespa1", "chewea1", "chibat1", "chtapa3", "chucis1", "cibwar1", "cohmar1", "colsun2",
                "combul2", "combuz1", "comsan", "crefra2", "crheag1", "crohor1", "darbar1", "darter3", "didcuc1",
                "dotbar1", "dutdov1", "easmog1", "eaywag1", "edcsun3", "egygoo", "equaka1", "eswdov1", "eubeat1",
                "fatrav1", "fatwid1", "fislov1", "fotdro5", "gabgos2", "gargan", "gbesta1", "gnbcam2", "gnhsun1",
                "gobbun1", "gobsta5", "gobwea1", "golher1", "grbcam1", "grccra1", "grecor", "greegr", "grewoo2",
                "grwpyt1", "gryapa1", "grywrw1", "gybfis1", "gycwar3", "gyhbus1", "gyhkin1", "gyhneg1", "gyhspa1",
                "gytbar1", "hadibi1", "hamerk1", "hartur1", "helgui", "hipbab1", "hoopoe", "huncis1", "hunsun2",
                "joygre1", "kerspa2", "klacuc1", "kvbsun1", "laudov1", "lawgol", "lesmaw1", "lessts1", "libeat1",
                "litegr", "litswi1", "litwea1", "loceag1", "lotcor1", "lotlap1", "luebus1", "mabeat1", "macshr1",
                "malkin1", "marsto1", "marsun2", "mcptit1", "meypar1", "moccha1", "mouwag1", "ndcsun2", "nobfly1",
                "norbro1", "norcro1", "norfis1", "norpuf1", "nubwoo1", "pabspa1", "palfly2", "palpri1", "piecro1",
                "piekin1", "pitwhy", "purgre2", "pygbat1", "quailf1", "ratcis1", "raybar1", "rbsrob1", "rebfir2",
                "rebhor1", "reboxp1", "reccor", "reccuc1", "reedov1", "refbar2", "refcro1", "reftin1", "refwar2",
                "rehblu1", "rehwea1", "reisee2", "rerswa1", "rewsta1", "rindov", "rocmar2", "rostur1", "ruegls1",
                "rufcha2", "sacibi2", "sccsun2", "scrcha1", "scthon1", "shesta1", "sichor1", "sincis1", "slbgre1",
                "slcbou1", "sltnig1", "sobfly1", "somgre1", "somtit4", "soucit1", "soufis1", "spemou2", "spepig1",
                "spewea1", "spfbar1", "spfwea1", "spmthr1", "spwlap1", "squher1", "strher", "strsee1", "stusta1",
                "subbus1", "supsta1", "tacsun1", "tafpri1", "tamdov1", "thrnig1", "trobou1", "varsun2", "vibsta2",
                "vilwea1", "vimwea1", "walsta1", "wbgbir1", "wbrcha2", "wbswea1", "wfbeat1", "whbcan1", "whbcou1",
                "whbcro2", "whbtit5", "whbwea1", "whbwhe3", "whcpri2", "whctur2", "wheslf1", "whhsaw1", "whihel1",
                "whrshr1", "witswa1", "wlwwar", "wookin1", "woosan", "wtbeat1", "yebapa1", "yebbar1", "yebduc1",
                "yebere1", "yebgre1", "yebsto1", "yeccan1", "yefcan", "yelbis1", "yenspu1", "yertin1", "yesbar1",
                "yespet1", "yetgre1", "yewgre1"]
