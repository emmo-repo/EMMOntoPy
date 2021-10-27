# Changelog

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
