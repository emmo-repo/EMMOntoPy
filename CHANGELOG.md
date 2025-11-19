# Changelog

## [v0.8.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.8.1) (2025-07-31)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.8.0...v0.8.1)

**Fixed bugs:**

- check only emmo terms [\#851](https://github.com/emmo-repo/EMMOntoPy/issues/851)

**Closed issues:**

- Add possibility of specifying IRI in new\_class etc. [\#843](https://github.com/emmo-repo/EMMOntoPy/issues/843)
- How to access metadata such as abstract and creators? [\#841](https://github.com/emmo-repo/EMMOntoPy/issues/841)

**Merged pull requests:**

- Recursive creation of squashed ontologies [\#869](https://github.com/emmo-repo/EMMOntoPy/pull/869) ([jesper-friis](https://github.com/jesper-friis))
- Deprecate support for python 3.8 [\#868](https://github.com/emmo-repo/EMMOntoPy/pull/868) ([francescalb](https://github.com/francescalb))
- Added `--namespace` option to `ontoconvert` [\#867](https://github.com/emmo-repo/EMMOntoPy/pull/867) ([jesper-friis](https://github.com/jesper-friis))
- Handle timeout errors in redirectioncheck [\#864](https://github.com/emmo-repo/EMMOntoPy/pull/864) ([jesper-friis](https://github.com/jesper-friis))
- move from sintef/ci-cd safety to safety own setup [\#854](https://github.com/emmo-repo/EMMOntoPy/pull/854) ([francescalb](https://github.com/francescalb))
- Emmocheck now does not check prefLabel for any of entities specific prefixes [\#852](https://github.com/emmo-repo/EMMOntoPy/pull/852) ([francescalb](https://github.com/francescalb))
- Made metadata repr easier to read. [\#847](https://github.com/emmo-repo/EMMOntoPy/pull/847) ([jesper-friis](https://github.com/jesper-friis))
- Update Metadata so that all metadata-items can be accessed [\#845](https://github.com/emmo-repo/EMMOntoPy/pull/845) ([francescalb](https://github.com/francescalb))
- Added possibility of specifying iri in new\_entity [\#844](https://github.com/emmo-repo/EMMOntoPy/pull/844) ([francescalb](https://github.com/francescalb))

## [v0.8.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.8.0) (2025-03-18)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.3...v0.8.0)

**Merged pull requests:**

- Update to emmo 1.0.0 as it is now released [\#839](https://github.com/emmo-repo/EMMOntoPy/pull/839) ([francescalb](https://github.com/francescalb))
- Updated to include python3.13 [\#831](https://github.com/emmo-repo/EMMOntoPy/pull/831) ([francescalb](https://github.com/francescalb))

## [v0.7.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.7.3) (2025-03-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.2...v0.7.3)

**Closed issues:**

- Loading non-emmo-related ontologies [\#811](https://github.com/emmo-repo/EMMOntoPy/issues/811)
- The test for load\_foaf is bypassed. [\#797](https://github.com/emmo-repo/EMMOntoPy/issues/797)
- Explicitly support Python 3.12 [\#763](https://github.com/emmo-repo/EMMOntoPy/issues/763)
- Update to emmo-beta5 [\#680](https://github.com/emmo-repo/EMMOntoPy/issues/680)

**Merged pull requests:**

- Ignore automatic dependency updates Python3.8 [\#830](https://github.com/emmo-repo/EMMOntoPy/pull/830) ([francescalb](https://github.com/francescalb))
- Minor fix for fact++ [\#817](https://github.com/emmo-repo/EMMOntoPy/pull/817) ([jesper-friis](https://github.com/jesper-friis))
- Importing rdfs schemas [\#814](https://github.com/emmo-repo/EMMOntoPy/pull/814) ([francescalb](https://github.com/francescalb))
- Updated sync\_reasoner\(\) such that it works for FaCT++ [\#810](https://github.com/emmo-repo/EMMOntoPy/pull/810) ([jesper-friis](https://github.com/jesper-friis))
- Updated emmocheck to ahead to latest formulation of units [\#809](https://github.com/emmo-repo/EMMOntoPy/pull/809) ([jesper-friis](https://github.com/jesper-friis))
- Added find\(\) method [\#807](https://github.com/emmo-repo/EMMOntoPy/pull/807) ([jesper-friis](https://github.com/jesper-friis))
- Added utils.get\_datatype\_class\(\) [\#804](https://github.com/emmo-repo/EMMOntoPy/pull/804) ([jesper-friis](https://github.com/jesper-friis))
- Added test\_unit\_dimension\_rc1\(\) [\#798](https://github.com/emmo-repo/EMMOntoPy/pull/798) ([jesper-friis](https://github.com/jesper-friis))
- Corrected test when loading rdfs. It used type for is\_a.  [\#796](https://github.com/emmo-repo/EMMOntoPy/pull/796) ([francescalb](https://github.com/francescalb))
- Handle owlready2:python\_names in genated triples in excelparser [\#795](https://github.com/emmo-repo/EMMOntoPy/pull/795) ([francescalb](https://github.com/francescalb))
- Added figures to generated documentation [\#767](https://github.com/emmo-repo/EMMOntoPy/pull/767) ([jesper-friis](https://github.com/jesper-friis))

## [v0.7.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.7.2) (2024-10-25)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.1...v0.7.2)

**Closed issues:**

- excelparser, allow for = in strings for other annotations. [\#751](https://github.com/emmo-repo/EMMOntoPy/issues/751)
- Add options to ontoconvert for adding annotations expected by FOOPS [\#728](https://github.com/emmo-repo/EMMOntoPy/issues/728)
- Remove or rename "old" version tags [\#547](https://github.com/emmo-repo/EMMOntoPy/issues/547)

**Merged pull requests:**

- Corrected publishing info [\#792](https://github.com/emmo-repo/EMMOntoPy/pull/792) ([francescalb](https://github.com/francescalb))
- Flb/trusted publisher on pypi [\#791](https://github.com/emmo-repo/EMMOntoPy/pull/791) ([francescalb](https://github.com/francescalb))
- Updated to owlready2==0.44 [\#780](https://github.com/emmo-repo/EMMOntoPy/pull/780) ([francescalb](https://github.com/francescalb))
- Added release\_pat secret to ci\_cd\_updated\_master workflow [\#777](https://github.com/emmo-repo/EMMOntoPy/pull/777) ([francescalb](https://github.com/francescalb))
- Added test for descriptions [\#766](https://github.com/emmo-repo/EMMOntoPy/pull/766) ([jesper-friis](https://github.com/jesper-friis))
- Fixed failing test\_save in master [\#756](https://github.com/emmo-repo/EMMOntoPy/pull/756) ([jesper-friis](https://github.com/jesper-friis))
- Added possibility for = in extra annotations defined in excelparser [\#752](https://github.com/emmo-repo/EMMOntoPy/pull/752) ([francescalb](https://github.com/francescalb))
- Load doamin-battery instead of battinfo which is just an extra wrapping [\#745](https://github.com/emmo-repo/EMMOntoPy/pull/745) ([francescalb](https://github.com/francescalb))
- Rewriting ontodoc based on domain-battery [\#742](https://github.com/emmo-repo/EMMOntoPy/pull/742) ([jesper-friis](https://github.com/jesper-friis))
- Make it possible to run HermiT on EMMO [\#740](https://github.com/emmo-repo/EMMOntoPy/pull/740) ([jesper-friis](https://github.com/jesper-friis))
- Added minor fixes for ontoconvert [\#739](https://github.com/emmo-repo/EMMOntoPy/pull/739) ([jesper-friis](https://github.com/jesper-friis))
- Added additional recognised prefixes [\#734](https://github.com/emmo-repo/EMMOntoPy/pull/734) ([jesper-friis](https://github.com/jesper-friis))
- Copy EMMO annotations [\#733](https://github.com/emmo-repo/EMMOntoPy/pull/733) ([jesper-friis](https://github.com/jesper-friis))
- Add --copy-annotation option to ontoconvert [\#732](https://github.com/emmo-repo/EMMOntoPy/pull/732) ([jesper-friis](https://github.com/jesper-friis))
- Updated list of IRIs to ignore when checking prefLabel [\#731](https://github.com/emmo-repo/EMMOntoPy/pull/731) ([jesper-friis](https://github.com/jesper-friis))

## [v0.7.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.7.1) (2024-02-29)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.0.1...v0.7.1)

## [v0.7.0.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.7.0.1) (2024-02-29)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.0...v0.7.0.1)

**Closed issues:**

- Implement ontoconvert --base-iri argument [\#716](https://github.com/emmo-repo/EMMOntoPy/issues/716)

**Merged pull requests:**

- Added `yield from` [\#720](https://github.com/emmo-repo/EMMOntoPy/pull/720) ([jesper-friis](https://github.com/jesper-friis))
- Correct saving squashed ontology [\#719](https://github.com/emmo-repo/EMMOntoPy/pull/719) ([jesper-friis](https://github.com/jesper-friis))
- Updated ontoconvert help [\#715](https://github.com/emmo-repo/EMMOntoPy/pull/715) ([jesper-friis](https://github.com/jesper-friis))

## [v0.7.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.7.0) (2024-01-26)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.6.3...v0.7.0)

**Merged pull requests:**

- Ontology copy [\#711](https://github.com/emmo-repo/EMMOntoPy/pull/711) ([francescalb](https://github.com/francescalb))
- Update save recursive and layout [\#710](https://github.com/emmo-repo/EMMOntoPy/pull/710) ([francescalb](https://github.com/francescalb))

## [v0.6.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.6.3) (2024-01-25)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.6.2...v0.6.3)

**Merged pull requests:**

- Fix infinite recursion in directory layout [\#708](https://github.com/emmo-repo/EMMOntoPy/pull/708) ([jesper-friis](https://github.com/jesper-friis))
- Ensure that saving with squash removes all but current ontology [\#707](https://github.com/emmo-repo/EMMOntoPy/pull/707) ([jesper-friis](https://github.com/jesper-friis))
- Turned on directory layout tests for emmo and made them pytest [\#706](https://github.com/emmo-repo/EMMOntoPy/pull/706) ([francescalb](https://github.com/francescalb))

## [v0.6.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.6.2) (2024-01-23)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.6.1...v0.6.2)

**Merged pull requests:**

- Allow controling ontology IRI when saving [\#700](https://github.com/emmo-repo/EMMOntoPy/pull/700) ([jesper-friis](https://github.com/jesper-friis))

## [v0.6.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.6.1) (2024-01-18)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.6.0...v0.6.1)

**Closed issues:**

- No tests for ontology.save [\#684](https://github.com/emmo-repo/EMMOntoPy/issues/684)
- Allow using HermiT from ontoconvert [\#664](https://github.com/emmo-repo/EMMOntoPy/issues/664)
- PrefLabel used by new\_entity, and get\_by\_label even if it is not in the ontology [\#642](https://github.com/emmo-repo/EMMOntoPy/issues/642)
- ontology\(imported=True\) returns all classes in world [\#640](https://github.com/emmo-repo/EMMOntoPy/issues/640)
- excel2onto example doesn't come into the github pages documentation [\#626](https://github.com/emmo-repo/EMMOntoPy/issues/626)
- owlready2 \> 0.41 fails [\#624](https://github.com/emmo-repo/EMMOntoPy/issues/624)
- get\_by\_label and get\_by\_label all force add label\_annotations [\#621](https://github.com/emmo-repo/EMMOntoPy/issues/621)

**Merged pull requests:**

- Avoid infinite recursion in set\_common\_prefix\(\) [\#701](https://github.com/emmo-repo/EMMOntoPy/pull/701) ([jesper-friis](https://github.com/jesper-friis))
- Updated the getattr patch [\#699](https://github.com/emmo-repo/EMMOntoPy/pull/699) ([jesper-friis](https://github.com/jesper-friis))
- WIP: Fix issues with changed IRIs effecting test\_excelparser [\#697](https://github.com/emmo-repo/EMMOntoPy/pull/697) ([jesper-friis](https://github.com/jesper-friis))
- Added directory\_layout\(\) function [\#696](https://github.com/emmo-repo/EMMOntoPy/pull/696) ([jesper-friis](https://github.com/jesper-friis))
- Added redirection checking tool [\#695](https://github.com/emmo-repo/EMMOntoPy/pull/695) ([jesper-friis](https://github.com/jesper-friis))
- Add test save [\#686](https://github.com/emmo-repo/EMMOntoPy/pull/686) ([francescalb](https://github.com/francescalb))
- Update test\_unit\_dimension in emmocheck to EMMO 1.0.0-beta5 [\#678](https://github.com/emmo-repo/EMMOntoPy/pull/678) ([jesper-friis](https://github.com/jesper-friis))
- Skip checking dimensional units for domain ontologies that doesn't load this class. [\#677](https://github.com/emmo-repo/EMMOntoPy/pull/677) ([jesper-friis](https://github.com/jesper-friis))
- HermiT is default reasoner. [\#671](https://github.com/emmo-repo/EMMOntoPy/pull/671) ([francescalb](https://github.com/francescalb))
- Ci/dependabot updates [\#662](https://github.com/emmo-repo/EMMOntoPy/pull/662) ([francescalb](https://github.com/francescalb))
- Updated emmocheck to new EMMO quantities and units [\#658](https://github.com/emmo-repo/EMMOntoPy/pull/658) ([jesper-friis](https://github.com/jesper-friis))
- Update README.md [\#657](https://github.com/emmo-repo/EMMOntoPy/pull/657) ([jesper-friis](https://github.com/jesper-friis))
- Corrected bug so that asking for entities in imported does not return all in world [\#655](https://github.com/emmo-repo/EMMOntoPy/pull/655) ([francescalb](https://github.com/francescalb))
- Corrected get\_by\_label to use only labels in the ontology [\#643](https://github.com/emmo-repo/EMMOntoPy/pull/643) ([francescalb](https://github.com/francescalb))
- Update to comply with owlready2\>0.41 [\#639](https://github.com/emmo-repo/EMMOntoPy/pull/639) ([francescalb](https://github.com/francescalb))
- Ontodoc example in documentation [\#630](https://github.com/emmo-repo/EMMOntoPy/pull/630) ([francescalb](https://github.com/francescalb))

## [v0.6.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.6.0) (2023-06-19)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.4...v0.6.0)

**Closed issues:**

- pyparsing has been updated [\#629](https://github.com/emmo-repo/EMMOntoPy/issues/629)

**Merged pull requests:**

- Check prefLabels in imported ontologies only if asked for. [\#628](https://github.com/emmo-repo/EMMOntoPy/pull/628) ([francescalb](https://github.com/francescalb))

## [v0.5.4](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.4) (2023-06-15)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.3.2...v0.5.4)

## [v0.5.3.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.3.2) (2023-06-15)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.3.1...v0.5.3.2)

**Merged pull requests:**

- remove warnings\_as\_errors in cd workflow introduced in 0.5.3 [\#625](https://github.com/emmo-repo/EMMOntoPy/pull/625) ([francescalb](https://github.com/francescalb))

## [v0.5.3.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.3.1) (2023-06-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.3...v0.5.3.1)

## [v0.5.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.3) (2023-06-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.2...v0.5.3)

**Closed issues:**

- Extend new\_entity to include properties [\#609](https://github.com/emmo-repo/EMMOntoPy/issues/609)
- Add support for Python 3.11 [\#599](https://github.com/emmo-repo/EMMOntoPy/issues/599)
- excelparser - enable object properties creation [\#587](https://github.com/emmo-repo/EMMOntoPy/issues/587)
- If there are altLabels that match, get\_by\_label\_all returns only the prefLabels. [\#511](https://github.com/emmo-repo/EMMOntoPy/issues/511)
- excel2onto: implement other annotations [\#462](https://github.com/emmo-repo/EMMOntoPy/issues/462)

**Merged pull requests:**

- default\_annotations no longer forced in get\_by\_label [\#623](https://github.com/emmo-repo/EMMOntoPy/pull/623) ([francescalb](https://github.com/francescalb))
- Updated documentation and excel sheet in example. [\#622](https://github.com/emmo-repo/EMMOntoPy/pull/622) ([francescalb](https://github.com/francescalb))
- Flb/excel2onto properties [\#620](https://github.com/emmo-repo/EMMOntoPy/pull/620) ([francescalb](https://github.com/francescalb))
- Fixed failing tests in test\_patch.py [\#618](https://github.com/emmo-repo/EMMOntoPy/pull/618) ([jesper-friis](https://github.com/jesper-friis))
- Add test for Python 3.11 and support it officially [\#615](https://github.com/emmo-repo/EMMOntoPy/pull/615) ([jesper-friis](https://github.com/jesper-friis))
- Added doctest [\#614](https://github.com/emmo-repo/EMMOntoPy/pull/614) ([jesper-friis](https://github.com/jesper-friis))
- Item access to classes [\#613](https://github.com/emmo-repo/EMMOntoPy/pull/613) ([jesper-friis](https://github.com/jesper-friis))
- Change ontology.new\_entity to also allow adding properties [\#610](https://github.com/emmo-repo/EMMOntoPy/pull/610) ([francescalb](https://github.com/francescalb))
- Added DOI badge [\#606](https://github.com/emmo-repo/EMMOntoPy/pull/606) ([jesper-friis](https://github.com/jesper-friis))

## [v0.5.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.2) (2023-05-24)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.1...v0.5.2)

**Fixed bugs:**

- Auto-merge dependabot PRs workflow invalid [\#566](https://github.com/emmo-repo/EMMOntoPy/issues/566)

**Closed issues:**

- Point to excelparser api from the tools-page [\#593](https://github.com/emmo-repo/EMMOntoPy/issues/593)
- BUG: pytest - missing remote file /0.5.0/electrochemicalquantities / ontology [\#589](https://github.com/emmo-repo/EMMOntoPy/issues/589)
- Owlready 0.41 support ? [\#588](https://github.com/emmo-repo/EMMOntoPy/issues/588)
- Allow space in labels [\#583](https://github.com/emmo-repo/EMMOntoPy/issues/583)
- is\_defined needs a better description  [\#563](https://github.com/emmo-repo/EMMOntoPy/issues/563)
- utils line 112 in get\_iri\_name link = "{lowerlabel}" vs "{label}" [\#562](https://github.com/emmo-repo/EMMOntoPy/issues/562)
- ontograph - update colour deafults [\#559](https://github.com/emmo-repo/EMMOntoPy/issues/559)
- ontograph - argument leafs should be leaves [\#558](https://github.com/emmo-repo/EMMOntoPy/issues/558)
- ontograph - write out more examples on how to use it [\#557](https://github.com/emmo-repo/EMMOntoPy/issues/557)
- ontograph --parents not working [\#556](https://github.com/emmo-repo/EMMOntoPy/issues/556)
- test\_graph2 is failing  [\#555](https://github.com/emmo-repo/EMMOntoPy/issues/555)
- Add client side redirection in generated html documentation [\#552](https://github.com/emmo-repo/EMMOntoPy/issues/552)
- Typos in PR template [\#523](https://github.com/emmo-repo/EMMOntoPy/issues/523)
- ontograph, read format from name [\#497](https://github.com/emmo-repo/EMMOntoPy/issues/497)

**Merged pull requests:**

- Add links to the original FaCT++ repo, GitHub profiles, etc. [\#600](https://github.com/emmo-repo/EMMOntoPy/pull/600) ([blokhin](https://github.com/blokhin))
- Added test update to PR template. [\#598](https://github.com/emmo-repo/EMMOntoPy/pull/598) ([jesper-friis](https://github.com/jesper-friis))
- Changed `is_defined` into a ThingClass property and improved its documentation. [\#597](https://github.com/emmo-repo/EMMOntoPy/pull/597) ([jesper-friis](https://github.com/jesper-friis))
- Added link to excelparser from tools for documentation of excel sheet. [\#594](https://github.com/emmo-repo/EMMOntoPy/pull/594) ([francescalb](https://github.com/francescalb))
- Bump SINTEF/ci-cd from 2.3.0 to 2.3.1 [\#584](https://github.com/emmo-repo/EMMOntoPy/pull/584) ([dependabot[bot]](https://github.com/apps/dependabot))
- Updated get\_by\_label\(\) so that it now accepts label, name and full iri [\#582](https://github.com/emmo-repo/EMMOntoPy/pull/582) ([jesper-friis](https://github.com/jesper-friis))
- Added two additional exceptions to emmocheck [\#577](https://github.com/emmo-repo/EMMOntoPy/pull/577) ([jesper-friis](https://github.com/jesper-friis))
- Bump SINTEF/ci-cd from 2.2.1 to 2.3.0 [\#575](https://github.com/emmo-repo/EMMOntoPy/pull/575) ([dependabot[bot]](https://github.com/apps/dependabot))
- get\_ancestors and get\_descendants have the same arguments. [\#572](https://github.com/emmo-repo/EMMOntoPy/pull/572) ([francescalb](https://github.com/francescalb))
- Bump SINTEF/ci-cd from 2.2.0 to 2.2.1 [\#571](https://github.com/emmo-repo/EMMOntoPy/pull/571) ([dependabot[bot]](https://github.com/apps/dependabot))
- ontograph: colour updates, examples, bugfix [\#569](https://github.com/emmo-repo/EMMOntoPy/pull/569) ([francescalb](https://github.com/francescalb))
- Bump SINTEF/ci-cd from 2.1.0 to 2.2.0 [\#567](https://github.com/emmo-repo/EMMOntoPy/pull/567) ([dependabot[bot]](https://github.com/apps/dependabot))
- Changed argument leafs to leaves, with deprecation warning in ontograph [\#564](https://github.com/emmo-repo/EMMOntoPy/pull/564) ([francescalb](https://github.com/francescalb))
- Corrected bug on getting default relation style. [\#561](https://github.com/emmo-repo/EMMOntoPy/pull/561) ([francescalb](https://github.com/francescalb))
- Fix internal links in generated documentation generated with ontodoc [\#548](https://github.com/emmo-repo/EMMOntoPy/pull/548) ([jesper-friis](https://github.com/jesper-friis))

## [v0.5.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.1) (2023-02-07)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.0...v0.5.1)

**Fixed bugs:**

- Use custom token for GitHub changelog generator [\#545](https://github.com/emmo-repo/EMMOntoPy/issues/545)
- Avoid using Azure mirror for APT packages [\#541](https://github.com/emmo-repo/EMMOntoPy/issues/541)

**Merged pull requests:**

- Use SINTEF/ci-cd v2.1.0 in CI/CD workflows [\#546](https://github.com/emmo-repo/EMMOntoPy/pull/546) ([CasperWA](https://github.com/CasperWA))
- Revert version to v0.5.0 [\#544](https://github.com/emmo-repo/EMMOntoPy/pull/544) ([CasperWA](https://github.com/CasperWA))
- Fix ontodoc for bigmap [\#543](https://github.com/emmo-repo/EMMOntoPy/pull/543) ([jesper-friis](https://github.com/jesper-friis))

## [v0.5.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.0) (2023-02-06)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.4.0...v0.5.0)

**Fixed bugs:**

- `LegacyVersion` does not exist in `packaging.version` [\#540](https://github.com/emmo-repo/EMMOntoPy/issues/540)
- ontodoc: Expect `is_instance_of` property to be iterable [\#506](https://github.com/emmo-repo/EMMOntoPy/issues/506)
- Reinstate `images/material.png` [\#495](https://github.com/emmo-repo/EMMOntoPy/issues/495)

**Closed issues:**

- Newest pylint \(2.15.4\) has intriduced some new rules. [\#534](https://github.com/emmo-repo/EMMOntoPy/issues/534)
- sync\_attributes according to emmo convention regenerates a new iri even if it already has a valid one [\#525](https://github.com/emmo-repo/EMMOntoPy/issues/525)
- Remove dependency on LegacyVersion of packaging [\#514](https://github.com/emmo-repo/EMMOntoPy/issues/514)
- pytests are importing packaging 22.0 even though it is not allowed in requirements [\#513](https://github.com/emmo-repo/EMMOntoPy/issues/513)
- ontodoc: adding annotations that are not strings fail [\#510](https://github.com/emmo-repo/EMMOntoPy/issues/510)
- get\_by\_label\_all only works after sync\_attributes [\#502](https://github.com/emmo-repo/EMMOntoPy/issues/502)
- excel2onto: support updating ontology  [\#501](https://github.com/emmo-repo/EMMOntoPy/issues/501)
- excel2onto: allow to use prefLabel already in imported ontologies [\#500](https://github.com/emmo-repo/EMMOntoPy/issues/500)
- Drop Python 3.6 support - extend Python \>3.7 support [\#486](https://github.com/emmo-repo/EMMOntoPy/issues/486)
- Update pypi-release github action [\#482](https://github.com/emmo-repo/EMMOntoPy/issues/482)
- Make workflows dispatchable [\#481](https://github.com/emmo-repo/EMMOntoPy/issues/481)
- excel2onto: Read catalog file for imported ontology [\#474](https://github.com/emmo-repo/EMMOntoPy/issues/474)
- Give option to write\_catalog for writing relative paths [\#473](https://github.com/emmo-repo/EMMOntoPy/issues/473)
- excel2onto: add choice of prefix for imported ontologies [\#467](https://github.com/emmo-repo/EMMOntoPy/issues/467)

## [v0.4.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.4.0) (2022-10-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.3.1...v0.4.0)

**Fixed bugs:**

- Update repo files with new repo name [\#479](https://github.com/emmo-repo/EMMOntoPy/issues/479)
- Pre-commit hook `bandit` failing [\#478](https://github.com/emmo-repo/EMMOntoPy/issues/478)
- Fix publish/release workflow [\#476](https://github.com/emmo-repo/EMMOntoPy/issues/476)
- excel2onto: not all relations are included in the generated ontology [\#457](https://github.com/emmo-repo/EMMOntoPy/issues/457)
- Unexpected behaviour of get\_unabbreviated\_triples\(\)  [\#454](https://github.com/emmo-repo/EMMOntoPy/issues/454)

**Closed issues:**

- excel2onto: restrictions does not allow for using "emmo:hasProcessOutput some xx" [\#464](https://github.com/emmo-repo/EMMOntoPy/issues/464)
- EMMO is updated to beta4, and now documentation fails [\#440](https://github.com/emmo-repo/EMMOntoPy/issues/440)
- some ObjectProperties from EMMO-beta-4.0 cause errors in OntoGraph [\#429](https://github.com/emmo-repo/EMMOntoPy/issues/429)
- Excelparser does not write catalog file correctly [\#421](https://github.com/emmo-repo/EMMOntoPy/issues/421)

## [v0.3.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.3.1) (2022-05-08)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.3.0...v0.3.1)

## [v0.3.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.3.0) (2022-05-05)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.2.0...v0.3.0)

## [v0.2.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.2.0) (2022-03-02)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.3...v0.2.0)

## [v0.1.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.3) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.2...v0.1.3)

## [v0.1.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.2) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.1...v0.1.2)

## [v0.1.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.1) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.0) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/34866fa72fea0b178cabbe21dfee06f735bbf373...v0.1.0)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
