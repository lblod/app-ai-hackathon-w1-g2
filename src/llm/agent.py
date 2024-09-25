import csv
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.llm.output_models import output_parser
from src.llm.prompts import SYSTEM_PROMPT, USER_PROMPT

APP_DIR = Path(__file__).parents[2]
OUTPUT_DIR = APP_DIR / 'data' / 'ai_output'
CSV_HEADERS = ['TextFragment', 'Forbidden', 'PermitNeeded']

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
    actions = chain.invoke({"paper": paper})

    allowed_actions_data = []
    if actions.allowed_action_list:
        allowed_actions_data = [
            {'TextFragment': allowed_action.action, 'Forbidden': False, 'PermitNeeded': allowed_action.permit_needed}
            for allowed_action in actions.allowed_action_list
        ]

    not_allowed_actions_data = []
    if actions.not_allowed_action_list:
        not_allowed_actions_data = [
            {'TextFragment': not_allowed_action.action, 'Forbidden': True, 'PermitNeeded':  not_allowed_action.permit_needed}
            for not_allowed_action in actions.not_allowed_action_list
        ]
    # Combine both lists
    all_actions_data = allowed_actions_data + not_allowed_actions_data
    filtered_data = [item for item in all_actions_data if item['TextFragment'] is not None]

    csv_file = OUTPUT_DIR / 'actions_some_besluit.csv'
    write_output_csv(actions=filtered_data, output_path=csv_file)
    return all_actions_data


if __name__ == '__main__':
    all_actions = process_decision(paper=""""
~\''.\ Vlaa~se '~\2 \ Regenng 
Ministerieel besluit tot voorlopige bescherming als monument van 
Architectenwoning Louis Hagen in Gent (Sint-Amandsberg) 
DE VLAAMSE MINISTER VAN BUITENLANDS BELEID EN ONROEREND ERFGOED, 
Gelet op het Onroerenderfgoeddecreet van 12 JUli 2013, artikel 6.1.1; 
Gelet op het besluit van de Vlaamse Regenng van 25 JUli 2014 tot bepalmg van de 
bevoegdheden van de leden van de Vlaamse Regenng, artikel 6, 1 o; 
Gelet op de advJesvraag biJ het college van burgemeester en schepenen van Gent, mged1end 
op 23 november 2018; 
Overwegende dat het advJes n1et tiJdig 1s meegedeeld en dus geacht wordt gunstig te ZIJn; 
Gelet op het advJes van de departementen of agentschappen van de Vlaamse overheid, 
bevoegd voor ruimteliJke ordenmg, woonbeleid en onroerend erfgoed, leefmilieu, natuur en 
energ1e, mobJIJtelt en openbare werken, landbouw en vJssenJ, waarvan de behandeling 1s 
opgenomen m biJlage; 
Gelet op de advJesvraag biJ de Vlaamse CommJssJe Onroerend Erfgoed, mged1end op 23 
november 2018; 
Overwegende dat het advJes n1et tiJdig 1s meegedeeld en dus geacht wordt gunst1g te ZIJn; 
Overwegende dat het waarderend onderzoek, waarvan de resultaten ZIJn opgenomen 1n het 
beschermmgsdoss1er, de erfgoedwaarde van Architectenwoning Lou1s Hagen aantoont; 
Overwegende dat Arch1tectenwonmg Lou1s Hagen als monument architecturale waarde bez1t 
d1e als volgt wordt gemotiveerd: 
De e1gen wonmg van architect Lou1s Hagen (1974) vormt een synthese vah de 
ontwerppnnCJpes die de vroegste fase van ZIJn oeuvre kenmerken. D1t oeuvre bouwde Hagen 
u1t tussen 1970 en 1978, onder de vleugels van het Gentse, natJonaal gerenommeerde en 
Internationaal onderscheiden bureau BARO. Bmnen het naoorlogse architectuurlandschap m 
Gent vormen de brutalistische realisaties van BARO een belangn]ke, progressieve n1che d1e 
z1ch onderscheidde van het doorsnee bouwen van dat moment. De arch1tectenwonmg van 
Lou1s Hagen siUJt hierbiJ aan en getu1gt van een hoge herkenbaarheld en representatJvJteJt, 
zowel op vlak van het behoud van de matenalltelt als van het ongmele concept. 
Op het vlak van vorm streefde Hagen er m ZIJn e1gen won1ng naar om te voldoen aan diverse 
randvoorwaarden, zoals biJVoorbeeld de afstemmmg op de spec1fieke context, met aandacht 
voor pnvacy, onentat1e en perspectieven. Deze elementen hadden een Impact op de 
rUJmtewerkmg en de mterne schikking, die beide getUigen van een spel met contrasten en 
doorz1chten. Doorheen een rUimteliJk ontworpen wonmg met splitlevels ereeerde Hagen v1a 
een centrale trappenstructuur een architecturale wandeling. Hierdoor ontstonden diverse 
sferen en soorten ru1mtes. Het labynntachtige karakter van de wandeling doorheen de wonmg 
liet ook een 'gliJdende schaal van pnvacy' toe. D1t kwam n1et enkel tegemoet aan noden op 
het vlak van afscherming naar de buitenwereld, maar evenzeer aan vragen tot mdJvJduele 

pnvacy. Ook konden enkele ru1mtes flexibel aangepast en mgevuld worden 1n 
overeenstemming met de evoluerende gezmsnoden. 
De architectenwoning van Lou1s Hagen 1s representatief voor de typologie van de 
architectenwoning en de comb1nat1e van werken en wonen. De ontvangstruimte en het 
architectuuratelier op de laagste n1veaus illustreren dit. Hagen zette de typologie echter sterk 
naar ZIJn hand door geen rUimteliJke scheiding aan te brengen tussen de representatieve en 
persoonliJke vertrekken, en te spelen met open- en geslotenheid. 
Ook de matenalen en constructiemethode droegen biJ tot de ereatle van een optimaal woonen werkklimaat. Het ruwe, zichtbare gebruik van betonsteen 1n het exteneur werd door Hagen 
radJeaal doorgetrokken 1n het mteneur en gecombineerd met plafonds 1n ruw bekiste beton. 
De matenaalkeuze IS een vormeliJk statement bmnen de maatschappeliJke amb1t1es van 
Hagen om z1ch door middel van architectuur af te zetten tegen het matenalisme en 
kapitalisme van de toenmalige maatschappiJ. Daarnaast biedt het onafgewerkte karakter 
ervan mogeliJkheden tot persoonliJke inbreng en toe-e1genmg van de ruimtes door de 
bewoners. 
Alle ontwerpkeuzes leidden tot een hoge ensemblewaarde, meer bepaald een onlosmakeliJke 
verbmdmg tussen exteneur en 1nteneur. Het gave ensemble bewaart zowel de leesbare 
matenalen en constructie, de bmnenmdeling, afwerking en vaste mncht1ngen m de keuken 
en badkamers. Het weloverwogen tumontwerp van Chnst1an Vermander (Buro voor Vn]e 
Ruimten en Groenvoorz~enmg, later Buro voor Vn]e Ruimte) versterkte het geheel en 
mtegreerde de wonmg 1n de bUJtenaanleg. Het oorspronkeliJke tumontwerp nam de wens tot 
pnvacy en het spel met sferen en rUimteliJk afgebakende zones u1t het mteneur over. Zo bez1t 
het volledige ontwerp een hoge sculpturale kwaliteit en vormt het een un1ek en erg persoonliJk 
totaal kunstwerk. 
De arch1tectenwonmg 1s echter ook representatief voor ru1mere natJonale en mternat1onale 
ontwikkelingen m de architectuur van de late ]aren 1960 en ]aren 1970. Hagen en ZIJn 
collega's zagen- m navolgmg van het revolutieJaar 1968- m architectuur mogeliJkheden om 
een maatschappeliJk manifest te realiseren. D1t kon aangepast worden aan de noden van het 
gezmsleven, en nam afstand van trad1t1onele plattegronden en won1ngtypes. 
Zo leunt ze zowel m de vormeliJke als conceptuele keuzes nauw aan biJ het Nederlandse 
structuralisme van Aldo Van Eyck en Herman Hertzberger, en de ontwerpprinCipes van Lou1s 
Kahn. Illustratief hiervoor ZIJn de aandacht voor de menseliJke schaal en de persoonliJke 
inbreng van gebruikers en bewoners, gestimuleerd door de specifieke 1ndel1ng en Zichtbare 
matenalen. De ontwerpen vormen een metafoor van een kleme stad, met aandacht voor 
bmnenstraten, ru1mtes voor ontmoeting, voor persoonliJke ontw1kkelmg en voor beschuttmg. 
De complexe, fragmentansche rUimteliJkheid van de ontwerpen Visualiseert de contrasten die 
de architect wij verzoenen. De opvallende rUimteliJk structurerende constructie breekt met 
traditionele conventJes en legt de focus op het wonen zelf. Deze structuur laat bovendJen 
flexibiliteit toe op het vlak van gebruik en 1nvullmg. 
Hagens arch1tectenwomng kwam ook tot stand op het moment dat het Gentse brutalisme een 
hoogtepunt beleefde. Het ontwerp vormt een VISitekaartJe en modelproJect van de filosofie 
van BARO en van de ontwerpprinCipes die Hagen zelf neerschreef. De open ru1mtewerkmg en 
de zichtbare matenalen vertonen parallellen met het naoorlogse brutalisme van Hagens 
collega's en vnenden biJ BARO, Schaffrath en Raman, en tiJdgenoten als Juliaan Lampens en 
Marc Dessauvage, en verWIJzen eveneens naar pnnc1pes u1t het mternat1onale modern1sme,
BESLUIT: 
Artikel 1. Met toepassmg van artikel 6.1.1 tot en met artikel 6.1.11 van het 
Onroerenderfgoeddecreet van 12 JUli 2013 en artikel 6.2.1 van het Onroerenderfgoedbesluit 
van 16 me1 2014 worden de volgende onroerende goederen voorlopig beschermd als 
monument: 
Arch1tectenwonmg Lou1s Hagen met tum, Ni]VerheJdskaaJ 43 m Gent (Smt-Amandsberg), 
bekend ten kadaster: Gent, 19de afdeling, sect1e C, perceelnummer 1225Z. 

De voorlopig beschermde onroerende goederen ZIJn aangeduld op het plan dat als biJlage biJ 
d1t beslult wordt gevoegd. 
De fotoreg1strat1e van de fysieke toestand van de voorlopig beschermde goederen wordt als 
biJlage biJ d1t beslult gevoegd. 
Art. 2. Het monument heeft architecturale waarde. 
De erfgoedelementen en de erfgoedkenmerken van het monument ZIJn: 
Inplantmg en tuinaanleg 
De architectenwoning ligt 1n een verkaveling ten zuldoosten van de kern van SintAmandsberg, aan de N1]Verhe1dskaa1. Deze straat IS enkel aan de noordziJde bebouwd. Ten 
zu1den wordt ze afgeliJnd door de Schelde. 
De mplant1ng van Hagens wonmg vertrok vanu1t de aandacht voor pnvacy van de bewoners. 
De groenaanleg schermt de won1ng af van de straat en mtegreert de architectuur m de 
omnngende natuur. Het ongmele tumontwerp door landschapsarch1tect Chnst1an Vermander 
1s op z1ch bewaard, maar de oorspronkeliJke structuur IS mmder herkenbaar. Het ontwerp 
speelde aanvankeliJk sterk m op het grondplan van de wonmg. De verharde opnt tot de 
garage IS Uitgewerkt met een baJonetvormige asverschu1v1ng, waarop tegeliJk een smal en 
vnJliggend verhard Inkompad naar de voordeur 1n de westgevel le1dt. Deze padenstructuur 1n 
betonklmkers 1s bewaard. 
De voortumru1mte bewaart referentles aan het oorspronkeliJke ontwerp met compacte, mm 
of meer rechthoekige tuinkamers, afgescheiden door gesloten heesterwanden en enkele 
verspreide opgaande bomen. De haagbeukenhagen d1e de tumkamers begrensden, resteren. 
momenteel enkel nog aan de ZIJde van de opnt en de straat. Ter hoogte van de wonmg slUit 
een verhard 'blnnenplemt]e' aan met 'verzonken z1trU1mte' en een hoekJe aansluitend biJ een 
ronde betonnen waterbak. De licht verdiepte zithoek 1s heden bewaard 1n de vorm van een 
vlerkante VIJVer. De tuinaanleg staat 1n d1aloog met een verhoogd terras boven de garage. 
D1t verhard terras verdeelde z1ch m een 'eetkamer' 1n open lucht en een 'zonneterras', 
Ingekleed met plantenbak. De afwatenng voert met een dru1pkett1ng af 1n de geliJkvloerse 
waterbak. De tumkamers werden dooraderd door een speels tracé van stapstenen Uit 
hergebruikt gran1et. 
De ondiepe achtertuinruimte met beperkte terremmodellenng IS losser vormgegeven. Ook 
deze tumru1mte, deels opgevat als bloemenweide, deels als gesloten heesterwand, met 
enkele opgaande bomen 1s dooraderd door een speels tracé van stapstenen dat verbmd1ng 
maakt met de 'mkom' en de 'verzonken z1tru1mte'. 
In de tum resteren momenteel nog een beperkt aantal beplantingen van de oorspronkeliJke 
aanleg, waaronder enkele klimplanten als Wilde wmgerd en kamperfoelie. De architectuur 
mtegreert z1ch sterk m de bu1tenru1mte door de aanwez1ghe1d van deze planten. Het was 
1mmers de wens van de architect om door m1ddel van de begroe11ng van de wonmg de breuk 
tussen de natuur en de architecturale Ingreep te verzachten. In de struiklaag ZIJn biJVOorbeeld 
de krentenboompJes bewaard. 
Exteneur 
De wonmg IS opgevat als een kubusvormig volume onder een plat dak. De bultenarchitectuur 
ont- en verhult op subtiele WIJZe de 1nwend1ge structuur op bas1s van splltlevels, d1e aan de 
straatziJde (zu1d) twee bouwlagen met verspnngende n1veaus voowet en achteraan (noord) 
dne n1veaus. De westgevel wordt verlevendigd door m- en Uitsprongen van het volume. De 
zuidZIJde wordt op straatniveau u1tgebre1d met een volume van één bouwlaag, dat d1enst doet 
als garage (garagepoort ten zu1den) of als overdekte bu1tenru1mte (schuifraam m de 
oostziJde). Daarboven 1s een u1tbouw met terras voowen, deels gesitueerd onder een lu1fel, 
gevormd door een u1tkragmg van het dak. 
De geslotenheld van de architectuur wordt versterkt door het matenaalgebru1k. Het parement 
bestaat u1t ZIChtbare betonstenen. Tegen de oostziJde van de garage ZIJn een betonnen 

waterspuwer en Cilindervormige waterput voorzien. Een metalen kettmg leidt het regenwater 
af tot m de waterput. U1tspnngende muurtJes 1n betonsteen biJ de garage en het 
bovenliggende terras verhogen eveneens de sculpturaliteit van het geheel. 
De aanwezige muuropenmgen stemmen overeen met de planmdeling1 de onentat1e en de 
verzoening tussen afschermmg en contact. De noord- en westgevel ZIJn grotendeels gesloten 
u1tgewerkt1 maar ook de vensteropeningen van de andere twee gevels ZIJn weloverwogen 
aangebracht 1n relatle tot de bu1tenru1mte. De rechthoekige vensters spnngen licht terug ten 
opzichte van het parement 1n betonsteen en bewaren quas1 volledig hun oorspronkeliJk 
houten schn]nwerk. 
De zuidgevel IS het sterkst opengewerkt. De bovenverdieping wordt ter hoogte van het terras 
verlicht door een groot schuifraam/ dat eveneens de toegang tot het terras vormt. Ernaast1 
ten oosten ervan1 IS de gevel volledig opengewerkt met een venster dat de ontvangstruimte 
en bovenliggende Zithoek verlicht en doorloopt over de hoek met de oostgevel. De oostgevel 
wordt centraal doorbroken door een vert1caal 1 gevelhoog venster1 dat schuin afloopt 
bovenaan tot het dak. De noordoosteliJke ZIJde van deze gevel IS voorz1en van een 
hooggeplaatst venster ter hoogte van de slaapkamer en van twee kle1nere1 dieperliggende 
hoekvensters. De noordgevel wordt behalve door de hoekvensters verlicht door twee 
asymmetnsch 1n de gevel geplaatste vensters. Het gesloten karakter van de noordgevel wordt 
verdergezet 1n de uitbouw van de westgevel. Een hoekvenster verlicht de keuken en stroken 
met glasdallen ZIJn voorz1en ter hoogte van het tollet en de douchekamer. 
De toegang 1s verdiept gesitueerd m de westgevel. De oorspronkeliJke houten deur met een 
honzontale beplanking IS bewaard en wordt lmks geflankeerd door een ZIJlicht. In de 
zu1dgevel 1 rechts naast de Uitbouw met garage1 IS eveneens een toegangsdeur voorz1en1 1n 
d1t geval een beglaasde deur met bovenlicht. 
De combmat1e van de opengewerkte bovenverdieping met aansluitend terras aan de zuidkant 
van de wonmg speelt volledig mop het panorama. Toch wordt 1nk1Jk vermeden. Het terras 1s 
ommuurd en ten zu1den voorzien van een eveneens ommuurde 'groenbuffer'1 geflankeerd 
door een 'wmdbeschutte zone'. Aan de westZIJde van het terras bevindt z1ch een mgemaakte 
kast1 Ingepast 1n een verticale Uitbouw 1n betonsteen 1n de westgevel. 
Inteneur 
Planmdel1ng en algemene kenmerken: 
De planmdeling en mteneurafwerkmg kunnen n1et losgekoppeld worden van het exteneur. 
Hagen trok 1n het mteneur het brutal1st1sche karakter door en liet de betonstenen wanden en 
constructleve elementen 1n ruw Zichtbeton of 'béton brut' overal ZIChtbaar. De specifieke 
constructiemethode leidde tot een complex en weloverwogen ontwerp waarbiJ alles op 
voorhand gepland diende te worden en le1dmgen ge1ntegreerd en verborgen werden. De 
verlichtingsarmaturen werden mgepast 1n daarvoor voorz1ene1 Cirkelvormige u1tspanngen 1n 
de betonnen plafonds. 
Achter de gesloten façade gaat een dynamische rUimtewerking schuil volgens een open plan. 
De bewoners en gebrulkers kunnen het gebouw stelselmatig ontdekken1 vanu1t de donkere 
benedenverdiepingen tot de lichte leefruimtes op de bovenverdiepingen. De lichtmval wordt 
bepaald door de opengewerkte zuidgevel en een gevelhoog venster en v1de 1n de oostgevel. 
Zen1tale verlichting 1s voorz1en v1a een lichtkoepel in de badkamer. De ru1mtes ZIJn gesitueerd 
op meerdere spl1tlevels1 wat zorgt voor een ruimteliJke complex1te1t rond de centrale traphal. 
De bordestrap ontvouwt z1ch rondom een verticaal structurerend1 sculpturaal element/ waann 
het gebruik van betonsteen wordt verdergezet. De trap en de piJlers 1n betonsteen d1e deze 
flankeren/ spelen met openheid en geslotenheid. De opengewerkte trap voorz1et eveneens 
vn]e doorgangen tot de n1veaus d1e erop aansluiten. Ook tussen de n1veaus onderling wordt 
gespeeld met v1suele relat1es en de grens tussen afschermmg/pnvacy en openheid/contact. 
Weloverwogen contact met de bu1tenru1mte maakt het ensemble compleet. 
De aandacht van Hagen voor het wonen en het gezmsleven leidde tot het verzachten van de 
brute matenalen door de vloeren van verschillende ru1mtes en de betonnen trap met tapiJt te 
bekleden. Deze aandacht zorgde er ook voor dat de sfeer en bestemmmg van de ru1mtes 
bepalend was voor hun s1tuenng1 aankleding en hoogte. De 1nt1emere of funct1onelere ru1mtes 

werden aan de achterZIJde (noord) gesitueerd, wat daar leidde tot dne lagere n1veaus. De 
representatieve leefru1mtes, gesitueerd 1n twee hogere n1veaus aan de straatziJde (zu1d), 
voorzagen telkens nog een niveauverschil, wat de dynam1ek van de ru1mtewerkmg 
verhoogde. 
Benedenverdiepingen: 
De toegang 1n de westgevel leidt Vla een open tochtportaal met Ingewerkte mat, tot de hal 
(n1veau 0). In de noordwand van het portaal 1s een u1tspanng aanwezig, waartussen een 
bewaarde afscherming van de verwarming en een legplank ZIJn voorzien. 
De ru1me, open hal IS voorz1en van een vloer 1n spliJttegels 1n rood aardewerk en b1edt ook 
aan de zuidZIJde een toegang tot de tu1n. In de zuidwesteliJke hoek IS een tollet gesitueerd, 
evenals een toegang tot de garage. Deze paneeldeuren ZIJn ongmeel en op de houten liJsten 
na voorz1en van een blauwe afwerking. De deuren ten noordwesten van de hal d1e toegang 
geven tot een douchekamer en stookplaats, ZIJn geliJkaardig Uitgewerkt. In het tollet en de 
douchekamer wordt de betegelde vloer van de hal doorgetrokken. De douchekamer bewaart 
eveneens het lavabomeubel 1n zwarte formica met twee lavabo's, voorzien van een zwarte 
afwerking en geplaatst tegen de westwand. Ook bewaart de noordeliJke doucheruimte met 
z1tbad de ongmele betegeling met blauwe mozaleksteentJes. 
De hal 1s met een betonstenen muur afgesloten van de twee treden lager gelegen 
ontvangstruimte (n1veau -1). De lage muur zorgt wel voor een open verbinding tussen de 
ru1mtes. De betegelde vloer van de hal wordt doorgetrokken tot de trap en de vloer van de 
ontvangstruimte. Een lage betonstenen muur schermt de noordziJde van deze ru1mte af, maar 
opent deze terzelfder tiJd naar de achterliggende v1de en het laagste n1veau. 
Enkele treden, eveneens afgewerkt met de spliJttegels, geven toegang tot het laagste n1veau 
aan de noordZIJde van de wonmg (n1veau -2). D1t laagste n1veau 1s voorz1en van een vloer 
met functionele, keramische tegels. Het had geen vastgelegde bestemmmg, kon worden 
aangepast aan de noden van het gezm en deed vanaf 1978 d1enst als tekenatelier. VlakbiJ de 
treden bevmdt z1ch een bewaarde deur met een blauwe afwerking, d1e le1dt tot de krUipkei der. 
Ten oosten 1s een smalle ru1mte voorz~en 1n de v1de, d1e 1n een open verb1nd1ng staat met de 
hoger gelegen ontvangstruimte en verlicht wordt door het gevelhoge venster 1n de oostgevel. 
Bovenverdiepingen: 
Vanuit de hal kunnen gebrulkers en bezoekers ook het parcours naar boven volgen. De 
bordestrap 1s vanaf daar bekleed met tapiJt en leidt 1n eerste mstant1e naar een 1nt1eme ru1mte 
aan de noordZiJde (n1veau 1). Het lage, relatief donkere karakter van de ru1mte wordt 
versterkt door de beperkte muuropeningen en de vloer, d1e met tapiJt 1s afgewerkt. Ten 
noordwesten IS ru1mte voor 'b1b en stud1e' voorz1en en ten noordwesten een '1nt1eme Zithoek'. 
De lichtinval wordt grotendeels bepaald door het spel met open- en geslotenheid van de v1de 
ten zu1den en de doorzichten tot de trap. De Zithoek 1s enkel voorz1en van een subtiele 
afslu1t1ng 1n de vorm van een lage betonstenen muur. Ten zulden 1s de z1thoek opengewerkt 
tot de v1de en de bovenliggende leefruimte. Voor de v1de IS er een haardensemble voorz1en, 
opgebouwd u1t betonnen elementen, die de geometnsche, sculpturale opbouw van de 
architectuur verderzetten. Het tablet ten oosten IS afgedekt met tegels 1n aardewerk, en wordt 
ten westen ervan geflankeerd door een verdiepte zone met de aslade, afgeliJnd aan de 
voorZIJde met baksteen. De haard zelf combineert een betonnen balkvormig volume met dne 
c11indervorm1ge verluchtlngspupen aan de voorziJde en een zichtbare, Cilindervormige schouw 
tot het dak. 
De trap leidt vervolgens naar de leefruimtes aan de zuidZIJde. In eerste mstant1e IS dit de 
open Zithoek (mveau 2). Deze IS n1et alleen ten zu1den en zuidoosten geopend naar de 
omgeving. Ze staat ook ten noorden 1n verbinding met de v1de, de haard, de lager gelegen 
Zithoek en het bovenliggende n1veau met het nachtgedeelte. Ook het gevelhoge venster 1n 
de oostgevel ter hoogte van de v1de ereeert lichtmval. Het hoge plafond, het sculpturale spel 
met betonstenen wanden en piJlers, versterkt biJkomend het ru1mtegevoel. 
Met tapiJt beklede treden le1den vervolgens tot de eethoek en open keuken aan de 
zuidwestZIJde (n1veau 3), d1e ten zu1den 1n verb1nd1ng staat met het terras. Deze ru1mtes ZIJn 

net als de benedenverdieping voorz1en van een vloer m spliJttegels. De volled1ge 
keukenmnchtmg m form1ca 1s ongmeel en voorz~en van een bar aan de ZIJde van de eethoek. 
Het keukenmeubilair werd net als de badkamermeubels gerealiseerd door W1lfra Keukens 
(Meulebeke). De kasten en werkbladen spelen met een contrast tussen de zwarte hoofdkleur 
en w1tte accenten. De architect koos hiervoor, aangez1en w1t een te dominante kleur zou ZIJn 
In de woonsfeer. Ook de wandafwerking met donkergnJze moza1eksteent]es IS bewaard. 
Het nachtgedeelte met badkamer en slaapkamer, dat z1ch op het hoogste n1veau aan de 
noordziJde bevmdt (n1veau 4). De bad- en slaapkamer staan m een open verbmdmg met 
elkaar en ZIJn voorz1en van een vloer m tapiJt. De badkamer (noordwest) bewaart de blauwe 
moza1ekbetegelmg van het bad en de wanden, evenals het donkere lavabomeubel en de 
kasten die een scheiding vormen tot de 'alkoof'. Een Vlerkante open1ng m het plafond, d1e het 
beton zichtbaar toont en afgesloten IS met een koepel, verlicht de badkamer. De slaapms 
(noordoost) knjgt licht v1a een venster m de oostwand en vanu1t het mwend1ge doorzicht ten 
zu1den. 
Art. 3. Voor het beschermde monument gelden de volgende beheersdoelstellmgen: 
1° de algemene doelstelling van de bescherming 1s het behoud van de erfgoedkenmerken 
en -elementen die de bas1s vormen voor de erfgoedwaarde; 
2° Architectenwoning Lou1s Hagen vormt een totaalconcept met een belangnJke relatle 
tussen het architectuurontwerp en de aanleg van de bu1tenru1mte. Het pand getu1gt van 
een onlosmakeliJke samenhang tussen exteneur, inplantmg en inteneur. Elke 
beheersdaad vraagt om een ge1ntegreerde en duurzame aanpak waarbiJ de 1mpact op 
de volledige s1te met al z'n componenten wordt afgewogen. Ingrepen d1enen de 
beschermde erfgoedkenmerken en -elementen te respecteren en te ondersteunen, en 
mogen de draagkracht van de beschermde s1te n1et overschriJden. D1t veronderstelt 
vakkundig onderhoud en md1en nodig conserverende mgrepen; 
3° met betrekking tot het exteneur van Arch1tectenwon1ng Lou1s Hagen beoogt de 
bescherming het behoud van het oorspronkeliJke bouwvolume qua schaal, 
gevelopbouw, afwerking, matenaalgebruik en schnjnwerk, d1e bepalend ZIJn voor de 
architecturale e1genhe1d en herkenbaarheid van het ontwerp. Ind1en behoud en herstel 
met meer mogeliJk 1s, d1ent het schnJnwerk vervangen te worden naar ong1neel model 
met respect voor het matenaal en de geledmgen van het ong1nele houten schnJnwerk; 
4° · met betrekking tot het 1nteneur beoogt de bescherming het behoud van de planindeling, 
de open ru1mtewerkmg, de v1des, de kenmerkende matenalen en afwerking van de 
muren, vloeren en de plafonds, binnenschnJnwerk, en de bewaarde vaste mnchting van 
de badkamers, keuken en zithoek met haard. Uiterst bepalend 1s de geledmg van de 
ru1mte met splitlevels, afgescheiden door lage muurtJes en m een open verbmdmg met 
de centrale trappenpartiJ en aanwezige v1des; 
5° het beeldbepalende, Zichtbare karakter van de matenalen (beton(steen)) d1ent steeds 
behouden te bliJVen en versterkt de samenhang tussen mteneur en exteneur. Enkel m 
de twee kamers aan de noordZiJde van het laagste n1veau, waar dit matenaal alm 1978 
werd geschilderd, IS er een beperktere v1suele 1mpact op het geheel en kan h1er VriJer 
mee worden omgegaan; 
6° de recentere aanpassing van het dak, het n1euwe dakvolume en de draaltrap tegen de 
westgevel maken geen deel u1t van het oorspronkelijke ontwerp. Toekomstig behoud IS 
dus n1et vere1st en een terugkeer naar de oorspronkeliJke toestand IS steeds mogeliJk. 
Aangezien de toevoegingen n1et mgnJpen op de matene vormen ze wel revers1 bele 
Ingrepen; 
7° de bescherming van het volledige perceel met mbegnp van de tu1n veronderstelt een 
respectvolle omgang met het bomenbestand en de aanwezige aanplantingen. Het 
vere1st ook het behoud van de weloverwegen aanleg, voor zover bewaard. Het IS 
wenseliJk dat de tumaanleg In de toekomst zoveel mogeliJk wordt hersteld 1n de geest 
van het oorspronkeliJke ontwerpplan, dat getu1gt van een grote samenhang en dialoog 
met de architectuur en binnenruimtes. 

Art. 4. De zakeliJkrechthouder en de gebru1ker van het beschermde monument ZIJn verplicht 
de Instandhouding en het onderhoud ervan te verzekeren door: 
1° het goed als een goede hulsvader te beheren en de nod1ge voorzorgsmaatregelen te 
nemen tegen schade ten gevolge van brand, bl1ksemmslag, diefstal, vandalisme, wmd 
of water; 
2° de toestand van het goed regelmatig te controleren; 
3° regulier onderhoud Uit te oefenen; 
4° onmiddelliJk passende consol1dat1e- en beve11ig1ngsmaatregelen te nemen m geval van 
nood. 
Art. 5. Voor de volgende handelingen aan het beschermde monument moet een toelatmg 
worden aangevraagd: 
1° het plaatsen, slopen, verbouwen of heropbouwen van een constructie; 
2° het verwiJderen, vervangen, WIJZigen of verstevigen van constructleve elementen; 
3° het verWIJderen, vervangen of WIJZigen van h1stonsche matenalen en het toepassen van 
behandelingen met als doel de h1stonsche matenalen te re1n1gen, te herstellen, te 
verduurzamen of te beschermen tegen verweer en aantastmg; 
4° het Uitvoeren van de volgende werken aan het dak en de buitenmuren van constructies: 
a) het verwiJderen, vervangen of WIJZigen van dakbedekking en gootconstruct1es; 
b) het verwiJderen van voegen en het hervoegen; 
c) het aanbrengen, verWIJderen, vervangen of WIJZigen van de kleur, textuur of 
samenstelling van de afwerkmgslagen; 
d) het aanbrengen, verWIJderen, vervangen of WIJZigen van buitenschn]nwerken, 
deuren, ramen, luiken, poorten, mclus1ef de al dan met figuratieve beglazmg, 
claustra, beslag, hang- en sluitwerk; 
e) het aanbrengen, verWIJderen, vervangen of WIJZigen van aard- en nagelvaste 
elementen, smeediJZer en beeldhouwwerk, mclus1ef n1euwe toevoegingen; 
f) het aanbrengen, vervangen of WIJZigen van opschnften, public1te1tsmncht1ngen of 
Uithangborden, met u1tzondenng van verk1ezmgspubi!Cite1t en met u1tzondenng van 
publie~te1tsmncht1ngen, waarbiJ wordt bekendgemaakt dat het goed te koop of te 
huur 1s, op voorwaarde dat de totale max1male oppervlakte met meer bedraagt dan 
4 m2 ; 
5° het Uitvoeren van de volgende omgev1ngswerken: 
a) het plaatsen of WIJZigen van bovengrondse nutsvoorz1enmgen en leidingen; 
b) het plaatsen of WIJZigen van afslu1tmgen, met u1tzondenng van gladde schnkdraad 
en pnkkeldraad ten behoeve van veekenng; 
c) het aanleggen, structureel en fundamenteel WIJZigen of verWIJderen van wegen en 
paden; 
d) het vellen of beschadigen van bomen en struiken d1e opgenomen ZIJn 1n het 
beschermmgsbeslu1t of 1n een goedgekeurd beheersplan, en elke handeling d1e een 
WIJZigmg van de groeiplaats en groe1vorm van de bomen en de struiken d1e 
opgenomen ZIJn m het beschermmgsbeslu1t of m een goedgekeurd beheersplan tot 
gevolg kan hebben; 
e) het aanleggen of WIJZigen van verhardmg met een mm1male gezamenliJke 
grondoppervlakte van 30 m2 of het u1tbre1den van bestaande verhardingen met 
m1n1maal 30 m2 , met u1tzondenng van verhardmgen geplaatst binnen een straal 
van 30 m rond een vergund of een vergund geacht gebouw; 
f) het aanleggen van sport- en spelinfrastructuur of parkeerplaatsen; 
g) het structureel en fundamenteel WIJZigen van de aanleg van de tum; 
6° het Uitvoeren van de volgende handelingen aan of 1n het 1nteneur: 
a) het Uitvoeren van destructief matenaaltechnisch onderzoek; 
b) het Uitvoeren van structurele werken en het toevoegen van meuwe structuren; 
c) het verWIJderen, vervangen of WIJZigen van h1stonsche matenalen en het toepassen 
van behandelingen met als doel de h1stonsche matenalen te rem1gen, te herstellen, 
te verduurzamen of te beschermen tegen verweer en aantastmg; 

d) het verwijderen, vervangen of wijzigen van plafonds, gewelven, vloeren, trappen, 
binnenschrijnwerken, inclusief de al dan niet figuratieve beglazing, lambrisering, 
beslag, hang- en sluitwerk, en van de waardevolle interieurdecoratie; 
e) het bepleisteren van niet-bepleisterde elementen of het bepleisteren met een 
andere samenstelling of textuur, alsook het ontpleisteren van bepleisterde 
elementen; 
f) het beschilderen van ongeschilderde elementen of het schilderen in andere kleuren 
of kleurschakeringen of met een andere verfsoort dan de aanwezige; 
g) het plaatsen of vernieuwen van technische voorzieningen zoals verwarming, 
klimaatregeling, elektrische installatie, geluidsinstallatie, sanitair, liften en 
beveiligingsinstallaties, met uitzondering van die installaties waarvoor geen 
destructieve ingrepen moeten gebeuren en/of die geen storende visuele impact 
hebben op de erfgoedelementen en -kenmerken. 
Er is geen toelating vereist voor het onmiddellijk nemen van passende consolidatie- en 
beveiligingsmaatregelen in geval van nood, noch voor de uitvoering van regulier onderhoud. 
Brussel, 2 1 FEB. 2019 · 
De Vlaamse minister van Buitenlands Beleid en Onroerend Erfgoed, 
Geert BOURGEOIS """)

    print(all_actions)