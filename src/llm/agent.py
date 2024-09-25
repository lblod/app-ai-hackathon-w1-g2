import csv
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.llm.output_models import output_parser, PossibleActionCategories
from src.llm.prompts import SYSTEM_PROMPT, USER_PROMPT

APP_DIR = Path(__file__).parents[2]
OUTPUT_DIR = APP_DIR / 'data' / 'ai_output'
CSV_HEADERS = ['TextFragment', 'Forbidden', 'PermitNeeded', 'Category']

LLM = ChatOllama(model="mistral-nemo", temperature=0, base_url="http://hackathon-ai-2.s.redhost.be:11434")


def write_output_csv(actions, output_path):
    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(actions)

    print(f"CSV file '{output_path}' has been saved.")


def process_decision(paper: str):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            ("human", USER_PROMPT),
        ]
    ).partial(format_instructions=output_parser.get_format_instructions())
    chain = prompt_template | LLM | output_parser
    actions = chain.invoke({"paper": paper, "action_categories": [e.value for e in PossibleActionCategories]})

    all_actions_data = [
        {'TextFragment': action_item.action, 'Forbidden': action_item.forbidden, 'PermitNeeded':  action_item.permit_needed, 'Category': action_item.category}
        for action_item in actions.action_list
    ]

    filtered_data = [item for item in all_actions_data if item['TextFragment'] is not None]

    csv_file = OUTPUT_DIR / 'actions_some_besluit_alt_21145.csv'
    write_output_csv(actions=filtered_data, output_path=csv_file)
    return all_actions_data


if __name__ == '__main__':
    all_actions = process_decision(paper=""""
Ministerieel besluit tot definitieve bescherming als monument van 
architectenwoning Ferdinand Schlich in Gent (Mariakerke) 
DE VLAAMSE MINISTER VAN BUITENLANDS BELEID EN ONROEREND ERFGOED; 
Gelet op het Onroerenderfgoeddecreet van 12 juli 2013, artikel 6.1.1; 
Gelet op het besluit van de Vlaamse Regering van 25 juli 2014 tot bepaling van de· 
bevoegdheden van de leden van de Vlaamse Regering, artikel 6, 1 °; 
Gelet op het ministerieel besluit van 1 oktober 2018 tot voorlopige bescherming als 
monument van architectenwoning Ferdinand Schlich in Gent (Mariakerke); 
Gelet op het openbaar onderzoek dat gehouden is van 15 oktober tot en met 13 november 
2018 en waarvan de behandeling is opgenomen in bijlage; 
Overwegende dat het waarderend onderzoek, waarvan de resultaten zijn opgenomen in het 
beschermingsdossier, de erfgoedwaarde van architectenwoning Ferdinand Schlich aantoont; 
Overwegende dat architectenwoning Ferdinand Schlich als monument architecturale waarde 
bezit die als volgt wordt gemotiveerd: · 
De woning wordt beschouwd als het meesterwerk van architect Ferdinand Schlich (Gent, 
1949), die een kwalitatief maar klein oeuvre realiseerde, voornamelijk in de regio van Gent. 
Aangezien de woning sinds de oplevering in 1988 amper wijzigingen onderging, vertoont het 
gebouw nog een hele hoge herkenbaarheid. · 
Opgeleid als bouwkundig tekenaar en architect aan het Gents Hoger Architectuurinstituut 
Sint-Lucas eind jaren 1960 en begin jaren 1970, gaf Schlich zelf meer dan 30 jaar lang les 
aan dit instituut. Tijdens zijn opleiding werd hij aanvankelijk beïnvloed door het structuralisme 
(en met name door de vrijheid eri de menselijke maat die door de aanhangers van deze 
stroming werden gepropageerd) en nadien door Juliaan Lampens die hij zijn leermeester 
noemt en van wie hij het belang van monumentaliteit en eenvoud overnam, evenals een 
voorliefde voor de meesters van het modernisme (Mies Van der Rohe en Le Corbusier). Een 
belangrijke inspiratiebron voor Schlich was ook Frank Lloyd Wright en in het bijzonder diens 
prairiehuizen: het integreren van een gebouw in zijn omgeving, daken op verschillende 
hoogte, een vierkante opbouw en asymmetrisch grondplan, een gevarieerde ruimtewerking 
en gebruik van opvallend houten schrijnwerk, lage buitenmuren en metselwerk. Ook bij zijn 
eigen woning is die invloed onmiskenbaar aanwezig. Daarnaast verraadt die woning de 
invloed van de Duitse architect Heinrich Tessenow, met name in het belang van eenvoud en 
proporties, en van het stijlloze traditionele bouwen van 'het volk', mogelijk ook onder invloed 
van Bernard Rudowski's reizende tentoonstelling Architecture without architects (1964-
1975). 
Ondanks de diversiteit van Schlichs oeuvre vertoont het enkele gemeenschappelijke 
kenmerken die ook aanwezig zijn in de architectenwoning, wat deze laatste een zekere 
representativiteit verleent. Een eerste is de aandacht voor ambachtelijke afwerking en 
detaillering, bijvoorbeeld in de uitwerking van het atelierraam en de ateliertrap maar ook van 
meer prozaïsche elementen zoals de gietijzeren radiatoren. Die detaillering stond bij Schlich 
wel steeds ten dienste van een duidelijk herkenbaar geheel wat hij bij zijn eigen woning vond 
in de toepassing van een langgerekt volume. Hiervoor haalde hij inspiratie bij eenvoudige 
Pagina 1 van 5 
adobe huizen in Turkije en Nubië (Zuid-Egypte) maar ook bij Vlaamse hoeves en bij de 
rivierboten die hij traag zag voorbijschuiven vanop zijn bouwgrond aan de Brugse Vaart. Die 
laatste inspiratiebron verwijst ook naar het belang dat Schlich hechtte aan de integratie van 
zijn gebouwen in hun omgeving, in het landschap. Het principe van de gevarieerde 
ruimtewerking, een ander weerkerend kenmerk, paste hij bij zijn eigen woning toe door met 
een aantal centrale muren en schuifdeuren ruimtes van verschillende grootte af te bakenen, 
en door de vensters van de woonkamer aan de achtergevel ter hoogte van de keuken en de 
badkamer te laten doorlopen waardoor deze woonkamer nog groter lijkt dan z.e eigenlijk is. 
Ook het selectief toepassen van verlaagde plafonds sluit aan bij deze zoektocht naar 
ruimtelijke diversiteit. Een laatste weerkerende aandachtspunt in Schlichs oeuvre is zijn 
respect voor het budget van de opdrachtgever. Voor zijn eigen woning stelde hij een 
onwaarschijnlijk laag budget voorop dat bij realisatie slechts in heel beperkte mate 
overschreden werd. De belangrijkste kostenbesparende elementen waren volgens Schlich de 
sterke, op zichzelf staande vorm die geen opsmuk vroeg, het gebruik van een plat dak, een 
redocrete (garage)vloer en een ruwbouw in cellenbeton (die een spouw overbodig maakt), 
het prioritair inzetten op woonkwaliteit (licht, ruimte, geborgenheid en technisch comfort) ten 
koste van de afwerking (die later zou volgen) en zoveel mogelijk zelfbouw. 
Omdat de woning met zo'n laag budget en zo snel gerealiseerd was, kreeg ze heel wat 
belangstelling in de populaire pers. Maar ook in architectuurkringen werd de waarde snel 
erkend, zoals blijkt uit de opname ervan in verscheidene publicaties en uit de toekenning van 
de Architectuurprijs van de provincie Oost-Vlaanderen in 1993. De"jury van deze prijs loofde 
met name de ruimte-indeling en de organisatie en oriëntatie van de verschillende kamers 
onderling. Volgens Schlich zelf lag de waarde van de woning in de eenvoud van de oplossing 
waartoe hij uiteindelijk was gekomen: twee evenwijdige muren op de juiste, meest 
economische afstand van elkaar. Om tot die eenvoud te komen had hij naar eigen zeggen 
pas dan de nodige maturiteit bereikt als architect. 
De woning Schlich is ook een waardevol voorbeeld van het type· architectenwoning, met name 
uit het laatste kwart van de 20ste eeuw. Schlich zag zijn eigen woning duidelijk als een 
gebouwd manifest, een opvoedend-didactisch instrument, zowel voor zijn studenten 
architectuur aan het Hoger Architectuurinstituut Sint-Lucas, als voor het ruime publiek dat 
zelfwilde bouwen. Dit blijkt uit het feit dat hij zijn woning openstelde voor heel wat bezoekers 
en ook voor de populaire pers. Met deze woning wou hij aantonen dat goedkoop en 
betekenisvol bouwen konden samengaan, zoals ook blijkt uit het manifest dat bewaard bleef 
in het archiefdossier van deze woning. Deze betrachting vertaalde zich in een vrij vroege 
toepassing van enkele architecturale kenmerken die heden vrij algemeen toegepast worden, 
zowel qua vormgeving (minimalisme), planopbouw (open) en materiaalgebruik (cellenbeton 
en redocrete vloer). Tegelijkertijd plaatst deze woning ook een belangrijke kanttekening bij 
de opvatting dat de waarde van een architectenwoning vooral gelegen is in het feit dat de 
ontwerper daar zonder compromissen zijn persoonlijke ideeën in realiteit zou kunnen 
omzetten. Hoe compromisloos de woning van Ferdinand Schlich op het eerste zicht ook lijkt, 
ze is het resultaat geweest van heel wat toegevingen die ingegeven werden docir het beperkte 
budget, de omgeving en de omwonenden. Dergelijke compromissen betekenen geen 
aantasting van de erfgoedwaarde maar getuigen juist van een gevoeligheid voor de context 
in de ruime betekenis van het woord, en dus van de architecturale waarde, 
BESLUIT: 
Artikel 1. Met toepassing van artikel 6.1.1 tot en met artikel 6.1.11 van het 
Onroerenderfgoeddecreet van 12 juli 2013 en artikel 6.2·.1 van het Onroerenderfgoedbesluit 
van 16 mei 2014 worden de volgende onroerende goederen definitief beschermd als 
monument: 
architectenwoning Ferdinand Schlich, Gérard Willemotlaan 85 in Gent (Mariakerke), bekend 
ten kadaster: Gent, 29ste afdeling, sectie A, perceelnummer 770M . 
De definitief beschermde onroerende goederen zijn aangeduid op het plan dat als bijlage bij 
dit besluit wordt gevoegd.
Het is verboden het dak van het onroerend erfgoed te schilderen in een paarse kleur.
Pagina 2 van 5 
De fotoregistratie van de fysieke toestand van de definitief beschermde goederen wordt als 
bijlage bij dit besluit gevoegd. 
Art. 2. Het monument heeft architecturale waarde. 
De erfgoedelementen en de erfgoedkenmerken van het monument zijn: 
De woning van Ferdinand Schlich is een vrijstaand langgerekt rechthoekig volume met de 
lange zijde evenwijdig aan de straat. In vergelijking met naburige woningen staat de woning 
minder diep op het perceel (een viertal meter) omwille van het ondiepe karakter en de vorm 
van dit laatste (versmallend naar achteren). Een gemengde haag (meidoorn -haagbeuk) aan 
de straatzijde zorgt voor beschutting. De woning telt één bouwlaag (twee aan de 
zuidoostelijke zijde voor het atelier) en heeft een lagere uitbouw (berging) die de noordelijke 
hoek omarmt. Alle daken zijn plat (uitkragend bij de berging) en bedekt met roofing en keien. 
De muren zijn spouwloos en opgetrokken in cellenbeton op een betonstenen plint. 
Binnenin bestaat de woning grotendeels uit één open rechthoekige ruimte van ruim 30 m 
lang op 6 m breed. Door een aantal centrale muren, dwars op de voor- en achtergevel, is 
deze ruimte verdeeld in vier zones vari verschillende breedte, van zuidoost naar noordwest: 
1. een dubbelhoog atelier met een houten mezzanine op een stalen draagbalk, die 
bereikbaar is via een heel sober vormgegeven houten steektrap; 
2. een zone die aan de voorzijde de inkomhal omvat met een WC en een ingemaakte kast 
achter een witte wand en aan de achterzijde een bureau; 
3. de living met een halfopen keuken; 
4. de nachtzone die een badkamer omvat (met aan weerzijden een gang en een toegang 
via een gewone deur) en twee slaapkamers. 
Deze zones kunnen volledig afgesloten worden door houten schuifdeuren, die langs de vooren achtergevel in enfilade geplaatst zijn en in de wanden schuiven. · 
Het plafond van het hoofdvolume wordt gevormd door licht hellende, gewapende 
betongewelven dwars op de voor- en achtergevel (bij het atelier evenwijdig ermee) die door 
houten latjes gescheiden zijn, en die in de inkomhal verborgen zijn achter een verlaagd 
plafond. De berging heeft een houten dakstructuur. De muren zijn bepleisterd en de vloer is 
uitgevoerd in gegoten beton (iedocrete) met een eenvoudige houten plint die aansluit bij het 
schrijnwerk. 
De voorgevel is vrij gesloten met uitzondering van de centrale dubbele voordeur en het 
monumentale ateliervenster aan de oostzijde. Dat atelier wordt verder verlicht door drie 
kleine, rechthoekige, excentrisch geplaatste vensters (één op de begane grond in de 
zuidoostelijke zijgevel en twee a~n weerszijden van de westelijke hoek van de mezzanine). 
De achtergevel heeft een smal venster ter hoogte van het bureau en vier brede gekoppelde 
vensters (twee aan de woonkamer, één met drieledig schrijnwerk en centrale deur aan de 
keuken en één ter hoogte van de badkamer en slaapkamer). Het meest linkse en rechtse 
venster zijn ook onderverdeeld met telkens één smal raam aan de zijkant. De noordwestelijke 
gevel heeft één dubbele raamdeur in de noordelijke slaapkamer, de berging een buitendeur 
in de twee korte buitengevels (zuidoostelijk en zuidwestelijk) en een binnendeur naar de · 
keuken. De badkamer wordt verlicht door een lichtkoepel. De gevelopeningen zijn heel 
eenvoudig uitgewerkt (zonder dorpel en onder betonnen lateien) en vrij diep ingevuld, met 
uitzondering van het atelierraam dat min of meer gelijk met de gevels komt. Alle 
gevelopeningen zijn ingevuld met typerend houten schrijnwerk (volgens de bouwplannen in 
te verven oregon kroon) en dubbel glas (thermopane). Het atelierraam kenmerkt zich door 
een vierkante, houten roedeverdeling, de voordeur en de deuren van de berging door een 
brede midden regel. Aan de achtergevel bevindt zich boven het smalle venster van het bureau 
een houten waterspuwer. Ook het geveldeel boven deze waterspuwer is bekleed met hout. 
In de tuin bevindt zich onder de mond van de waterspuwer een ronde put met waterafvoer. 
Pagina 3 van 5 
Art. 3. Voor het beschermde monument gelden de volgende beheersdoelstellingen: 
1 o de algemene doelstelling van de bescherming is het behoud van de erfgoedkenmerken 
en -elementen die de basis vormen voor de erfgoedwaarden. Elke aanpassing of nieuwe 
functie moet de beschermde erfgoedwaarde, -kenmerken en -elementen respecteren 
en ondersteunen. Bewaren gaat daarbij voor op vernieuwen. Dit veronderstelt in de 
eerste plaats vakkundig onderhoud en conserverende ingrepen. Indien restauratie of 
vervanging noodzakelijk blijkt, is het aangewezen de historische toestand te hernemen, 
indien nodig op basis van bouwhistorisch onderzoek; 
2° verder is het wenselijk: 
a) de gevelafwerking uit te voeren zoals bedoeld door Schlich. Hij voorzag een ruw 
aangebrachte (acryl)verf die het metselverband nog enigszins doorlaat. Voor de 
structuur en de kleur van de verf kan men zich baseren op de uitgevoerde proeven 
op de zuidwestelijke muur van de berging. Verder had de ontwerper de intentie om 
de gevels te laten begroeien met klimop en andere klimplanten, en maakte hij 
ontwerpen voor een zonnewering boven de grote vensters van de achtergevel; 
b) de tuinaanleg uit te voeren zoals bedoeld door Schlich. Hij ontwierp een rechthoekig 
terras aan de grote vensters van de achtergevel en een rond opvangbassin aan de 
mond van de waterspuwer waarvoor al een waterafvoer werd aangelegd. Eventueel 
kan ook gedacht worden aan uitvoering van de trapvormige muur met 
autostaanplaats aan de zuidoostelijke zijde van het perceel; . 
c) om bij de toekomstige inrichting van het interieur rekening te houden met de 
plannen die Schlich hiervoor maakte, met name het voorzien van verlaagde 
plafonds in de kleinere ruimtes en deels in de living en de keuken, en de inrichting 
van de keuken en de badkamer. 
Art. 4. De zakelijkrechthouder en de gebruiker van het beschermde monument zijn verplicht 
de instandhouding en het onderhoud ervan te verzekeren door: 
1° het goed als een goede huisvader te beheren en de nodige voorzorgsmaatregelen te 
nemen tegen schade ten gevolge van brand, blikseminslag, diefstal, vandalisme, wind 
of water; 
2° de toestand van het goed regelmatig te controleren; 
3° regulier onderhoud uit te oefenen; 
4° onmiddellijk passende consolidatie- en beveiligingsmaatregelen te nemen in geval van 
nood. 
Art. 5. Voor de volgende handelingen aan het beschermde monument moet een toelating 
worden aangevraagd: 
1° het plaatsen, slopen, verbouwen of heropbouwen van een constructie; 
2° het verwijderen, vervangen, wijzigen of verstevigen van constructieve elementen; 
3° het verwijderen, vervangen of wijzigen van historische materialen en het toepassen van 
behandelingen met als doel de historische materialen te reinigen, te herstellen, te 
verduurzamen of te beschermen tegen verweer en aantasting; 
4° het uitvoeren van de volgende werken aan het dak en de buitenmuren van constructies: 
a) het verwijderen, vervangen of wijzigingen van het dakvolume, de dakbedekking, 
de dakconstructie en gootconstructies; 
b) het verwijderen van voegen en het hervoegen; 
c) het aanbrengen, verwijderen, vervangen of wijzigen van de kleur, textuur of 
samenstelling van de afwerkingslagen; 
d) het aanbrengen, verwijderen, vervangen of wijzigen van buitenschrijnwerken, 
deuren, ramen, oculi, poorten, inclusief de beglazing, beslag, hang- en sluitwerk; 
e) het aanbrengen, verwijderen, vervangen of wijzigen van aa rd- en nagelvaste 
elementen, smeedijzer en beeldhouwwerk, inclusief nieuwe toevoegingen; 
f) het aanbrengen, vervangen of wijzigen van opschriften, publiciteitsinrichtingen of 
uithangborden, met uitzondering van verkiezingspubliciteit en met uitzondering van 
publiciteitsinrichtingen, waarbij wordt bekend gemaakt dat het goed te kqop of te 
Pagina 4 van 5
huur is, op voorwaarde dat de totale maximale oppervlakte niet meer bedraagt dan 
4m 2 ; 
5° het uitvoeren van de volgende omgevingswerken: 
a) het plaatsen of wijzigen van boven- en ondergrondse nutsvoorzieningen en 
leidingen; 
b) het plaatsen of wijzigen van afsluitingen; 
c) het aanleggen of wijzigen van verharding met een minimale gezamenlijke 
grondoppervlakte van 30 m2 of het uitbreiden van bestaande verhardingen met 
minimaal 30m2, met uitzondering van verhardingen geplaatst binnen de straal van 
30 m rond een vergund of een vergund geacht gebouw; 
d) het structureel en fundamenteel wijzigen van de tuinaanleg; 
6° het uitvoeren van de volgende handelingen aan of in het interieur: 
a) het uitvoeren van destructief materiaaltechnisch onderzoek; 
b) het uitvoeren van structurele werken en het toevoegen van nieuwe structuren; 
c) · het verwijderen, vervangen of wijzigen van historische materialen en het 
toepassen van behandelingen met als doel de historische materialen te reinigen, 
te herstellen, te verduurzamen of te beschermen tegen verweer en aantasting; 
d) het verwijderen, vervangen of wijzigen van plafonds, gewelven, vloeren, 
trappen, wandbekledingen, binnenschrijnwerk, inclusief de lambriseringen, 
beslag, hang- en sluitwerk, en van de waardevolle interieurdecoratie; 
e) het bepleisteren van niet-bepleisterde elementen of het bepleisteren met een 
andere samenstelling of textuur, alsook het ontpleisteren van bepleisterde 
elementen; 
f) het beschilderen van ongeschilderde elementen of het schilderen in andere 
kleuren of kleurschakeringen of met een andere verfsoort dan de aanwezige; 
g) het plaatsen of vernieuwen van technische voorzieningen, zoals verwarming, 
klimaatregeling, elektrische installatie, geluidsinstallatie, sanitair, liften .en 
beveiligingsinstallaties, met uitzondering van de installaties waarvoor · geen 
destructieve ingrepen moeten gebeuren en/of die geen storende visuele impact 
hebben op het waardevolle interieur. 
Er is geen toelating vereist voor het onmiddellijk nemen van passende consolidatie- en 
beveiligingsmaatregelen in geval van nood, noch voor de uitvoering van regulier onderhoud.  """)

    print(all_actions)