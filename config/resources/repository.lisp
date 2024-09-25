(in-package :mu-cl-resources)

(add-prefix "ext" "http://mu.semte.ch/vocabularies/ext/")
(add-prefix "tmp" "http://mu.semte.ch/vocabularies/tmp/")

(add-prefix "besluit" "http://data.vlaanderen.be/ns/besluit#")
(add-prefix "mandaat" "http://data.vlaanderen.be/ns/mandaat#")
(add-prefix "persoon" "http://data.vlaanderen.be/ns/persoon#")
(add-prefix "generiek" "http://data.vlaanderen.be/ns/generiek#")
(add-prefix "mobiliteit" "https://data.vlaanderen.be/ns/mobiliteit#")

(add-prefix "eli" "http://data.europa.eu/eli/ontology#")
(add-prefix "m8g" "http://data.europa.eu/m8g/")
(add-prefix "dct" "http://purl.org/dc/terms/")
(add-prefix "cpsv" "http://purl.org/vocab/cpsv#")
(add-prefix "dul" "http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#")
(add-prefix "adms" "http://www.w3.org/ns/adms#")
(add-prefix "person" "http://www.w3.org/ns/person#")
(add-prefix "org" "http://www.w3.org/ns/org#")
(add-prefix "prov" "http://www.w3.org/ns/prov#")
(add-prefix "regorg" "https://www.w3.org/ns/regorg#")
(add-prefix "skos" "http://www.w3.org/2004/02/skos/core#")
(add-prefix "foaf" "http://xmlns.com/foaf/0.1/")
(add-prefix "nao" "http://www.semanticdesktop.org/ontologies/2007/08/15/nao#")
(add-prefix "pav" "http://purl.org/pav/")
(add-prefix "schema" "http://schema.org/")
(add-prefix "rdfs" "http://www.w3.org/2000/01/rdf-schema#")

(add-prefix "nfo" "http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#")
(add-prefix "nie" "http://www.semanticdesktop.org/ontologies/2007/01/19/nie#")
(add-prefix "dbpedia" "http://dbpedia.org/ontology/")

(add-prefix "sign" "http://mu.semte.ch/vocabularies/ext/signing/")
(add-prefix "lblodlg" "http://data.lblod.info/vocabularies/leidinggevenden/")
(add-prefix "lblodmow" "http://data.lblod.info/vocabularies/mobiliteit/")
(add-prefix "locn" "http://www.w3.org/ns/locn#")
(add-prefix "adres" "https://data.vlaanderen.be/ns/adres#")
(add-prefix "lblodlg" "http://data.lblod.info/vocabularies/leidinggevenden/")
(add-prefix "dct" "http://purl.org/dc/terms/")
(add-prefix "adms" "http://www.w3.org/ns/adms#")
(add-prefix "task" "http://redpencil.data.gift/vocabularies/tasks/")
(add-prefix "cogs" "http://vocab.deri.ie/cogs#")
(add-prefix "oe" "https://inventaris.onroerenderfgoed.be/")
(add-prefix "oent" "https://id.erfgoed.net/vocab/ontology#")
;;;;
;; NOTE
;; docker-compose stop; docker-compose rm; docker-compose up
;; after altering this file.


;;;;
;; Describe the prefixes which you'll use in the domain file here.
;; This is a short-form which allows you to write, for example,
;; (s-url "http://purl.org/dc/terms/title")
;; as (s-prefix "dct:title")

;; (add-prefix "dct" "http://purl.org/dc/terms/")


;;;;;
;; The following is the commented out version of those used in the
;; commented out domain.lisp.

;; (add-prefix "dcat" "http://www.w3.org/ns/dcat#")
;; (add-prefix "dct" "http://purl.org/dc/terms/")
;; (add-prefix "skos" "http://www.w3.org/2004/02/skos/core#")


;;;;;
;; You can use the ext: prefix when you're still searching for
;; the right predicates during development.  This should *not* be
;; used to publish any data under.  It's merely a prefix of which
;; the mu.semte.ch organisation indicates that it will not be used
;; by them and that it shouldn't be used for permanent URIs.

(add-prefix "ext" "http://mu.semte.ch/vocabularies/ext/")
