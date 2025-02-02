from django.core.management.base import BaseCommand
from core.models import Continent, Federation, Country

# Данные о федерациях и континентах
FEDERATIONS = [
    ("КОНКАКАФ", "Конфедерация футбола Северной, Центральной Америки и стран Карибского бассейна",
     "Северная и Центральная Америка"),
    ("КОНМЕБОЛ", "Южноамериканская футбольная конфедерация", "Южная Америка"),
    ("УЕФА", "Союз европейских футбольных ассоциаций", "Европа"),
    ("КАФ", "Африканская конфедерация футбола", "Африка"),
    ("АФК", "Азиатская конфедерация футбола", "Азия"),
    ("ОФК", "Конфедерация футбола Океании", "Океания"),
]

# Данные о странах (пример для УЕФА)
COUNTRIES_BY_FEDERATION = {
    "OФК": [
        ("ASA", "Американское Самоа", "Территория Американское Самоа", "https://flagcdn.com/w320/as.png", "Американское Самоа — зависимая территория США."),
        ("COK", "Острова Кука", "Острова Кука", "https://flagcdn.com/w320/ck.png", "Острова Кука находятся в свободной ассоциации с Новой Зеландией."),
        ("FJI", "Фиджи", "Республика Фиджи", "https://flagcdn.com/w320/fj.png", "Фиджи — одно из самых крупных государств Океании."),
        ("NCL", "Новая Каледония", "Новая Каледония", "https://flagcdn.com/w320/nc.png", "Новая Каледония — заморская территория Франции."),
        ("NZL", "Новая Зеландия", "Новая Зеландия", "https://flagcdn.com/w320/nz.png", "Новая Зеландия — сильнейшая футбольная нация в ОФК."),
        ("PNG", "Папуа — Новая Гвинея", "Независимое Государство Папуа — Новая Гвинея", "https://flagcdn.com/w320/pg.png", "Папуа — Новая Гвинея расположена в Океании и Азии."),
        ("SAM", "Самоа", "Независимое Государство Самоа", "https://flagcdn.com/w320/ws.png", "Самоа получило независимость от Новой Зеландии в 1962 году."),
        ("SOL", "Соломоновы Острова", "Соломоновы Острова", "https://flagcdn.com/w320/sb.png", "Соломоновы Острова — архипелаг в южной части Тихого океана."),
        ("TAH", "Таити", "Французская Полинезия", "https://flagcdn.com/w320/pf.png", "Таити — заморская территория Франции."),
        ("TGA", "Тонга", "Королевство Тонга", "https://flagcdn.com/w320/to.png", "Тонга — одно из немногих королевств в Океании."),
        ("VAN", "Вануату", "Республика Вануату", "https://flagcdn.com/w320/vu.png", "Вануату состоит из более чем 80 островов.")
    ],
    "АФК": [
        ("AFG", "Афганистан", "Исламская Республика Афганистан", "https://flagcdn.com/w320/af.png", "Афганистан расположен в Южной Азии."),
        ("AUS", "Австралия", "Содружество Австралии", "https://flagcdn.com/w320/au.png", "Австралия присоединилась к АФК в 2006 году."),
        ("BHR", "Бахрейн", "Королевство Бахрейн", "https://flagcdn.com/w320/bh.png", "Бахрейн — островное государство в Персидском заливе."),
        ("BAN", "Бангладеш", "Народная Республика Бангладеш", "https://flagcdn.com/w320/bd.png", "Бангладеш — одна из самых густонаселенных стран мира."),
        ("BTN", "Бутан", "Королевство Бутан", "https://flagcdn.com/w320/bt.png", "Бутан известен своим индексом национального счастья."),
        ("BRN", "Бруней", "Бруней-Даруссалам", "https://flagcdn.com/w320/bn.png", "Бруней — небольшое богатое государство в Юго-Восточной Азии."),
        ("CAM", "Камбоджа", "Королевство Камбоджа", "https://flagcdn.com/w320/kh.png", "Камбоджа известна храмовым комплексом Ангкор-Ват."),
        ("CHN", "Китай", "Китайская Народная Республика", "https://flagcdn.com/w320/cn.png", "Китай — самая населённая страна мира."),
        ("HKG", "Гонконг", "Гонконг (особый административный район Китая)", "https://flagcdn.com/w320/hk.png", "Гонконг имеет отдельную футбольную федерацию."),
        ("IND", "Индия", "Республика Индия", "https://flagcdn.com/w320/in.png", "Индия — одна из крупнейших экономик Азии."),
        ("IDN", "Индонезия", "Республика Индонезия", "https://flagcdn.com/w320/id.png", "Индонезия — крупнейшее островное государство в мире."),
        ("IRN", "Иран", "Исламская Республика Иран", "https://flagcdn.com/w320/ir.png", "Иран — один из ведущих футбольных центров Азии."),
        ("IRQ", "Ирак", "Республика Ирак", "https://flagcdn.com/w320/iq.png", "Ирак имеет богатую историю и культуру."),
        ("JPN", "Япония", "Япония", "https://flagcdn.com/w320/jp.png", "Япония — одна из сильнейших футбольных стран Азии."),
        ("JOR", "Иордания", "Иорданское Хашимитское Королевство", "https://flagcdn.com/w320/jo.png", "Иордания расположена в Западной Азии."),
        ("KOR", "Южная Корея", "Республика Корея", "https://flagcdn.com/w320/kr.png", "Южная Корея — один из лидеров азиатского футбола."),
        ("KUW", "Кувейт", "Государство Кувейт", "https://flagcdn.com/w320/kw.png", "Кувейт имеет богатую футбольную историю."),
        ("KGZ", "Киргизия", "Кыргызская Республика", "https://flagcdn.com/w320/kg.png", "Киргизия расположена в Центральной Азии."),
        ("LAO", "Лаос", "Лаосская Народно-Демократическая Республика", "https://flagcdn.com/w320/la.png", "Лаос — одна из наименее развитых стран региона."),
        ("LBN", "Ливан", "Ливанская Республика", "https://flagcdn.com/w320/lb.png", "Ливан имеет давние футбольные традиции."),
        ("MAC", "Макао", "Макао (особый административный район Китая)", "https://flagcdn.com/w320/mo.png", "Макао участвует в турнирах АФК как отдельная команда."),
        ("MAS", "Малайзия", "Малайзия", "https://flagcdn.com/w320/my.png", "Малайзия является активным участником АФК."),
        ("MDV", "Мальдивы", "Мальдивская Республика", "https://flagcdn.com/w320/mv.png", "Мальдивы — островное государство в Индийском океане."),
        ("MNG", "Монголия", "Монголия", "https://flagcdn.com/w320/mn.png", "Монголия — одна из крупнейших по территории стран Азии."),
        ("MYA", "Мьянма", "Республика Союз Мьянма", "https://flagcdn.com/w320/mm.png", "Мьянма имеет долгую футбольную историю."),
        ("NEP", "Непал", "Федеративная Демократическая Республика Непал", "https://flagcdn.com/w320/np.png", "Непал известен Гималаями и Эверестом."),
        ("OMA", "Оман", "Султанат Оман", "https://flagcdn.com/w320/om.png", "Оман активно развивает футбол в регионе."),
        ("PAK", "Пакистан", "Исламская Республика Пакистан", "https://flagcdn.com/w320/pk.png", "Пакистан исторически связан с футболом через британское наследие."),
        ("PAL", "Палестина", "Государство Палестина", "https://flagcdn.com/w320/ps.png", "Палестина признана в соревнованиях АФК."),
        ("PHI", "Филиппины", "Республика Филиппины", "https://flagcdn.com/w320/ph.png", "Филиппины активно развивают футбол."),
        ("QAT", "Катар", "Государство Катар", "https://flagcdn.com/w320/qa.png", "Катар был хозяином ЧМ-2022."),
        ("KSA", "Саудовская Аравия", "Королевство Саудовская Аравия", "https://flagcdn.com/w320/sa.png", "Саудовская Аравия — один из ведущих футбольных центров Азии."),
        ("SGP", "Сингапур", "Республика Сингапур", "https://flagcdn.com/w320/sg.png", "Сингапур — небольшое, но влиятельное государство в Юго-Восточной Азии."),
        ("SRI", "Шри-Ланка", "Демократическая Социалистическая Республика Шри-Ланка", "https://flagcdn.com/w320/lk.png", "Шри-Ланка находится в Южной Азии."),
        ("SYR", "Сирия", "Сирийская Арабская Республика", "https://flagcdn.com/w320/sy.png", "Сирия участвует в соревнованиях АФК."),
        ("TJK", "Таджикистан", "Республика Таджикистан", "https://flagcdn.com/w320/tj.png", "Таджикистан активно развивает футбол."),
        ("THA", "Таиланд", "Королевство Таиланд", "https://flagcdn.com/w320/th.png", "Таиланд — сильная футбольная нация в Юго-Восточной Азии."),
        ("TLS", "Восточный Тимор", "Демократическая Республика Тимор-Лесте", "https://flagcdn.com/w320/tl.png", "Одна из самых молодых стран в АФК."),
        ("TKM", "Туркменистан", "Туркменистан", "https://flagcdn.com/w320/tm.png", "Туркменистан активно развивает спорт."),
        ("UAE", "ОАЭ", "Объединенные Арабские Эмираты", "https://flagcdn.com/w320/ae.png", "ОАЭ имеют сильный футбольный чемпионат."),
        ("UZB", "Узбекистан", "Республика Узбекистан", "https://flagcdn.com/w320/uz.png", "Узбекистан — одна из сильнейших футбольных стран Центральной Азии."),
        ("VIE", "Вьетнам", "Социалистическая Республика Вьетнам", "https://flagcdn.com/w320/vn.png", "Вьетнам активно развивает футбол.")
    ],
    "КАФ": [
        ("ALG", "Алжир", "Алжирская Народная Демократическая Республика", "https://flagcdn.com/w320/dz.png", "Алжир — крупнейшая страна Африки по площади."),
        ("ANG", "Ангола", "Республика Ангола", "https://flagcdn.com/w320/ao.png", "Ангола расположена на юго-западе Африки."),
        ("BEN", "Бенин", "Республика Бенин", "https://flagcdn.com/w320/bj.png", "Бенин находится в Западной Африке."),
        ("BFA", "Буркина-Фасо", "Буркина-Фасо", "https://flagcdn.com/w320/bf.png", "Буркина-Фасо — государство в Западной Африке."),
        ("BDI", "Бурунди", "Республика Бурунди", "https://flagcdn.com/w320/bi.png", "Бурунди расположена в регионе Великих Африканских озер."),
        ("BOT", "Ботсвана", "Республика Ботсвана", "https://flagcdn.com/w320/bw.png", "Ботсвана славится своей природой и национальными парками."),
        ("CPV", "Кабо-Верде", "Республика Кабо-Верде", "https://flagcdn.com/w320/cv.png", "Островное государство в Атлантическом океане."),
        ("CMR", "Камерун", "Республика Камерун", "https://flagcdn.com/w320/cm.png", "Камерун — одна из самых успешных африканских футбольных стран."),
        ("CAF", "ЦАР", "Центральноафриканская Республика", "https://flagcdn.com/w320/cf.png", "ЦАР расположена в самом сердце Африки."),
        ("CHA", "Чад", "Республика Чад", "https://flagcdn.com/w320/td.png", "Чад — страна с разнообразным климатом от пустынь до саванн."),
        ("COM", "Коморы", "Союз Коморских Островов", "https://flagcdn.com/w320/km.png", "Коморы — небольшое островное государство в Индийском океане."),
        ("CGO", "Республика Конго", "Республика Конго", "https://flagcdn.com/w320/cg.png", "Республика Конго граничит с Демократической Республикой Конго."),
        ("COD", "ДР Конго", "Демократическая Республика Конго", "https://flagcdn.com/w320/cd.png", "Одна из крупнейших стран Африки по площади."),
        ("CIV", "Кот-д’Ивуар", "Республика Кот-д’Ивуар", "https://flagcdn.com/w320/ci.png", "Кот-д’Ивуар известен своими кофейными плантациями."),
        ("DJI", "Джибути", "Республика Джибути", "https://flagcdn.com/w320/dj.png", "Джибути расположена на стратегическом перекрестке Африки и Аравии."),
        ("EGY", "Египет", "Арабская Республика Египет", "https://flagcdn.com/w320/eg.png", "Египет — одна из древнейших цивилизаций в мире."),
        ("EQG", "Экваториальная Гвинея", "Республика Экваториальная Гвинея", "https://flagcdn.com/w320/gq.png", "Одна из немногих стран Африки, где официальный язык — испанский."),
        ("ERI", "Эритрея", "Государство Эритрея", "https://flagcdn.com/w320/er.png", "Эритрея расположена на побережье Красного моря."),
        ("ETH", "Эфиопия", "Федеративная Демократическая Республика Эфиопия", "https://flagcdn.com/w320/et.png", "Эфиопия — одна из древнейших стран мира."),
        ("GAB", "Габон", "Габонская Республика", "https://flagcdn.com/w320/ga.png", "Габон богат природными ресурсами."),
        ("GAM", "Гамбия", "Республика Гамбия", "https://flagcdn.com/w320/gm.png", "Гамбия — самая маленькая страна на континенте."),
        ("GHA", "Гана", "Республика Гана", "https://flagcdn.com/w320/gh.png", "Гана известна своими золотыми запасами."),
        ("GUI", "Гвинея", "Гвинейская Республика", "https://flagcdn.com/w320/gn.png", "Гвинея богата природными ресурсами."),
        ("GNB", "Гвинея-Бисау", "Республика Гвинея-Бисау", "https://flagcdn.com/w320/gw.png", "Небольшая страна в Западной Африке."),
        ("KEN", "Кения", "Республика Кения", "https://flagcdn.com/w320/ke.png", "Кения славится своей природой и сафари."),
        ("LES", "Лесото", "Королевство Лесото", "https://flagcdn.com/w320/ls.png", "Лесото — государство, полностью окруженное ЮАР."),
        ("LBR", "Либерия", "Республика Либерия", "https://flagcdn.com/w320/lr.png", "Либерия была основана освобожденными американскими рабами."),
        ("LBY", "Ливия", "Государство Ливия", "https://flagcdn.com/w320/ly.png", "Ливия располагается в Северной Африке."),
        ("MAD", "Мадагаскар", "Республика Мадагаскар", "https://flagcdn.com/w320/mg.png", "Островное государство с уникальной флорой и фауной."),
        ("MWI", "Малави", "Республика Малави", "https://flagcdn.com/w320/mw.png", "Малави славится своими озерами."),
        ("MLI", "Мали", "Республика Мали", "https://flagcdn.com/w320/ml.png", "Мали была центром древних африканских цивилизаций."),
        ("MAR", "Марокко", "Королевство Марокко", "https://flagcdn.com/w320/ma.png", "Марокко — страна с богатой историей и культурой."),
        ("MTN", "Мавритания", "Исламская Республика Мавритания", "https://flagcdn.com/w320/mr.png", "Мавритания — страна в Северо-Западной Африке."),
        ("MOZ", "Мозамбик", "Республика Мозамбик", "https://flagcdn.com/w320/mz.png", "Мозамбик имеет длинную береговую линию на Индийском океане."),
        ("NAM", "Намибия", "Республика Намибия", "https://flagcdn.com/w320/na.png", "Намибия знаменита пустыней Намиб."),
        ("NGA", "Нигерия", "Федеративная Республика Нигерия", "https://flagcdn.com/w320/ng.png", "Нигерия — самая густонаселенная страна Африки."),
        ("RWA", "Руанда", "Республика Руанда", "https://flagcdn.com/w320/rw.png", "Руанда известна своей программой восстановления экономики."),
        ("SEN", "Сенегал", "Республика Сенегал", "https://flagcdn.com/w320/sn.png", "Сенегал славится своим футбольным наследием."),
        ("ZAF", "ЮАР", "Южно-Африканская Республика", "https://flagcdn.com/w320/za.png", "ЮАР провела ЧМ-2010, первый в Африке."),
        ("ZAM", "Замбия", "Республика Замбия", "https://flagcdn.com/w320/zm.png", "Замбия знаменита водопадом Виктория."),
        ("ZIM", "Зимбабве", "Республика Зимбабве", "https://flagcdn.com/w320/zw.png", "Зимбабве славится древними руинами Великих Зимбабве.")
    ],
    "КОНКАКАФ": [
        ("AIA", "Ангилья", "Ангилья", "https://flagcdn.com/w320/ai.png",
         "Британская заморская территория в Карибском море."),
        ("ATG", "Антигуа и Барбуда", "Антигуа и Барбуда", "https://flagcdn.com/w320/ag.png",
         "Островное государство в Карибском бассейне."),
        ("ABW", "Аруба", "Аруба", "https://flagcdn.com/w320/aw.png", "Нидерландская территория в Карибском море."),
        ("BAH", "Багамы", "Содружество Багамских Островов", "https://flagcdn.com/w320/bs.png",
         "Островное государство на севере Карибского моря."),
        ("BRB", "Барбадос", "Барбадос", "https://flagcdn.com/w320/bb.png", "Островное государство в Вест-Индии."),
        ("BLZ", "Белиз", "Белиз", "https://flagcdn.com/w320/bz.png", "Государство в Центральной Америке."),
        ("BER", "Бермуды", "Бермудские острова", "https://flagcdn.com/w320/bm.png",
         "Британская заморская территория в Атлантике."),
        ("VGB", "Британские Виргинские Острова", "Британские Виргинские Острова", "https://flagcdn.com/w320/vg.png",
         "Британская заморская территория в Карибском море."),
        ("CAN", "Канада", "Канада", "https://flagcdn.com/w320/ca.png", "Вторая по величине страна в мире."),
        ("CAY", "Каймановы острова", "Каймановы острова", "https://flagcdn.com/w320/ky.png",
         "Британская заморская территория в Карибском море."),
        ("CRC", "Коста-Рика", "Республика Коста-Рика", "https://flagcdn.com/w320/cr.png",
         "Государство в Центральной Америке."),
        (
        "CUB", "Куба", "Республика Куба", "https://flagcdn.com/w320/cu.png", "Островное государство в Карибском море."),
        ("CUW", "Кюрасао", "Кюрасао", "https://flagcdn.com/w320/cw.png",
         "Автономная территория в составе Королевства Нидерландов."),
        ("DMA", "Доминика", "Содружество Доминики", "https://flagcdn.com/w320/dm.png",
         "Островное государство в Карибском море."),
        ("DOM", "Доминиканская Республика", "Доминиканская Республика", "https://flagcdn.com/w320/do.png",
         "Государство на острове Эспаньола."),
        ("SLV", "Сальвадор", "Республика Эль-Сальвадор", "https://flagcdn.com/w320/sv.png",
         "Самая маленькая страна Центральной Америки."),
        ("GRD", "Гренада", "Гренада", "https://flagcdn.com/w320/gd.png", "Островное государство в Карибском море."),
        (
        "GUA", "Гватемала", "Республика Гватемала", "https://flagcdn.com/w320/gt.png", "Страна в Центральной Америке."),
        ("GUY", "Гайана", "Кооперативная Республика Гайана", "https://flagcdn.com/w320/gy.png",
         "Государство в северной части Южной Америки."),
        ("HAI", "Гаити", "Республика Гаити", "https://flagcdn.com/w320/ht.png", "Государство на острове Эспаньола."),
        ("HON", "Гондурас", "Республика Гондурас", "https://flagcdn.com/w320/hn.png",
         "Центральноамериканская страна с выходом к Карибскому морю."),
        ("JAM", "Ямайка", "Ямайка", "https://flagcdn.com/w320/jm.png", "Островное государство в Карибском море."),
        ("MTQ", "Мартиника", "Мартиника", "https://flagcdn.com/w320/mq.png",
         "Французский заморский департамент в Карибском море."),
        ("MEX", "Мексика", "Мексиканские Соединённые Штаты", "https://flagcdn.com/w320/mx.png",
         "Страна в Северной Америке."),
        ("MSR", "Монтсеррат", "Монтсеррат", "https://flagcdn.com/w320/ms.png",
         "Британская заморская территория в Карибском море."),
        ("NCA", "Никарагуа", "Республика Никарагуа", "https://flagcdn.com/w320/ni.png",
         "Государство в Центральной Америке."),
        ("PAN", "Панама", "Республика Панама", "https://flagcdn.com/w320/pa.png",
         "Страна, соединяющая Северную и Южную Америку."),
        ("PUR", "Пуэрто-Рико", "Пуэрто-Рико", "https://flagcdn.com/w320/pr.png",
         "Ненаселённая территория США в Карибском море."),
        ("SKN", "Сент-Китс и Невис", "Федерация Сент-Китс и Невис", "https://flagcdn.com/w320/kn.png",
         "Островное государство в Карибском море."),
        ("LCA", "Сент-Люсия", "Сент-Люсия", "https://flagcdn.com/w320/lc.png",
         "Островное государство в Карибском море."),
        ("VCT", "Сент-Винсент и Гренадины", "Сент-Винсент и Гренадины", "https://flagcdn.com/w320/vc.png",
         "Островное государство в Карибском море."),
        ("SUR", "Суринам", "Республика Суринам", "https://flagcdn.com/w320/sr.png",
         "Страна в северной части Южной Америки."),
        ("TCA", "Теркс и Кайкос", "Теркс и Кайкос", "https://flagcdn.com/w320/tc.png",
         "Британская заморская территория в Карибском море."),
        ("TTO", "Тринидад и Тобаго", "Республика Тринидад и Тобаго", "https://flagcdn.com/w320/tt.png",
         "Островное государство у берегов Южной Америки."),
        ("USA", "США", "Соединённые Штаты Америки", "https://flagcdn.com/w320/us.png", "Крупнейшая экономика мира."),
        ("VIR", "Американские Виргинские острова", "Американские Виргинские острова", "https://flagcdn.com/w320/vi.png",
         "Заморская территория США в Карибском море.")
    ],
    "КОНМЕБОЛ": [
        ("ARG", "Аргентина", "Аргентинская Республика", "https://flagcdn.com/w320/ar.png", "Аргентина — родина футбольной легенды Диего Марадоны."),
        ("BOL", "Боливия", "Многонациональное Государство Боливия", "https://flagcdn.com/w320/bo.png", "Боливия расположена в центральной части Южной Америки."),
        ("BRA", "Бразилия", "Федеративная Республика Бразилия", "https://flagcdn.com/w320/br.png", "Бразилия — страна с пятью победами на чемпионатах мира."),
        ("CHI", "Чили", "Республика Чили", "https://flagcdn.com/w320/cl.png", "Чили занимает узкую полосу земли вдоль западного побережья Южной Америки."),
        ("COL", "Колумбия", "Республика Колумбия", "https://flagcdn.com/w320/co.png", "Колумбия известна своей футбольной культурой и выдающимися игроками."),
        ("ECU", "Эквадор", "Республика Эквадор", "https://flagcdn.com/w320/ec.png", "Эквадор расположен на экваторе и имеет разнообразный климат."),
        ("PAR", "Парагвай", "Республика Парагвай", "https://flagcdn.com/w320/py.png", "Парагвай — страна без выхода к морю в Южной Америке."),
        ("PER", "Перу", "Республика Перу", "https://flagcdn.com/w320/pe.png", "Перу — родина древней цивилизации инков."),
        ("URU", "Уругвай", "Восточная Республика Уругвай", "https://flagcdn.com/w320/uy.png", "Уругвай выиграл первый чемпионат мира по футболу в 1930 году."),
        ("VEN", "Венесуэла", "Боливарианская Республика Венесуэла", "https://flagcdn.com/w320/ve.png", "Венесуэла славится своей природной красотой и нефтяными ресурсами.")
    ],
    "УЕФА": [
        ("ALB", "Албания", "Республика Албания", "https://flagcdn.com/w320/al.png",
         "Албания расположена на Балканском полуострове в Юго-Восточной Европе."),
        ("AND", "Андорра", "Княжество Андорра", "https://flagcdn.com/w320/ad.png",
         "Андорра — небольшое княжество в Пиренеях."),
        ("ARM", "Армения", "Республика Армения", "https://flagcdn.com/w320/am.png",
         "Армения — страна на Южном Кавказе."),
        ("AUT", "Австрия", "Австрийская Республика", "https://flagcdn.com/w320/at.png",
         "Австрия — страна в Центральной Европе."),
        ("AZE", "Азербайджан", "Азербайджанская Республика", "https://flagcdn.com/w320/az.png",
         "Азербайджан находится в Закавказье."),
        ("BEL", "Бельгия", "Королевство Бельгия", "https://flagcdn.com/w320/be.png",
         "Бельгия — страна в Западной Европе."),
        ("BIH", "Босния и Герцеговина", "Босния и Герцеговина", "https://flagcdn.com/w320/ba.png",
         "Балканская страна с богатой историей."),
        ("BLR", "Беларусь", "Республика Беларусь", "https://flagcdn.com/w320/by.png",
         "Беларусь находится в Восточной Европе."),
        ("CRO", "Хорватия", "Республика Хорватия", "https://flagcdn.com/w320/hr.png",
         "Хорватия имеет выход к Адриатическому морю."),
        ("CYP", "Кипр", "Республика Кипр", "https://flagcdn.com/w320/cy.png",
         "Кипр — островное государство в Средиземном море."),
        ("CZE", "Чехия", "Чешская Республика", "https://flagcdn.com/w320/cz.png",
         "Чехия славится своими замками и пивом."),
        ("DEN", "Дания", "Королевство Дания", "https://flagcdn.com/w320/dk.png",
         "Дания является скандинавской страной."),
        ("ENG", "Англия", "Англия", "https://flagcdn.com/w320/gb-eng.png", "Англия — родина футбола."),
        ("EST", "Эстония", "Эстонская Республика", "https://flagcdn.com/w320/ee.png", "Эстония — страна Балтии."),
        ("FIN", "Финляндия", "Финляндская Республика", "https://flagcdn.com/w320/fi.png",
         "Финляндия известна своими озерами и лесами."),
        ("FRA", "Франция", "Французская Республика", "https://flagcdn.com/w320/fr.png",
         "Франция — крупнейшая страна Западной Европы."),
        ("GEO", "Грузия", "Грузия", "https://flagcdn.com/w320/ge.png", "Грузия расположена на стыке Европы и Азии."),
        ("GER", "Германия", "Федеративная Республика Германия", "https://flagcdn.com/w320/de.png",
         "Германия — крупнейшая экономика Европы."),
        ("GIB", "Гибралтар", "Гибралтар", "https://flagcdn.com/w320/gi.png",
         "Британская заморская территория в южной Европе."),
        ("GRE", "Греция", "Греческая Республика", "https://flagcdn.com/w320/gr.png",
         "Греция — колыбель западной цивилизации."),
        ("HUN", "Венгрия", "Венгерская Республика", "https://flagcdn.com/w320/hu.png",
         "Венгрия славится своими термальными источниками."),
        ("ISL", "Исландия", "Республика Исландия", "https://flagcdn.com/w320/is.png",
         "Исландия известна своими вулканами и гейзерами."),
        ("IRL", "Ирландия", "Республика Ирландия", "https://flagcdn.com/w320/ie.png",
         "Ирландия славится своими зелеными лугами."),
        ("ISR", "Израиль", "Государство Израиль", "https://flagcdn.com/w320/il.png",
         "Израиль — страна в Западной Азии, выступающая в УЕФА."),
        ("ITA", "Италия", "Итальянская Республика", "https://flagcdn.com/w320/it.png",
         "Италия известна своей кухней и древними городами."),
        ("KAZ", "Казахстан", "Республика Казахстан", "https://flagcdn.com/w320/kz.png",
         "Казахстан частично расположен в Европе и Азии."),
        ("LVA", "Латвия", "Латвийская Республика", "https://flagcdn.com/w320/lv.png", "Латвия — страна Балтии."),
        ("LIE", "Лихтенштейн", "Княжество Лихтенштейн", "https://flagcdn.com/w320/li.png",
         "Лихтенштейн — небольшое альпийское княжество."),
        ("LTU", "Литва", "Литовская Республика", "https://flagcdn.com/w320/lt.png",
         "Литва — самая южная из стран Балтии."),
        ("LUX", "Люксембург", "Великое Герцогство Люксембург", "https://flagcdn.com/w320/lu.png",
         "Люксембург — одно из богатейших государств Европы."),
        ("MLT", "Мальта", "Республика Мальта", "https://flagcdn.com/w320/mt.png",
         "Мальта — островное государство в Средиземном море."),
        ("MDA", "Молдова", "Республика Молдова", "https://flagcdn.com/w320/md.png",
         "Молдова расположена в Восточной Европе."),
        ("MON", "Монако", "Княжество Монако", "https://flagcdn.com/w320/mc.png",
         "Монако — небольшое княжество на Лазурном берегу."),
        ("MNE", "Черногория", "Республика Черногория", "https://flagcdn.com/w320/me.png",
         "Черногория славится своими горными пейзажами и Адриатическим побережьем."),
        ("NED", "Нидерланды", "Королевство Нидерландов", "https://flagcdn.com/w320/nl.png",
         "Нидерланды известны своими каналами и тюльпанами."),
        ("MKD", "Северная Македония", "Республика Северная Македония", "https://flagcdn.com/w320/mk.png",
         "Балканская страна с богатой историей."),
        ("NOR", "Норвегия", "Королевство Норвегия", "https://flagcdn.com/w320/no.png",
         "Норвегия славится фьордами и северным сиянием."),
        ("POL", "Польша", "Республика Польша", "https://flagcdn.com/w320/pl.png",
         "Польша — крупнейшая страна Центральной Европы."),
        ("POR", "Португалия", "Португальская Республика", "https://flagcdn.com/w320/pt.png",
         "Португалия известна своими пляжами и вином."),
        ("ROU", "Румыния", "Румыния", "https://flagcdn.com/w320/ro.png", "Румыния славится замками и Карпатами."),
        ("RUS", "Россия", "Российская Федерация", "https://flagcdn.com/w320/ru.png", "Крупнейшая страна в мире."),
        ("SCO", "Шотландия", "Шотландия", "https://flagcdn.com/w320/gb-sct.png",
         "Шотландия известна замками и традициями."),
        ("SMR", "Сан-Марино", "Республика Сан-Марино", "https://flagcdn.com/w320/sm.png",
         "Одно из самых маленьких государств Европы."),
        ("SRB", "Сербия", "Республика Сербия", "https://flagcdn.com/w320/rs.png",
         "Сербия находится в центральной части Балкан."),
        ("SVK", "Словакия", "Словацкая Республика", "https://flagcdn.com/w320/sk.png",
         "Словакия славится своими замками и горами."),
        ("SVN", "Словения", "Республика Словения", "https://flagcdn.com/w320/si.png",
         "Небольшая страна с выходом к Адриатике."),
        ("ESP", "Испания", "Королевство Испания", "https://flagcdn.com/w320/es.png",
         "Испания известна корридой и фламенко."),
        ("SWE", "Швеция", "Королевство Швеция", "https://flagcdn.com/w320/se.png",
         "Скандинавская страна с высоким уровнем жизни."),
        ("SUI", "Швейцария", "Швейцарская Конфедерация", "https://flagcdn.com/w320/ch.png",
         "Швейцария известна своими Альпами и банками."),
        ("TUR", "Турция", "Турецкая Республика", "https://flagcdn.com/w320/tr.png",
         "Турция находится на стыке Европы и Азии."),
        ("UKR", "Украина", "Украина", "https://flagcdn.com/w320/ua.png",
         "Крупнейшая страна, полностью расположенная в Европе."),
        ("WAL", "Уэльс", "Уэльс", "https://flagcdn.com/w320/gb-wls.png", "Уэльс славится своими замками и природой.")
    ],

    # Добавить остальные конфедерации
}


class Command(BaseCommand):
    help = "Заполняет базу данных федерациями и странами"

    def handle(self, *args, **kwargs):
        for short_name, full_name, continent_name in FEDERATIONS:
            continent, _ = Continent.objects.get_or_create(name=continent_name)
            federation, _ = Federation.objects.get_or_create(
                short_name=short_name, full_name=full_name, continent=continent
            )

            for code, short_name, full_name, flag, description in COUNTRIES_BY_FEDERATION.get(short_name, []):
                Country.objects.get_or_create(
                    code=code,
                    short_name=short_name,
                    full_name=full_name,
                    flag=flag,
                    description=description,
                    federation=federation
                )
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))