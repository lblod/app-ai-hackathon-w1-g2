from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from src.llm.output_models import output_parser
from src.llm.prompts import SYSTEM_PROMPT

LLM = ChatOllama(model="llama3.1", temperature=0, base_url="http://hackathon-ai-2.s.redhost.be:11434")


def process_decision(paper: str):
    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT,
            ),
            ("human", "Haal op basis van de systeeminstructies de acties uit dit erfgoeddocument: {paper}. "
                      "Retourneer het resultaat als een JSON-object, volgens dit voorbeeld {format_instructions}."),
        ]
    ).partial(format_instructions=output_parser.get_format_instructions())
    chain = prompt_template | LLM | output_parser
    actions = chain.invoke({"paper": paper})
    for action in actions:
        print(action)


process_decision(paper=""""
Voor het beschermde monument gelden de volgende beheersdoelstellingen: 
de algemene doelstelling van de beschermmg 1s het behoud van de erfgoedkenmerken 
en -elementen die de bas1s vormen voor de erfgoedwaarde; 
Architectenwoning Daemers getuigt van een totaalconcept en IS een ensemble, 
gekenmerkt door een dialoog en een grote homogen1te1t tussen 1nteneur en exteneur. 
Elke beheersdaad vraagt om een gemtegreerde en duurzame aanpak waarbij de Impact 
op de volledige s1te met al z'n componenten wordt afgewogen. Ingrepen dienen de 
beschermde erfgoedkenmerken en -elementen te respecteren en te ondersteunen, en 
mogen de draagkracht van de beschermde s1te n1et overschn]den. Dit veronderstelt 
vakkundig onderhoud en 1nd1en nodig conserverende mgrepen; 
met betrekking tot het exteneur beoogt de beschermmg het behoud van de 
bUltenarchitectuur qua schaal, volumewerkmg, matenaalgebrUik, afwerking en 
schn]nwerk. Bepalend voor de herkenbaarheid IS het behoud van het contrast tussen 
de Witgeschilderde bakstenen gevels en het centrale, c11indervorm1ge torenvolume m 
zichtbaar metselwerk, evenals de typische sch1kkmg van de volumes en hun 
geometnsche, strakke karakter, die de Interne planmdeling veruitwendigt; 
met betrekking tot het mteneur beoogt de beschermmg het behoud van de globale 
planmdeling en ru1mtewerkmg met verspnngende n1veaus, waarbij het dag- en 
nachtgedeelte log1sch ZIJn geschikt rondom de centrale, verhoogde zithoek m het 
cilindervormige volume, en het leefgedeelte bepaald wordt door een open plan. In de 
afwerkmg, vormgeving en het matenaalgebruik van het daggedeelte (inkom, leefruimte 
en keuken) dient rekenmg gehouden te worden met de oorspronkeliJke toestand, d1e 
gedeelteliJk bewaard 1s. Beeldbepalend ziJn de typische vloeren en hun behandelmg, en 
de afwerking van muren en plafonds. In het geval van mgrepen d1ent de samenhang 
tussen mteneur en exteneur qua afwerking en matenaalgebruik gerespecteerd te 
worden. Het nachtgedeelte (slaapkamers en badkamer) laat flexibiliteit en 
aanpassmgen toe op het vlak van aankleding en sluit ook de samenvoeging van 
somm1ge kamers niet u1t; 
de bescherming beoogt eveneens het behoud van het vaste meubilair m het atelier, 
ontworpen door de architect. 
de beschermmg van het volledige perceel veronderstelt het behoud van de buitenaanleg 
van paden, terrassen en muurtjes, met mbegnp van hun typische matenaalgebru1k. 
De zakeliJkrechthouder en de gebruiker van het beschermde monument ZIJn verplicht 
de mstandhoudmg en het onderhoud ervan te verzekeren door: 
het goed als een goede hulsvader te beheren en de nod1ge voorzorgsmaatregelen te 
nemen tegen schade ten gevolge van brand, bl1ksemmslag, diefstal, vandalisme, wmd 
of water; 
de toestand van het goed regelmatig te controleren; 
regulier onderhoud u1t te oefenen; 
onmiddelliJk passende consolidatie- en beve11ig1ngsmaatregelen te nemen 1n geval van 
nood. 

Voor de volgende handelmgen aan het beschermde monument moet een toelatmg 
worden aangevraagd: 
het plaatsen, slopen, verbouwen of heropbouwen van een construct1e; 
het verWIJderen, vervangen, WIJZigen of verstevigen van constructleve elementen; 

het verWJJderen1 vervangen of WIJZigen van h1stonsche matenalen en het toepassen van 
behandelmgen met als doel de histonsche matenalen te re1mgen1 te herstellen1 te 
verduurzamen of te beschermen tegen verweer en aantasting; 
het Uitvoeren van de volgende werken aan het dak en de buitenmuren van constructies: 
het verwijderen1 vervangen of WIJZigen van dakbedekking en gootconstructJes; 
het verwiJderen van voegen en het hervoegen; 
het aanbrengen1 verWIJderen/ vervangen of WIJZigen van de kleur/ textuur of 
samenstelling van de afwerkmgslagen; 
het aanbrengen1 verWJJderen1 vervangen of WIJZigen van buJtenschnjnwerken1 
deuren1 ramen1 poorten1 mclus1ef de beglazmg1 beslag1 hang- en sluitwerk; 
het aanbrengen1 verWJJderen1 vervangen of wiJZigen van aard- en nagelvaste 
elementen1 smeediJZer en beeldhouwwerk1 mclusJef n1euwe toevoegmgen; 
het aanbrengen1 vervangen of WIJZigen van opschnften1 publicJteJtsmnchtmgen of 
uJthangborden1 met u1tzondenng van verkJezJngspublicJteJt en met uJtzondenng van 
publiCJteitsinnchtmgen1 waarbiJ wordt bekendgemaakt dat het goed te koop of te 
huur JS1 op voorwaarde dat de totale max1male oppervlakte n1et meer bedraagt dan 
4 m2 ; 
het Uitvoeren van de volgende omgevingswerken: 
het plaatsen of WIJZigen van bovengrondse nutsvoorz1enmgen en leidingen; 
het plaatsen of WIJZigen van afslu1tmgen; 
het aanleggen1 structureel en fundamenteel WIJZigen of verWIJderen van wegen en 
paden; ' 
het aanleggen of WIJZigen van verhardmg met een mm1male gezamenliJke 
grondoppervlakte van 30 m2 of het uJtbreJden van bestaande verhardingen met 
mm1maal 30 m2 1 met u1tzondenng van verhardingen geplaatst bmnen een straal 
van 30 m rond een vergund of een vergund geacht gebouw; 
het uitvoeren van graafwerken d1e de stabliJtelt van de gebouwen en constructJes 
m gevaar kunnen brengen; 
het uitvoeren van de volgende handelmgen aan of m het mteneur: 
het Uitvoeren van destructief matenaaltechnisch onderzoek; 
het uitvoeren van structurele werken en het toevoegen van nieuwe structuren; 
het uitvoeren van werken die het uJtzJcht of de mdelmg van het mteneur WIJZigen; 
het verWJJderen1 vervangen of wijzigen van historische materialen en het toepassen 
van behandelmgen met als doel de h1stonsche matenalen te rem1gen1 te herstellen/ 
te verduurzamen of te beschermen tegen verweer en aantasting; 
het verWJJderen1 vervangen of WIJZigen van plafonds/ vloeren1 trappen1 
bmnenschriJnwerk1 mclus1ef de beglazmg1 beslag1 hang- en sluitwerk/ en van vast 
meub11a1r; 
het bepleisteren van niet-bepleisterde elementen of het bepleisteren met een 
andere samenstelling of textuur1 alsook het ontple1steren van bepleisterde 
elementen; 
het beschilderen van ongesch1lderde elementen of het schilderen m andere kleuren 
of kleurschakenngen of met een andere verfsoort dan de aanwezige; 
""")
