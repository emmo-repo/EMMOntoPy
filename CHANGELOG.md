# Changelog

## [v0.3.1](https://github.com/emmo-repo/EMMO-python/tree/v0.3.1) (2022-05-08)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.3.0...v0.3.1)

**Merged pull requests:**

- Fixed typo in ontoconvert [\#409](https://github.com/emmo-repo/EMMO-python/pull/409) ([jesper-friis](https://github.com/jesper-friis))

## [v0.3.0](https://github.com/emmo-repo/EMMO-python/tree/v0.3.0) (2022-05-05)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.2.0...v0.3.0)

**Fixed bugs:**

- Documentation is currently not building [\#407](https://github.com/emmo-repo/EMMO-python/issues/407)
- Pytest is currently failing [\#384](https://github.com/emmo-repo/EMMO-python/issues/384)
- permission denied when working with temporary file [\#313](https://github.com/emmo-repo/EMMO-python/issues/313)

**Closed issues:**

- Make get\_descendants\(levels=1\) [\#403](https://github.com/emmo-repo/EMMO-python/issues/403)
- Add functionality for setting name part of IRI to prefLabel [\#398](https://github.com/emmo-repo/EMMO-python/issues/398)
- Generate excelsheet from ontology. [\#394](https://github.com/emmo-repo/EMMO-python/issues/394)
- Return a list of the concepts that are disregarded during when converting from excel with -force argument [\#393](https://github.com/emmo-repo/EMMO-python/issues/393)
- Demo - Broken ontology URLs [\#390](https://github.com/emmo-repo/EMMO-python/issues/390)
- Excelparser: how to handle entities that already exist in one of the imported ontologies? [\#334](https://github.com/emmo-repo/EMMO-python/issues/334)

**Merged pull requests:**

- Updated docs python handler [\#408](https://github.com/emmo-repo/EMMO-python/pull/408) ([CasperWA](https://github.com/CasperWA))
- Flb/get descendants [\#405](https://github.com/emmo-repo/EMMO-python/pull/405) ([francescalb](https://github.com/francescalb))
- Corrected expected number of returned arguments [\#404](https://github.com/emmo-repo/EMMO-python/pull/404) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#402](https://github.com/emmo-repo/EMMO-python/pull/402) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#400](https://github.com/emmo-repo/EMMO-python/pull/400) ([TEAM4-0](https://github.com/TEAM4-0))
- Add functionality for setting name part of IRI to prefLabel [\#399](https://github.com/emmo-repo/EMMO-python/pull/399) ([jesper-friis](https://github.com/jesper-friis))
- create\_from\_excel/pandas return as list of concepts that are worngly defined in the excelfile [\#396](https://github.com/emmo-repo/EMMO-python/pull/396) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#395](https://github.com/emmo-repo/EMMO-python/pull/395) ([TEAM4-0](https://github.com/TEAM4-0))
- Download EMMO from raw.github deirectly as redirection is broken [\#392](https://github.com/emmo-repo/EMMO-python/pull/392) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#389](https://github.com/emmo-repo/EMMO-python/pull/389) ([TEAM4-0](https://github.com/TEAM4-0))
- Workaround for failing test [\#385](https://github.com/emmo-repo/EMMO-python/pull/385) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#380](https://github.com/emmo-repo/EMMO-python/pull/380) ([TEAM4-0](https://github.com/TEAM4-0))
- fix \#313 remove handle [\#315](https://github.com/emmo-repo/EMMO-python/pull/315) ([sygout](https://github.com/sygout))

## [v0.2.0](https://github.com/emmo-repo/EMMO-python/tree/v0.2.0) (2022-03-02)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.1.3...v0.2.0)

**Implemented enhancements:**

- spaces before or after word in prefLabel makes excelparser fail [\#332](https://github.com/emmo-repo/EMMO-python/issues/332)
- Make EMMOntopy PyPi [\#268](https://github.com/emmo-repo/EMMO-python/issues/268)
- Use `pre-commit` [\#243](https://github.com/emmo-repo/EMMO-python/issues/243)
- Standard dunder/magic methods for `Ontology` [\#228](https://github.com/emmo-repo/EMMO-python/issues/228)
- Update code styling and linting [\#223](https://github.com/emmo-repo/EMMO-python/issues/223)
- Fix checking PR body & improve error message in CD [\#318](https://github.com/emmo-repo/EMMO-python/pull/318) ([CasperWA](https://github.com/CasperWA))
- New workflows for dependabot automation [\#285](https://github.com/emmo-repo/EMMO-python/pull/285) ([CasperWA](https://github.com/CasperWA))

**Fixed bugs:**

- GH GraphQL type issue for auto-merge workflow [\#374](https://github.com/emmo-repo/EMMO-python/issues/374)
- Missing warning for excel parser relations and problem with "nan" [\#365](https://github.com/emmo-repo/EMMO-python/issues/365)
- Ignore NumPy `safety` warning [\#360](https://github.com/emmo-repo/EMMO-python/issues/360)
- Seting metadata in excelparser fails if there are no imported ontologies. [\#331](https://github.com/emmo-repo/EMMO-python/issues/331)
- Edge-case fails CD workflow for dependabot [\#319](https://github.com/emmo-repo/EMMO-python/issues/319)
- Ontodoc failing due to wrong `rdflib` import [\#306](https://github.com/emmo-repo/EMMO-python/issues/306)
- Overwriting `get_triples()` method [\#280](https://github.com/emmo-repo/EMMO-python/issues/280)
- OpenModel logo not loading in README [\#278](https://github.com/emmo-repo/EMMO-python/issues/278)

**Closed issues:**

- Add NumPy as an explicit dependency [\#359](https://github.com/emmo-repo/EMMO-python/issues/359)
- Use TEAM 4.0\[bot\] for GH Actions jobs [\#352](https://github.com/emmo-repo/EMMO-python/issues/352)
- \_get\_triples\_spo take argumens s, and p, not subject and predicate [\#350](https://github.com/emmo-repo/EMMO-python/issues/350)
- Add --force to excelparser [\#333](https://github.com/emmo-repo/EMMO-python/issues/333)
- Cannot load ontology in Windows. [\#328](https://github.com/emmo-repo/EMMO-python/issues/328)
- make get\_ontology accept 'PosixPath' [\#326](https://github.com/emmo-repo/EMMO-python/issues/326)
- Make EMMOntoPy baseexception and basewarning [\#321](https://github.com/emmo-repo/EMMO-python/issues/321)
- get\_by\_label crash  if not str [\#311](https://github.com/emmo-repo/EMMO-python/issues/311)
- make excel parser that creates and ontology from a filled excel file [\#302](https://github.com/emmo-repo/EMMO-python/issues/302)
- Check out how to get version of ontology [\#299](https://github.com/emmo-repo/EMMO-python/issues/299)
- Let ontology.new\_entity acccept one or more parents directly [\#294](https://github.com/emmo-repo/EMMO-python/issues/294)
- Make ManchesterSyntaxParser that returns Owlready2 [\#293](https://github.com/emmo-repo/EMMO-python/issues/293)
- onto.new\_entity should throw Error if label name consists of more than one word [\#290](https://github.com/emmo-repo/EMMO-python/issues/290)
- Add logo to README [\#287](https://github.com/emmo-repo/EMMO-python/issues/287)
- Write EMMO-python is deprecated and link to EMMOtopy on PyPi [\#269](https://github.com/emmo-repo/EMMO-python/issues/269)

**Merged pull requests:**

- \[Auto-generated\] Update dependencies [\#378](https://github.com/emmo-repo/EMMO-python/pull/378) ([TEAM4-0](https://github.com/TEAM4-0))
- Use `ID!` type instead of `String!` [\#375](https://github.com/emmo-repo/EMMO-python/pull/375) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#371](https://github.com/emmo-repo/EMMO-python/pull/371) ([TEAM4-0](https://github.com/TEAM4-0))
- Avoided infinite recursion when loading catalog files that recursively [\#370](https://github.com/emmo-repo/EMMO-python/pull/370) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#367](https://github.com/emmo-repo/EMMO-python/pull/367) ([TEAM4-0](https://github.com/TEAM4-0))
- Warning relation excelparser [\#366](https://github.com/emmo-repo/EMMO-python/pull/366) ([sygout](https://github.com/sygout))
- Close temporary file before reading it [\#364](https://github.com/emmo-repo/EMMO-python/pull/364) ([jesper-friis](https://github.com/jesper-friis))
- Ignore safety ID 44715 + add numpy dependency [\#361](https://github.com/emmo-repo/EMMO-python/pull/361) ([CasperWA](https://github.com/CasperWA))
- \[Auto-generated\] Update dependencies [\#358](https://github.com/emmo-repo/EMMO-python/pull/358) ([TEAM4-0](https://github.com/TEAM4-0))
- \[Auto-generated\] Update dependencies [\#357](https://github.com/emmo-repo/EMMO-python/pull/357) ([TEAM4-0](https://github.com/TEAM4-0))
- Use TEAM 4.0\[bot\] [\#353](https://github.com/emmo-repo/EMMO-python/pull/353) ([CasperWA](https://github.com/CasperWA))
- Changed arguments in \_has\_obj\_triples\_spo [\#351](https://github.com/emmo-repo/EMMO-python/pull/351) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#349](https://github.com/emmo-repo/EMMO-python/pull/349) ([francescalb](https://github.com/francescalb))
- Fix serialised ontology iri [\#341](https://github.com/emmo-repo/EMMO-python/pull/341) ([jesper-friis](https://github.com/jesper-friis))
- Corrected parsing cardinality restrictions [\#340](https://github.com/emmo-repo/EMMO-python/pull/340) ([jesper-friis](https://github.com/jesper-friis))
- When visualising restrictions, annotate the edges with the restriction type by default [\#339](https://github.com/emmo-repo/EMMO-python/pull/339) ([jesper-friis](https://github.com/jesper-friis))
- \[Auto-generated\] Update dependencies [\#338](https://github.com/emmo-repo/EMMO-python/pull/338) ([francescalb](https://github.com/francescalb))
- Flb/update excel parser accroding to thermodynamics example [\#336](https://github.com/emmo-repo/EMMO-python/pull/336) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#330](https://github.com/emmo-repo/EMMO-python/pull/330) ([francescalb](https://github.com/francescalb))
- Added sconverting Posix to str in get\_ontology [\#327](https://github.com/emmo-repo/EMMO-python/pull/327) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#324](https://github.com/emmo-repo/EMMO-python/pull/324) ([francescalb](https://github.com/francescalb))
- Added package specific base exception and base warning for EMMOntoPy [\#322](https://github.com/emmo-repo/EMMO-python/pull/322) ([francescalb](https://github.com/francescalb))
- Added checking that label is string in get\_by\_label [\#312](https://github.com/emmo-repo/EMMO-python/pull/312) ([francescalb](https://github.com/francescalb))
- Make excelparser that converts a filled excel sheet to an ontology [\#309](https://github.com/emmo-repo/EMMO-python/pull/309) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#308](https://github.com/emmo-repo/EMMO-python/pull/308) ([francescalb](https://github.com/francescalb))
- Fix ontoconvert rdflib import [\#307](https://github.com/emmo-repo/EMMO-python/pull/307) ([CasperWA](https://github.com/CasperWA))
- Check first versionIRI then versionInfo in ontology.get\_version\(\) [\#301](https://github.com/emmo-repo/EMMO-python/pull/301) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#300](https://github.com/emmo-repo/EMMO-python/pull/300) ([francescalb](https://github.com/francescalb))
- Removed .readthedocs.yml [\#298](https://github.com/emmo-repo/EMMO-python/pull/298) ([jesper-friis](https://github.com/jesper-friis))
- Added support for evaluating Manchester expression to owlready2 [\#296](https://github.com/emmo-repo/EMMO-python/pull/296) ([jesper-friis](https://github.com/jesper-friis))
- Added functionality for more than one parent in new\_entity [\#295](https://github.com/emmo-repo/EMMO-python/pull/295) ([francescalb](https://github.com/francescalb))
- \[Auto-generated\] Update dependencies [\#292](https://github.com/emmo-repo/EMMO-python/pull/292) ([francescalb](https://github.com/francescalb))
- Added test for label name length in ontology.new\_entity [\#291](https://github.com/emmo-repo/EMMO-python/pull/291) ([francescalb](https://github.com/francescalb))
- add logo to Readme and doc [\#289](https://github.com/emmo-repo/EMMO-python/pull/289) ([m-abdollahi](https://github.com/m-abdollahi))
- Improved representation of blank nodes [\#283](https://github.com/emmo-repo/EMMO-python/pull/283) ([jesper-friis](https://github.com/jesper-friis))
- Update method name to avoid overwriting inherited [\#281](https://github.com/emmo-repo/EMMO-python/pull/281) ([CasperWA](https://github.com/CasperWA))
- Fixed link to OpenModel logo [\#279](https://github.com/emmo-repo/EMMO-python/pull/279) ([francescalb](https://github.com/francescalb))
- Skip FOAF test [\#277](https://github.com/emmo-repo/EMMO-python/pull/277) ([CasperWA](https://github.com/CasperWA))
- Added Standard methods to Ontology [\#246](https://github.com/emmo-repo/EMMO-python/pull/246) ([francescalb](https://github.com/francescalb))
- Implement `pre-commit` & various tools [\#245](https://github.com/emmo-repo/EMMO-python/pull/245) ([CasperWA](https://github.com/CasperWA))

## [v0.1.3](https://github.com/emmo-repo/EMMO-python/tree/v0.1.3) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.1.2...v0.1.3)

## [v0.1.2](https://github.com/emmo-repo/EMMO-python/tree/v0.1.2) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.1.1...v0.1.2)

## [v0.1.1](https://github.com/emmo-repo/EMMO-python/tree/v0.1.1) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/emmo-repo/EMMO-python/tree/v0.1.0) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.1b...v0.1.0)

**Implemented enhancements:**

- "Warning" Importing from `collections` [\#236](https://github.com/emmo-repo/EMMO-python/issues/236)

**Fixed bugs:**

- Loading ontologies that do not import skos fails [\#261](https://github.com/emmo-repo/EMMO-python/issues/261)
- Fix documentation build warnings [\#250](https://github.com/emmo-repo/EMMO-python/issues/250)
- Fix images in documentation [\#233](https://github.com/emmo-repo/EMMO-python/issues/233)
- Circular reference from Owlready2 [\#210](https://github.com/emmo-repo/EMMO-python/issues/210)

**Closed issues:**

- Write up transfer from EMMOpython to EMMOntoPy i README.md [\#267](https://github.com/emmo-repo/EMMO-python/issues/267)
- Add test to emmocheck for upcoming EMMO [\#257](https://github.com/emmo-repo/EMMO-python/issues/257)
- Add packaging as dependency in requirements [\#255](https://github.com/emmo-repo/EMMO-python/issues/255)
- Add CI check for building documentation [\#244](https://github.com/emmo-repo/EMMO-python/issues/244)
- Add OpenModel as contributing project [\#237](https://github.com/emmo-repo/EMMO-python/issues/237)
- Update public documentation to new framework [\#234](https://github.com/emmo-repo/EMMO-python/issues/234)
- Automate documentation releases [\#232](https://github.com/emmo-repo/EMMO-python/issues/232)
- Update name of EMMO to Elemental Multiperspective Material Ontology [\#230](https://github.com/emmo-repo/EMMO-python/issues/230)
- Tidy up unittests [\#220](https://github.com/emmo-repo/EMMO-python/issues/220)
- Remove importability of sub-`factpluspluswrapper` folders [\#213](https://github.com/emmo-repo/EMMO-python/issues/213)
- Make function that automatically loads emmo [\#209](https://github.com/emmo-repo/EMMO-python/issues/209)
- Require rdflib\>5.0.0? [\#206](https://github.com/emmo-repo/EMMO-python/issues/206)
- change package name [\#205](https://github.com/emmo-repo/EMMO-python/issues/205)
- test\_catalog fails because seraching for .owl in emmo/master [\#203](https://github.com/emmo-repo/EMMO-python/issues/203)
- Consider using `mike` for versioned documentation [\#197](https://github.com/emmo-repo/EMMO-python/issues/197)
- Add a test that checks that loading of non-EMMO based ontologies work - e.g. do not require skos:prefLabel [\#196](https://github.com/emmo-repo/EMMO-python/issues/196)
- Setup Materials for MkDocs framework [\#195](https://github.com/emmo-repo/EMMO-python/issues/195)
- Clean up demo, examples and docs [\#193](https://github.com/emmo-repo/EMMO-python/issues/193)
- Formalize review process with checklists [\#190](https://github.com/emmo-repo/EMMO-python/issues/190)
- funksjon ontology.add\_class\(label, parent\)  [\#183](https://github.com/emmo-repo/EMMO-python/issues/183)

**Merged pull requests:**

- Reset version to 0.1.0 [\#271](https://github.com/emmo-repo/EMMO-python/pull/271) ([CasperWA](https://github.com/CasperWA))
- Update README with PyPI and deprecation msgs [\#270](https://github.com/emmo-repo/EMMO-python/pull/270) ([CasperWA](https://github.com/CasperWA))
- Added option: EMMObased = False in ontology.load\(\) [\#262](https://github.com/emmo-repo/EMMO-python/pull/262) ([francescalb](https://github.com/francescalb))
- Update pyyaml requirement from \<6,\>=5.4.1 to \>=5.4.1,\<7 [\#260](https://github.com/emmo-repo/EMMO-python/pull/260) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update owlready2 requirement from !=0.32,!=0.34,\<0.35,\>=0.28 to \>=0.28,!=0.32,!=0.34,\<0.36 [\#259](https://github.com/emmo-repo/EMMO-python/pull/259) ([dependabot[bot]](https://github.com/apps/dependabot))
- Added new test "test\_physical\_quantity\_dimension" [\#258](https://github.com/emmo-repo/EMMO-python/pull/258) ([jesper-friis](https://github.com/jesper-friis))
- Add `packaging` to list of requirements [\#256](https://github.com/emmo-repo/EMMO-python/pull/256) ([CasperWA](https://github.com/CasperWA))
- Fix MkDocs build warnings and CI job [\#254](https://github.com/emmo-repo/EMMO-python/pull/254) ([CasperWA](https://github.com/CasperWA))
- Update mkdocstrings requirement from ~=0.16.1 to ~=0.16.2 [\#253](https://github.com/emmo-repo/EMMO-python/pull/253) ([dependabot[bot]](https://github.com/apps/dependabot))
- Update dependencies [\#252](https://github.com/emmo-repo/EMMO-python/pull/252) ([CasperWA](https://github.com/CasperWA))
- Add OpenModel contributing project [\#247](https://github.com/emmo-repo/EMMO-python/pull/247) ([francescalb](https://github.com/francescalb))
- Automate documentation releases [\#242](https://github.com/emmo-repo/EMMO-python/pull/242) ([CasperWA](https://github.com/CasperWA))
- Import from `collections.abc` when possible [\#240](https://github.com/emmo-repo/EMMO-python/pull/240) ([CasperWA](https://github.com/CasperWA))
- Ensure all produced files from tests are in a temp dir [\#239](https://github.com/emmo-repo/EMMO-python/pull/239) ([CasperWA](https://github.com/CasperWA))
- Changed EMMO to be acronym for Elemental Multiperspective Material Ontology [\#238](https://github.com/emmo-repo/EMMO-python/pull/238) ([francescalb](https://github.com/francescalb))
- Use width in img HTML [\#235](https://github.com/emmo-repo/EMMO-python/pull/235) ([CasperWA](https://github.com/CasperWA))
- Update graphviz requirement from \<0.17,\>=0.16 to \>=0.16,\<0.18 [\#229](https://github.com/emmo-repo/EMMO-python/pull/229) ([dependabot[bot]](https://github.com/apps/dependabot))
- Added function to load the emmo \(the ontology\) directly [\#226](https://github.com/emmo-repo/EMMO-python/pull/226) ([francescalb](https://github.com/francescalb))
- Created pull request template [\#225](https://github.com/emmo-repo/EMMO-python/pull/225) ([francescalb](https://github.com/francescalb))
- Setup new documentation framework [\#222](https://github.com/emmo-repo/EMMO-python/pull/222) ([CasperWA](https://github.com/CasperWA))
- Remove `__init__.py` files for FaCT++ wrapper \(again\) [\#221](https://github.com/emmo-repo/EMMO-python/pull/221) ([CasperWA](https://github.com/CasperWA))
- Unskip test as \#210 has been resolved [\#218](https://github.com/emmo-repo/EMMO-python/pull/218) ([CasperWA](https://github.com/CasperWA))
- Remove sub-fact++ modules importability [\#217](https://github.com/emmo-repo/EMMO-python/pull/217) ([CasperWA](https://github.com/CasperWA))
- Update requirements [\#216](https://github.com/emmo-repo/EMMO-python/pull/216) ([CasperWA](https://github.com/CasperWA))
- Avoid using Owlready2 v0.34 [\#211](https://github.com/emmo-repo/EMMO-python/pull/211) ([CasperWA](https://github.com/CasperWA))
- Update package names [\#208](https://github.com/emmo-repo/EMMO-python/pull/208) ([CasperWA](https://github.com/CasperWA))
- Added function new\_entitiy to ontology [\#207](https://github.com/emmo-repo/EMMO-python/pull/207) ([francescalb](https://github.com/francescalb))
- ttl standard for emmo [\#204](https://github.com/emmo-repo/EMMO-python/pull/204) ([francescalb](https://github.com/francescalb))
- Added choice for specifying namespace in get\_by\_label [\#202](https://github.com/emmo-repo/EMMO-python/pull/202) ([francescalb](https://github.com/francescalb))

## [v1.0.1b](https://github.com/emmo-repo/EMMO-python/tree/v1.0.1b) (2021-07-01)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.1...v1.0.1b)

**Closed issues:**

- Correct updating of catalog in ontology.load [\#188](https://github.com/emmo-repo/EMMO-python/issues/188)

**Merged pull requests:**

- Update version to 1.0.1 [\#189](https://github.com/emmo-repo/EMMO-python/pull/189) ([francescalb](https://github.com/francescalb))

## [v1.0.1](https://github.com/emmo-repo/EMMO-python/tree/v1.0.1) (2021-07-01)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0...v1.0.1)

**Implemented enhancements:**

- Specify version ranges for dependencies [\#155](https://github.com/emmo-repo/EMMO-python/issues/155)

**Fixed bugs:**

- Windows paths are not handled properly [\#147](https://github.com/emmo-repo/EMMO-python/issues/147)

**Closed issues:**

- Failing tests when lodaing battinfo [\#185](https://github.com/emmo-repo/EMMO-python/issues/185)
- Fix dependatbot to 'wider' [\#182](https://github.com/emmo-repo/EMMO-python/issues/182)
- Change to get\_label instead of asstring in ontograph, emmodoc, ontodoc, be careful [\#158](https://github.com/emmo-repo/EMMO-python/issues/158)
- licence does not work with metadata [\#157](https://github.com/emmo-repo/EMMO-python/issues/157)
- ontograph with several roots fails [\#153](https://github.com/emmo-repo/EMMO-python/issues/153)
- fix redudant getlabel, get\_preferred\_label, get\_label [\#152](https://github.com/emmo-repo/EMMO-python/issues/152)
- add --no-catalog and default as in emmocheck for ontograph [\#150](https://github.com/emmo-repo/EMMO-python/issues/150)
- make tests for checking upgrade of Owlready2 [\#137](https://github.com/emmo-repo/EMMO-python/issues/137)
- Add periodic\_table to examples [\#130](https://github.com/emmo-repo/EMMO-python/issues/130)
- Add support for simple property-based ontology annotations like dcterms:license [\#129](https://github.com/emmo-repo/EMMO-python/issues/129)
- Update documentation of tools re reasoner [\#123](https://github.com/emmo-repo/EMMO-python/issues/123)
- Ontograph: Include multiple parents/inheritance [\#86](https://github.com/emmo-repo/EMMO-python/issues/86)

**Merged pull requests:**

- Fixed updating of catalog in load [\#187](https://github.com/emmo-repo/EMMO-python/pull/187) ([francescalb](https://github.com/francescalb))
- Temporarily commented out loading ontologies with error in redirecting link on emmo.info [\#186](https://github.com/emmo-repo/EMMO-python/pull/186) ([francescalb](https://github.com/francescalb))
- Changed dependabot to widen [\#181](https://github.com/emmo-repo/EMMO-python/pull/181) ([francescalb](https://github.com/francescalb))
- Changed requirements to greater than [\#179](https://github.com/emmo-repo/EMMO-python/pull/179) ([francescalb](https://github.com/francescalb))
- Owread2-0.32 not accepted die to error in owlready2 triplelite [\#178](https://github.com/emmo-repo/EMMO-python/pull/178) ([francescalb](https://github.com/francescalb))
- Fixed import of defaultstyle in ontograph-tool [\#177](https://github.com/emmo-repo/EMMO-python/pull/177) ([francescalb](https://github.com/francescalb))
- Update pyyaml requirement from ~=5.4.0 to ~=5.4.1 [\#171](https://github.com/emmo-repo/EMMO-python/pull/171) ([dependabot[bot]](https://github.com/apps/dependabot))
- Updated pygments req to at least 2.7.4 because of high seq alert [\#168](https://github.com/emmo-repo/EMMO-python/pull/168) ([francescalb](https://github.com/francescalb))
- Owlready requirement \>0.28 [\#167](https://github.com/emmo-repo/EMMO-python/pull/167) ([francescalb](https://github.com/francescalb))
- Bump actions/setup-python from 2 to 2.2.2 [\#166](https://github.com/emmo-repo/EMMO-python/pull/166) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump actions/checkout from 2 to 2.3.4 [\#165](https://github.com/emmo-repo/EMMO-python/pull/165) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump owlready2 from 0.30 to 0.31 [\#164](https://github.com/emmo-repo/EMMO-python/pull/164) ([dependabot[bot]](https://github.com/apps/dependabot))
- WIP: Ipycytoscape [\#163](https://github.com/emmo-repo/EMMO-python/pull/163) ([francescalb](https://github.com/francescalb))
- Made it possible to load other ontologies like foaf [\#162](https://github.com/emmo-repo/EMMO-python/pull/162) ([jesper-friis](https://github.com/jesper-friis))
- Added get\_label instead of asstring [\#160](https://github.com/emmo-repo/EMMO-python/pull/160) ([francescalb](https://github.com/francescalb))
- Added write\_catalog\(\) [\#159](https://github.com/emmo-repo/EMMO-python/pull/159) ([jesper-friis](https://github.com/jesper-friis))
- Periodic table example [\#156](https://github.com/emmo-repo/EMMO-python/pull/156) ([francescalb](https://github.com/francescalb))
- Make one get label [\#154](https://github.com/emmo-repo/EMMO-python/pull/154) ([francescalb](https://github.com/francescalb))
- Issue150 ontograph cannotload emmo inferred directly [\#151](https://github.com/emmo-repo/EMMO-python/pull/151) ([francescalb](https://github.com/francescalb))
- Added Fact++ in tools documentation [\#149](https://github.com/emmo-repo/EMMO-python/pull/149) ([francescalb](https://github.com/francescalb))
- Bump owlready2 from 0.29 to 0.30 [\#148](https://github.com/emmo-repo/EMMO-python/pull/148) ([dependabot[bot]](https://github.com/apps/dependabot))
- Improved issue reporting in emmocheck [\#146](https://github.com/emmo-repo/EMMO-python/pull/146) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0) (2021-03-25)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-30...v1.0.0)

**Closed issues:**

- Use rdflib in Ontology.save\(\) to support more file formats [\#143](https://github.com/emmo-repo/EMMO-python/issues/143)
- Tool for publishing domain ontologies [\#140](https://github.com/emmo-repo/EMMO-python/issues/140)

**Merged pull requests:**

- Save to turtle and ontology annotations \(via the metadata attribute\) [\#144](https://github.com/emmo-repo/EMMO-python/pull/144) ([jesper-friis](https://github.com/jesper-friis))
- Corrected configuration of exceptions for test\_class\_label test. [\#142](https://github.com/emmo-repo/EMMO-python/pull/142) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-30](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-30) (2021-03-18)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-29...v1.0.0-alpha-30)

**Merged pull requests:**

- Load ontology [\#141](https://github.com/emmo-repo/EMMO-python/pull/141) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-29](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-29) (2021-03-16)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-28...v1.0.0-alpha-29)

**Implemented enhancements:**

- Add Wu&Palmer measure [\#134](https://github.com/emmo-repo/EMMO-python/issues/134)

**Closed issues:**

- Convert-imported update in utils [\#138](https://github.com/emmo-repo/EMMO-python/issues/138)

**Merged pull requests:**

- Fixed reading xml as 'rdfxml' [\#139](https://github.com/emmo-repo/EMMO-python/pull/139) ([francescalb](https://github.com/francescalb))
- Bump owlready2 from 0.28 to 0.29 [\#136](https://github.com/emmo-repo/EMMO-python/pull/136) ([dependabot[bot]](https://github.com/apps/dependabot))
- Added wu\_palmer\_measure for semantic similarity [\#135](https://github.com/emmo-repo/EMMO-python/pull/135) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-28](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-28) (2021-03-09)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-27...v1.0.0-alpha-28)

**Closed issues:**

- Also use the catalog file to map web URLs, not only local files. [\#109](https://github.com/emmo-repo/EMMO-python/issues/109)
- Check Error with Owlready2-0.26 [\#81](https://github.com/emmo-repo/EMMO-python/issues/81)

**Merged pull requests:**

- Version updated for rel of v0.28 [\#133](https://github.com/emmo-repo/EMMO-python/pull/133) ([francescalb](https://github.com/francescalb))
- Bump owlready2 from 0.27 to 0.28 [\#132](https://github.com/emmo-repo/EMMO-python/pull/132) ([dependabot[bot]](https://github.com/apps/dependabot))
- Load ontology [\#131](https://github.com/emmo-repo/EMMO-python/pull/131) ([jesper-friis](https://github.com/jesper-friis))
- Optimised label lookup in ontology and dir listing. It is now much faster [\#127](https://github.com/emmo-repo/EMMO-python/pull/127) ([jesper-friis](https://github.com/jesper-friis))
- Use catalog by default [\#126](https://github.com/emmo-repo/EMMO-python/pull/126) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-27](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-27) (2021-02-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-26...v1.0.0-alpha-27)

**Merged pull requests:**

- Ontodoc [\#125](https://github.com/emmo-repo/EMMO-python/pull/125) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-26](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-26) (2021-02-26)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-25...v1.0.0-alpha-26)

**Closed issues:**

- Make fact++ reasoner available and default in tools [\#122](https://github.com/emmo-repo/EMMO-python/issues/122)
- Use PyPI token in publish workflow [\#118](https://github.com/emmo-repo/EMMO-python/issues/118)
- Update publish workflow [\#115](https://github.com/emmo-repo/EMMO-python/issues/115)
- do something [\#108](https://github.com/emmo-repo/EMMO-python/issues/108)

**Merged pull requests:**

- Added functionality to document domain ontologies [\#124](https://github.com/emmo-repo/EMMO-python/pull/124) ([jesper-friis](https://github.com/jesper-friis))
- Bump owlready2 from 0.25 to 0.27 [\#121](https://github.com/emmo-repo/EMMO-python/pull/121) ([dependabot[bot]](https://github.com/apps/dependabot))
- Made ontoconvert and ontograph tools executable in linux [\#120](https://github.com/emmo-repo/EMMO-python/pull/120) ([jesper-friis](https://github.com/jesper-friis))
- Update CI  [\#119](https://github.com/emmo-repo/EMMO-python/pull/119) ([CasperWA](https://github.com/CasperWA))
- Update publish workflow + add dependabot [\#116](https://github.com/emmo-repo/EMMO-python/pull/116) ([CasperWA](https://github.com/CasperWA))

## [v1.0.0-alpha-25](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-25) (2021-01-17)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-24...v1.0.0-alpha-25)

**Closed issues:**

- Update Dockerfile to install correct pandoc [\#99](https://github.com/emmo-repo/EMMO-python/issues/99)
- Correct turtle serialisation [\#97](https://github.com/emmo-repo/EMMO-python/issues/97)

**Merged pull requests:**

- Update emmocheck exceptions [\#113](https://github.com/emmo-repo/EMMO-python/pull/113) ([jesper-friis](https://github.com/jesper-friis))
- Fix recursion in graph [\#112](https://github.com/emmo-repo/EMMO-python/pull/112) ([jesper-friis](https://github.com/jesper-friis))
- Avoid unnessesary/infinite recursion in get\_imported\_ontologies\(\) [\#111](https://github.com/emmo-repo/EMMO-python/pull/111) ([jesper-friis](https://github.com/jesper-friis))
- Break recursion error in get\_by\_label\(\) [\#110](https://github.com/emmo-repo/EMMO-python/pull/110) ([jesper-friis](https://github.com/jesper-friis))
- Updated the Ontology.sync\_attributes\(\) method. [\#107](https://github.com/emmo-repo/EMMO-python/pull/107) ([jesper-friis](https://github.com/jesper-friis))
- Updated pandoc req in Dockerfile [\#106](https://github.com/emmo-repo/EMMO-python/pull/106) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-24](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-24) (2021-01-04)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-23...v1.0.0-alpha-24)

**Merged pull requests:**

- Bumped version number up to 1.0.0-alpha-24  [\#105](https://github.com/emmo-repo/EMMO-python/pull/105) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-23](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-23) (2021-01-04)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-22...v1.0.0-alpha-23)

**Closed issues:**

- Fix loading imported ttl from web such that emmocheck works for crystallography.ttl [\#98](https://github.com/emmo-repo/EMMO-python/issues/98)
- Add reasoning with FaCT++ [\#95](https://github.com/emmo-repo/EMMO-python/issues/95)
- Correctly load ontologies like crystallography that imports both local and online sub-ontologies [\#91](https://github.com/emmo-repo/EMMO-python/issues/91)
- Fix flake8 errors [\#88](https://github.com/emmo-repo/EMMO-python/issues/88)
- Remove the .ttl namespace when loading domain-crystallography in EMMO-python [\#83](https://github.com/emmo-repo/EMMO-python/issues/83)
- Add option of documenting imported ontologies in ontodoc and ontograph [\#82](https://github.com/emmo-repo/EMMO-python/issues/82)
- Emmocheck fails if Physicaluantities and MeaurementsUnits are not imported from emmo. Make sure that it does not fail if whole of EMMO is not imported. [\#80](https://github.com/emmo-repo/EMMO-python/issues/80)
- Ontograph: Make default root [\#79](https://github.com/emmo-repo/EMMO-python/issues/79)
- Ontodoc: PDF is not generated, produces error. [\#76](https://github.com/emmo-repo/EMMO-python/issues/76)
- AttributeError from ontodoc [\#70](https://github.com/emmo-repo/EMMO-python/issues/70)
- Import emmo .ttl from emmo-repo.github.io [\#69](https://github.com/emmo-repo/EMMO-python/issues/69)
- Unable to use the vertical interoperability demo .py files [\#66](https://github.com/emmo-repo/EMMO-python/issues/66)

**Merged pull requests:**

- Release 1.0.0-alpha-23 [\#104](https://github.com/emmo-repo/EMMO-python/pull/104) ([jesper-friis](https://github.com/jesper-friis))
- Allow to load turtle ontologies without catalog file. [\#102](https://github.com/emmo-repo/EMMO-python/pull/102) ([jesper-friis](https://github.com/jesper-friis))
- Bump junit from 4.11 to 4.13.1 in /emmo/factpluspluswrapper/java [\#101](https://github.com/emmo-repo/EMMO-python/pull/101) ([dependabot[bot]](https://github.com/apps/dependabot))
- Updated README file [\#100](https://github.com/emmo-repo/EMMO-python/pull/100) ([jesper-friis](https://github.com/jesper-friis))
- Changed the sync\_reasoner\(\) method to use FaCT++ as the default reasoner [\#94](https://github.com/emmo-repo/EMMO-python/pull/94) ([jesper-friis](https://github.com/jesper-friis))
- Add reasoning [\#93](https://github.com/emmo-repo/EMMO-python/pull/93) ([jesper-friis](https://github.com/jesper-friis))
- Improve load ontologies [\#92](https://github.com/emmo-repo/EMMO-python/pull/92) ([jesper-friis](https://github.com/jesper-friis))
- Remove the '.ttl' in namespace names by monkey patching owlready2.Namespace [\#90](https://github.com/emmo-repo/EMMO-python/pull/90) ([jesper-friis](https://github.com/jesper-friis))
- Fix flake8 warnings [\#89](https://github.com/emmo-repo/EMMO-python/pull/89) ([jesper-friis](https://github.com/jesper-friis))
- Ontodoc pdf [\#87](https://github.com/emmo-repo/EMMO-python/pull/87) ([jesper-friis](https://github.com/jesper-friis))
- Automatically find roots in ontograph  [\#85](https://github.com/emmo-repo/EMMO-python/pull/85) ([francescalb](https://github.com/francescalb))
- Automatic import of ttl from GitHub emmo-repo.io [\#84](https://github.com/emmo-repo/EMMO-python/pull/84) ([francescalb](https://github.com/francescalb))
- Fixes needed for access ontologies [\#77](https://github.com/emmo-repo/EMMO-python/pull/77) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-22](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-22) (2020-12-21)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-21b...v1.0.0-alpha-22)

**Merged pull requests:**

- Loading ttl both locally and importing from iri [\#75](https://github.com/emmo-repo/EMMO-python/pull/75) ([francescalb](https://github.com/francescalb))
- Added sync\_python\_names\(\) and corrected handling of individuals in sync\_attributes\(\) [\#73](https://github.com/emmo-repo/EMMO-python/pull/73) ([jesper-friis](https://github.com/jesper-friis))
- Add preflabel to individuals declared in python [\#72](https://github.com/emmo-repo/EMMO-python/pull/72) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-21b](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-21b) (2020-12-13)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-21...v1.0.0-alpha-21b)

**Merged pull requests:**

- Fix bug introduced in ontoconvert [\#71](https://github.com/emmo-repo/EMMO-python/pull/71) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-21](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-21) (2020-12-11)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-20b...v1.0.0-alpha-21)

**Merged pull requests:**

- Use rdflib to load non-supported formats. [\#68](https://github.com/emmo-repo/EMMO-python/pull/68) ([jesper-friis](https://github.com/jesper-friis))
- Added a quick fix for vertical demo. [\#67](https://github.com/emmo-repo/EMMO-python/pull/67) ([jesper-friis](https://github.com/jesper-friis))
- Updated emmocheck to new 1.0.0-beta. Old version should still work. [\#65](https://github.com/emmo-repo/EMMO-python/pull/65) ([jesper-friis](https://github.com/jesper-friis))
- Added ontoconvert tool [\#64](https://github.com/emmo-repo/EMMO-python/pull/64) ([jesper-friis](https://github.com/jesper-friis))
- Improved error messages for classes that doesn't define prefLabel [\#63](https://github.com/emmo-repo/EMMO-python/pull/63) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-20b](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-20b) (2020-11-04)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-20...v1.0.0-alpha-20b)

**Merged pull requests:**

- Version1.0.0 alpha20 [\#62](https://github.com/emmo-repo/EMMO-python/pull/62) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-20](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-20) (2020-11-04)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-19...v1.0.0-alpha-20)

**Merged pull requests:**

- Improve support for imported ontologies [\#61](https://github.com/emmo-repo/EMMO-python/pull/61) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-19](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-19) (2020-11-02)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-18...v1.0.0-alpha-19)

**Merged pull requests:**

- Added --ignore-namespace to emmocheck  [\#60](https://github.com/emmo-repo/EMMO-python/pull/60) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-18](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-18) (2020-10-29)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-17...v1.0.0-alpha-18)

**Merged pull requests:**

- Bumped up version number to 1.0.0-alpha-18 [\#59](https://github.com/emmo-repo/EMMO-python/pull/59) ([jesper-friis](https://github.com/jesper-friis))
- Added option url\_from\_catalog to ontology.load\(\) [\#58](https://github.com/emmo-repo/EMMO-python/pull/58) ([jesper-friis](https://github.com/jesper-friis))
- Added get\_preferred\_label\(\) method to classes, properties and individuals [\#57](https://github.com/emmo-repo/EMMO-python/pull/57) ([jesper-friis](https://github.com/jesper-friis))
- Correct default IRI to inferred ontology [\#56](https://github.com/emmo-repo/EMMO-python/pull/56) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-17](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-17) (2020-10-21)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-16...v1.0.0-alpha-17)

**Merged pull requests:**

- Added materials.EngineeredMaterial to namespace exception in emmocheck [\#55](https://github.com/emmo-repo/EMMO-python/pull/55) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-16](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-16) (2020-10-20)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-15...v1.0.0-alpha-16)

**Closed issues:**

- Include all annotations in .get\_annotations\(\) [\#50](https://github.com/emmo-repo/EMMO-python/issues/50)

**Merged pull requests:**

- Update to v1.0.0-alpha-16 for new release [\#54](https://github.com/emmo-repo/EMMO-python/pull/54) ([francescalb](https://github.com/francescalb))
- Update dimensionality checks [\#53](https://github.com/emmo-repo/EMMO-python/pull/53) ([jesper-friis](https://github.com/jesper-friis))
- Updated to say that pypi realese is automatic in docs [\#52](https://github.com/emmo-repo/EMMO-python/pull/52) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-15](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-15) (2020-09-25)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-13...v1.0.0-alpha-15)

**Merged pull requests:**

- Added all labels in get\_class\_annotations in emmo/patch.py including [\#51](https://github.com/emmo-repo/EMMO-python/pull/51) ([francescalb](https://github.com/francescalb))
- Support use of skos:prefLabel instead of rdfs:label [\#49](https://github.com/emmo-repo/EMMO-python/pull/49) ([jesper-friis](https://github.com/jesper-friis))
- v1.0.0-alpha-14  [\#48](https://github.com/emmo-repo/EMMO-python/pull/48) ([jesper-friis](https://github.com/jesper-friis))
- Fix emmocheck to not fail upon use of dcterms and skos [\#47](https://github.com/emmo-repo/EMMO-python/pull/47) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-13](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-13) (2020-09-19)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-11...v1.0.0-alpha-13)

**Closed issues:**

- Not immediately installable with pip [\#45](https://github.com/emmo-repo/EMMO-python/issues/45)

**Merged pull requests:**

- Fix setup [\#46](https://github.com/emmo-repo/EMMO-python/pull/46) ([jesper-friis](https://github.com/jesper-friis))
- Make emmo package pip installable in fresh env [\#44](https://github.com/emmo-repo/EMMO-python/pull/44) ([CasperWA](https://github.com/CasperWA))
- Update emmodoc to latest version of emmo-alpha2 [\#43](https://github.com/emmo-repo/EMMO-python/pull/43) ([jesper-friis](https://github.com/jesper-friis))
- Ensure that emmocheck exit with non-zero return value if a test is faing [\#42](https://github.com/emmo-repo/EMMO-python/pull/42) ([jesper-friis](https://github.com/jesper-friis))
- Installed missing dependencies in pythonpublish deployment workflow [\#41](https://github.com/emmo-repo/EMMO-python/pull/41) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-11](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-11) (2020-08-12)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-10...v1.0.0-alpha-11)

**Merged pull requests:**

- Add skip option to emmocheck [\#40](https://github.com/emmo-repo/EMMO-python/pull/40) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-10](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-10) (2020-04-27)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-9...v1.0.0-alpha-10)

**Merged pull requests:**

- Added exceptions to emmocheck "test\_number\_of\_labels" [\#39](https://github.com/emmo-repo/EMMO-python/pull/39) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-9](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-9) (2020-04-13)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-8...v1.0.0-alpha-9)

**Closed issues:**

- Enhance ontology.sync\_attributes\(\) to also update class names [\#10](https://github.com/emmo-repo/EMMO-python/issues/10)
- Add support for the FaCT++ reasoner [\#9](https://github.com/emmo-repo/EMMO-python/issues/9)

**Merged pull requests:**

- Set new release version 1.0.0-alpha-9 [\#38](https://github.com/emmo-repo/EMMO-python/pull/38) ([francescalb](https://github.com/francescalb))
- Added get\_version\(\) and set\_version\(\) methods to emmo.Ontology. [\#37](https://github.com/emmo-repo/EMMO-python/pull/37) ([jesper-friis](https://github.com/jesper-friis))
- Updated example in README file to current version of EMMO. [\#36](https://github.com/emmo-repo/EMMO-python/pull/36) ([jesper-friis](https://github.com/jesper-friis))
- Update tools [\#35](https://github.com/emmo-repo/EMMO-python/pull/35) ([jesper-friis](https://github.com/jesper-friis))
- Updated simplifed demo\_vertical in compliance with EMMO-1.0.0alpha2 as of 202… [\#34](https://github.com/emmo-repo/EMMO-python/pull/34) ([francescalb](https://github.com/francescalb))
- Fixed PyPI badge in README [\#33](https://github.com/emmo-repo/EMMO-python/pull/33) ([jesper-friis](https://github.com/jesper-friis))
- Update emmocheck [\#32](https://github.com/emmo-repo/EMMO-python/pull/32) ([jesper-friis](https://github.com/jesper-friis))
- Sync attributes [\#31](https://github.com/emmo-repo/EMMO-python/pull/31) ([jesper-friis](https://github.com/jesper-friis))
- Cleanup ci workflow [\#28](https://github.com/emmo-repo/EMMO-python/pull/28) ([jesper-friis](https://github.com/jesper-friis))
- Added ontoversion tool [\#27](https://github.com/emmo-repo/EMMO-python/pull/27) ([jesper-friis](https://github.com/jesper-friis))
- Update emmodoc [\#25](https://github.com/emmo-repo/EMMO-python/pull/25) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-8](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-8) (2020-03-22)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-5...v1.0.0-alpha-8)

**Merged pull requests:**

- 1.0.0 alpha 8 [\#30](https://github.com/emmo-repo/EMMO-python/pull/30) ([jesper-friis](https://github.com/jesper-friis))
- Updated requirements such that "pip install EMMO" works [\#24](https://github.com/emmo-repo/EMMO-python/pull/24) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-5](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-5) (2020-03-18)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-3...v1.0.0-alpha-5)

**Implemented enhancements:**

- Make EMMO-python available on pypi \(installable with pip\) [\#7](https://github.com/emmo-repo/EMMO-python/issues/7)

**Merged pull requests:**

- Bumbed up version to 1.0.0-alpha-5 [\#23](https://github.com/emmo-repo/EMMO-python/pull/23) ([jesper-friis](https://github.com/jesper-friis))
- Emmocheck [\#22](https://github.com/emmo-repo/EMMO-python/pull/22) ([jesper-friis](https://github.com/jesper-friis))
- Reworked the generation of graphs - using the graphviz Python package [\#21](https://github.com/emmo-repo/EMMO-python/pull/21) ([jesper-friis](https://github.com/jesper-friis))
- 1.0.0 [\#19](https://github.com/emmo-repo/EMMO-python/pull/19) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-3](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-3) (2020-02-16)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-2...v1.0.0-alpha-3)

## [v1.0.0-alpha-2](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-2) (2020-01-11)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha-1...v1.0.0-alpha-2)

## [v1.0.0-alpha-1](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha-1) (2020-01-11)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v1.0.0-alpha...v1.0.0-alpha-1)

**Closed issues:**

- Missing https://emmc.info/emmo-inferred [\#16](https://github.com/emmo-repo/EMMO-python/issues/16)
- setup.py [\#15](https://github.com/emmo-repo/EMMO-python/issues/15)
- Fix emmodoc [\#6](https://github.com/emmo-repo/EMMO-python/issues/6)

## [v1.0.0-alpha](https://github.com/emmo-repo/EMMO-python/tree/v1.0.0-alpha) (2020-01-08)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/v0.9.9...v1.0.0-alpha)

**Closed issues:**

- Update the user case ontology [\#3](https://github.com/emmo-repo/EMMO-python/issues/3)

**Merged pull requests:**

- Fixed a typo in the title [\#14](https://github.com/emmo-repo/EMMO-python/pull/14) ([blokhin](https://github.com/blokhin))
- Fixed \#5 - homogenised call to reasoner [\#13](https://github.com/emmo-repo/EMMO-python/pull/13) ([francescalb](https://github.com/francescalb))

## [v0.9.9](https://github.com/emmo-repo/EMMO-python/tree/v0.9.9) (2019-07-14)

[Full Changelog](https://github.com/emmo-repo/EMMO-python/compare/34866fa72fea0b178cabbe21dfee06f735bbf373...v0.9.9)

**Closed issues:**

- Homogenise call to reasoner in emmo.Ontology.sync\_reasoner\(\) [\#5](https://github.com/emmo-repo/EMMO-python/issues/5)

**Merged pull requests:**

- \#3 update usercase ontology [\#12](https://github.com/emmo-repo/EMMO-python/pull/12) ([jesper-friis](https://github.com/jesper-friis))
- Fixed 3 [\#8](https://github.com/emmo-repo/EMMO-python/pull/8) ([jesper-friis](https://github.com/jesper-friis))
- Dockerdevel [\#2](https://github.com/emmo-repo/EMMO-python/pull/2) ([francescalb](https://github.com/francescalb))
- Fix by lukas [\#1](https://github.com/emmo-repo/EMMO-python/pull/1) ([jesper-friis](https://github.com/jesper-friis))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
