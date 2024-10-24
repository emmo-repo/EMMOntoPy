# Changelog

## [v7.0.2](https://github.com/emmo-repo/EMMOntoPy/tree/v7.0.2) (2024-10-24)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.7.1...v7.0.2)

**Closed issues:**

- excelparser, allow for = in strings for other annotations. [\#751](https://github.com/emmo-repo/EMMOntoPy/issues/751)
- Add options to ontoconvert for adding annotations expected by FOOPS [\#728](https://github.com/emmo-repo/EMMOntoPy/issues/728)

**Merged pull requests:**

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
- hasPhysicalDimension convention has changed in EMMO-1.0.0-beta3 [\#347](https://github.com/emmo-repo/EMMOntoPy/issues/347)

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

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.3...v0.5.3.2)

**Merged pull requests:**

- remove warnings\_as\_errors in cd workflow introduced in 0.5.3 [\#625](https://github.com/emmo-repo/EMMOntoPy/pull/625) ([francescalb](https://github.com/francescalb))

## [v0.5.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.3) (2023-06-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.3.1...v0.5.3)

## [v0.5.3.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.5.3.1) (2023-06-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.5.2...v0.5.3.1)

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
- Harmonize get\_descendants and get\_ancestors [\#406](https://github.com/emmo-repo/EMMOntoPy/issues/406)
- Review default colours and style in ontopy/graph.py [\#345](https://github.com/emmo-repo/EMMOntoPy/issues/345)

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

**Merged pull requests:**

- Fix fixtures for Python3.7 [\#536](https://github.com/emmo-repo/EMMOntoPy/pull/536) ([CasperWA](https://github.com/CasperWA))
- Flb/fix to pylint2.15.4 [\#535](https://github.com/emmo-repo/EMMOntoPy/pull/535) ([francescalb](https://github.com/francescalb))
- Bypass punning in ontodoc. [\#532](https://github.com/emmo-repo/EMMOntoPy/pull/532) ([francescalb](https://github.com/francescalb))
- Added possibility to update ontology.  [\#527](https://github.com/emmo-repo/EMMOntoPy/pull/527) ([francescalb](https://github.com/francescalb))
- Only generate new uuid if not already a valid one [\#526](https://github.com/emmo-repo/EMMOntoPy/pull/526) ([francescalb](https://github.com/francescalb))
- Removed LegacyVersion from ontopy.utils [\#515](https://github.com/emmo-repo/EMMOntoPy/pull/515) ([francescalb](https://github.com/francescalb))
- Added fix for adding annotations that are not strings in ontodoc [\#512](https://github.com/emmo-repo/EMMOntoPy/pull/512) ([francescalb](https://github.com/francescalb))
- Do not trigger an emmocheck failure for ontologies with a foaf:logo annotation [\#509](https://github.com/emmo-repo/EMMOntoPy/pull/509) ([jesper-friis](https://github.com/jesper-friis))
- New concepts allowed even if name alrady exists in imported ontologies [\#504](https://github.com/emmo-repo/EMMOntoPy/pull/504) ([francescalb](https://github.com/francescalb))
- Corrected so that get\_by\_label\_all also returns all concepts [\#503](https://github.com/emmo-repo/EMMOntoPy/pull/503) ([francescalb](https://github.com/francescalb))
- Added correct material.png figure in tool-instructions [\#498](https://github.com/emmo-repo/EMMOntoPy/pull/498) ([francescalb](https://github.com/francescalb))
- Updated logo [\#494](https://github.com/emmo-repo/EMMOntoPy/pull/494) ([jesper-friis](https://github.com/jesper-friis))
- Makeover for CI/CD workflows, pre-commit & MkDocs [\#485](https://github.com/emmo-repo/EMMOntoPy/pull/485) ([CasperWA](https://github.com/CasperWA))
- write catalog now writes relative paths per default [\#483](https://github.com/emmo-repo/EMMOntoPy/pull/483) ([francescalb](https://github.com/francescalb))
- Setting prefix explicitly in excelparser [\#470](https://github.com/emmo-repo/EMMOntoPy/pull/470) ([francescalb](https://github.com/francescalb))

## [v0.4.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.4.0) (2022-10-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.3.1...v0.4.0)

**Fixed bugs:**

- Update repo files with new repo name [\#479](https://github.com/emmo-repo/EMMOntoPy/issues/479)
- Pre-commit hook `bandit` failing [\#478](https://github.com/emmo-repo/EMMOntoPy/issues/478)
- Fix publish/release workflow [\#476](https://github.com/emmo-repo/EMMOntoPy/issues/476)
- excel2onto: not all relations are included in the generated ontology [\#457](https://github.com/emmo-repo/EMMOntoPy/issues/457)
- Unexpected behaviour of get\_unabbreviated\_triples\(\)  [\#454](https://github.com/emmo-repo/EMMOntoPy/issues/454)
- Edge without label crash the graph creation [\#397](https://github.com/emmo-repo/EMMOntoPy/issues/397)

**Closed issues:**

- excel2onto: restrictions does not allow for using "emmo:hasProcessOutput some xx" [\#464](https://github.com/emmo-repo/EMMOntoPy/issues/464)
- EMMO is updated to beta4, and now documentation fails [\#440](https://github.com/emmo-repo/EMMOntoPy/issues/440)
- some ObjectProperties from EMMO-beta-4.0 cause errors in OntoGraph [\#429](https://github.com/emmo-repo/EMMOntoPy/issues/429)
- Excelparser does not write catalog file correctly [\#421](https://github.com/emmo-repo/EMMOntoPy/issues/421)
- Add support for prefix [\#416](https://github.com/emmo-repo/EMMOntoPy/issues/416)
- Pre.commit failed with ontology.py [\#415](https://github.com/emmo-repo/EMMOntoPy/issues/415)
- visualization of EMMO based ontology [\#412](https://github.com/emmo-repo/EMMOntoPy/issues/412)
- Avoid infinite recursion when loading catalog file [\#369](https://github.com/emmo-repo/EMMOntoPy/issues/369)
- Excelparser: Automatize emmo-based? [\#335](https://github.com/emmo-repo/EMMOntoPy/issues/335)
- What are the applications of EMMO for materials informatics? [\#325](https://github.com/emmo-repo/EMMOntoPy/issues/325)
- Provide 'support' for same entities with different namespaces [\#128](https://github.com/emmo-repo/EMMOntoPy/issues/128)
- Remove deprecated emmo/ontograph.py that uses pydot [\#103](https://github.com/emmo-repo/EMMOntoPy/issues/103)

**Merged pull requests:**

- Update from 'EMMO-python' -\> 'EMMOntoPy' [\#477](https://github.com/emmo-repo/EMMOntoPy/pull/477) ([CasperWA](https://github.com/CasperWA))
- Allow for adding prefix in manchester notation. [\#469](https://github.com/emmo-repo/EMMOntoPy/pull/469) ([francescalb](https://github.com/francescalb))
- Fixed issue with exel2onto: not all relations are included in the generated ontology [\#458](https://github.com/emmo-repo/EMMOntoPy/pull/458) ([jesper-friis](https://github.com/jesper-friis))
- Added documentation of excel2onto [\#456](https://github.com/emmo-repo/EMMOntoPy/pull/456) ([jesper-friis](https://github.com/jesper-friis))
- factpluspluswrapper README file [\#453](https://github.com/emmo-repo/EMMOntoPy/pull/453) ([jesper-friis](https://github.com/jesper-friis))
- Improved get\_unabbreviated\_triples\(\) [\#449](https://github.com/emmo-repo/EMMOntoPy/pull/449) ([jesper-friis](https://github.com/jesper-friis))
- Fix loading in windows, url paths [\#446](https://github.com/emmo-repo/EMMOntoPy/pull/446) ([francescalb](https://github.com/francescalb))
- Fixed reading web destinations defined in catalog [\#445](https://github.com/emmo-repo/EMMOntoPy/pull/445) ([francescalb](https://github.com/francescalb))
- SUPPORT EMMO-beta4.0 [\#441](https://github.com/emmo-repo/EMMOntoPy/pull/441) ([francescalb](https://github.com/francescalb))
- Support for userdefined prefixes [\#439](https://github.com/emmo-repo/EMMOntoPy/pull/439) ([francescalb](https://github.com/francescalb))
- Flb/issue421 [\#438](https://github.com/emmo-repo/EMMOntoPy/pull/438) ([francescalb](https://github.com/francescalb))
- Update demo [\#437](https://github.com/emmo-repo/EMMOntoPy/pull/437) ([jesper-friis](https://github.com/jesper-friis))
- Silence false negative from pylint on github [\#436](https://github.com/emmo-repo/EMMOntoPy/pull/436) ([jesper-friis](https://github.com/jesper-friis))
- Better error messages [\#435](https://github.com/emmo-repo/EMMOntoPy/pull/435) ([jesper-friis](https://github.com/jesper-friis))
- Updated logo. [\#418](https://github.com/emmo-repo/EMMOntoPy/pull/418) ([jesper-friis](https://github.com/jesper-friis))
- cytoscapegraph fails with missing edge labels [\#414](https://github.com/emmo-repo/EMMOntoPy/pull/414) ([francescalb](https://github.com/francescalb))

## [v0.3.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.3.1) (2022-05-08)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.3.0...v0.3.1)

**Merged pull requests:**

- Fixed typo in ontoconvert [\#409](https://github.com/emmo-repo/EMMOntoPy/pull/409) ([jesper-friis](https://github.com/jesper-friis))

## [v0.3.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.3.0) (2022-05-05)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.2.0...v0.3.0)

**Fixed bugs:**

- Documentation is currently not building [\#407](https://github.com/emmo-repo/EMMOntoPy/issues/407)
- Pytest is currently failing [\#384](https://github.com/emmo-repo/EMMOntoPy/issues/384)
- permission denied when working with temporary file [\#313](https://github.com/emmo-repo/EMMOntoPy/issues/313)

**Closed issues:**

- Make get\_descendants\(levels=1\) [\#403](https://github.com/emmo-repo/EMMOntoPy/issues/403)
- Add functionality for setting name part of IRI to prefLabel [\#398](https://github.com/emmo-repo/EMMOntoPy/issues/398)
- Generate excelsheet from ontology. [\#394](https://github.com/emmo-repo/EMMOntoPy/issues/394)
- Return a list of the concepts that are disregarded during when converting from excel with -force argument [\#393](https://github.com/emmo-repo/EMMOntoPy/issues/393)
- Demo - Broken ontology URLs [\#390](https://github.com/emmo-repo/EMMOntoPy/issues/390)
- Excelparser: how to handle entities that already exist in one of the imported ontologies? [\#334](https://github.com/emmo-repo/EMMOntoPy/issues/334)

**Merged pull requests:**

- Updated docs python handler [\#408](https://github.com/emmo-repo/EMMOntoPy/pull/408) ([CasperWA](https://github.com/CasperWA))
- Flb/get descendants [\#405](https://github.com/emmo-repo/EMMOntoPy/pull/405) ([francescalb](https://github.com/francescalb))
- Corrected expected number of returned arguments [\#404](https://github.com/emmo-repo/EMMOntoPy/pull/404) ([jesper-friis](https://github.com/jesper-friis))
- Add functionality for setting name part of IRI to prefLabel [\#399](https://github.com/emmo-repo/EMMOntoPy/pull/399) ([jesper-friis](https://github.com/jesper-friis))
- create\_from\_excel/pandas return as list of concepts that are worngly defined in the excelfile [\#396](https://github.com/emmo-repo/EMMOntoPy/pull/396) ([francescalb](https://github.com/francescalb))
- Download EMMO from raw.github deirectly as redirection is broken [\#392](https://github.com/emmo-repo/EMMOntoPy/pull/392) ([francescalb](https://github.com/francescalb))
- Workaround for failing test [\#385](https://github.com/emmo-repo/EMMOntoPy/pull/385) ([CasperWA](https://github.com/CasperWA))
- fix \#313 remove handle [\#315](https://github.com/emmo-repo/EMMOntoPy/pull/315) ([sygout](https://github.com/sygout))

## [v0.2.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.2.0) (2022-03-02)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.3...v0.2.0)

**Implemented enhancements:**

- spaces before or after word in prefLabel makes excelparser fail [\#332](https://github.com/emmo-repo/EMMOntoPy/issues/332)
- Make EMMOntopy PyPi [\#268](https://github.com/emmo-repo/EMMOntoPy/issues/268)
- Use `pre-commit` [\#243](https://github.com/emmo-repo/EMMOntoPy/issues/243)
- Standard dunder/magic methods for `Ontology` [\#228](https://github.com/emmo-repo/EMMOntoPy/issues/228)
- Update code styling and linting [\#223](https://github.com/emmo-repo/EMMOntoPy/issues/223)
- Fix checking PR body & improve error message in CD [\#318](https://github.com/emmo-repo/EMMOntoPy/pull/318) ([CasperWA](https://github.com/CasperWA))

**Fixed bugs:**

- GH GraphQL type issue for auto-merge workflow [\#374](https://github.com/emmo-repo/EMMOntoPy/issues/374)
- Missing warning for excel parser relations and problem with "nan" [\#365](https://github.com/emmo-repo/EMMOntoPy/issues/365)
- Seting metadata in excelparser fails if there are no imported ontologies. [\#331](https://github.com/emmo-repo/EMMOntoPy/issues/331)
- Edge-case fails CD workflow for dependabot [\#319](https://github.com/emmo-repo/EMMOntoPy/issues/319)
- Ontodoc failing due to wrong `rdflib` import [\#306](https://github.com/emmo-repo/EMMOntoPy/issues/306)
- Overwriting `get_triples()` method [\#280](https://github.com/emmo-repo/EMMOntoPy/issues/280)
- OpenModel logo not loading in README [\#278](https://github.com/emmo-repo/EMMOntoPy/issues/278)
- Disable FOAF test as xmlns.com is down [\#276](https://github.com/emmo-repo/EMMOntoPy/issues/276)

**Closed issues:**

- Use TEAM 4.0\[bot\] for GH Actions jobs [\#352](https://github.com/emmo-repo/EMMOntoPy/issues/352)
- \_get\_triples\_spo take argumens s, and p, not subject and predicate [\#350](https://github.com/emmo-repo/EMMOntoPy/issues/350)
- Add --force to excelparser [\#333](https://github.com/emmo-repo/EMMOntoPy/issues/333)
- Cannot load ontology in Windows. [\#328](https://github.com/emmo-repo/EMMOntoPy/issues/328)
- make get\_ontology accept 'PosixPath' [\#326](https://github.com/emmo-repo/EMMOntoPy/issues/326)
- Make EMMOntoPy baseexception and basewarning [\#321](https://github.com/emmo-repo/EMMOntoPy/issues/321)
- get\_by\_label crash  if not str [\#311](https://github.com/emmo-repo/EMMOntoPy/issues/311)
- make excel parser that creates and ontology from a filled excel file [\#302](https://github.com/emmo-repo/EMMOntoPy/issues/302)
- Check out how to get version of ontology [\#299](https://github.com/emmo-repo/EMMOntoPy/issues/299)
- Let ontology.new\_entity acccept one or more parents directly [\#294](https://github.com/emmo-repo/EMMOntoPy/issues/294)
- Make ManchesterSyntaxParser that returns Owlready2 [\#293](https://github.com/emmo-repo/EMMOntoPy/issues/293)
- onto.new\_entity should throw Error if label name consists of more than one word [\#290](https://github.com/emmo-repo/EMMOntoPy/issues/290)
- ReadTheDocs [\#288](https://github.com/emmo-repo/EMMOntoPy/issues/288)
- Add logo to README [\#287](https://github.com/emmo-repo/EMMOntoPy/issues/287)
- Write EMMO-python is deprecated and link to EMMOtopy on PyPi [\#269](https://github.com/emmo-repo/EMMOntoPy/issues/269)
- Consider MarkDown header styling [\#231](https://github.com/emmo-repo/EMMOntoPy/issues/231)

**Merged pull requests:**

- Use `ID!` type instead of `String!` [\#375](https://github.com/emmo-repo/EMMOntoPy/pull/375) ([CasperWA](https://github.com/CasperWA))
- Avoided infinite recursion when loading catalog files that recursively [\#370](https://github.com/emmo-repo/EMMOntoPy/pull/370) ([jesper-friis](https://github.com/jesper-friis))
- Warning relation excelparser [\#366](https://github.com/emmo-repo/EMMOntoPy/pull/366) ([sygout](https://github.com/sygout))
- Close temporary file before reading it [\#364](https://github.com/emmo-repo/EMMOntoPy/pull/364) ([jesper-friis](https://github.com/jesper-friis))
- Ignore safety ID 44715 + add numpy dependency [\#361](https://github.com/emmo-repo/EMMOntoPy/pull/361) ([CasperWA](https://github.com/CasperWA))
- Use TEAM 4.0\[bot\] [\#353](https://github.com/emmo-repo/EMMOntoPy/pull/353) ([CasperWA](https://github.com/CasperWA))
- Changed arguments in \_has\_obj\_triples\_spo [\#351](https://github.com/emmo-repo/EMMOntoPy/pull/351) ([francescalb](https://github.com/francescalb))
- Fix serialised ontology iri [\#341](https://github.com/emmo-repo/EMMOntoPy/pull/341) ([jesper-friis](https://github.com/jesper-friis))
- Corrected parsing cardinality restrictions [\#340](https://github.com/emmo-repo/EMMOntoPy/pull/340) ([jesper-friis](https://github.com/jesper-friis))
- When visualising restrictions, annotate the edges with the restriction type by default [\#339](https://github.com/emmo-repo/EMMOntoPy/pull/339) ([jesper-friis](https://github.com/jesper-friis))
- Flb/update excel parser accroding to thermodynamics example [\#336](https://github.com/emmo-repo/EMMOntoPy/pull/336) ([francescalb](https://github.com/francescalb))
- Added sconverting Posix to str in get\_ontology [\#327](https://github.com/emmo-repo/EMMOntoPy/pull/327) ([francescalb](https://github.com/francescalb))
- Added package specific base exception and base warning for EMMOntoPy [\#322](https://github.com/emmo-repo/EMMOntoPy/pull/322) ([francescalb](https://github.com/francescalb))
- Added checking that label is string in get\_by\_label [\#312](https://github.com/emmo-repo/EMMOntoPy/pull/312) ([francescalb](https://github.com/francescalb))
- Make excelparser that converts a filled excel sheet to an ontology [\#309](https://github.com/emmo-repo/EMMOntoPy/pull/309) ([francescalb](https://github.com/francescalb))
- Fix ontoconvert rdflib import [\#307](https://github.com/emmo-repo/EMMOntoPy/pull/307) ([CasperWA](https://github.com/CasperWA))
- Check first versionIRI then versionInfo in ontology.get\_version\(\) [\#301](https://github.com/emmo-repo/EMMOntoPy/pull/301) ([francescalb](https://github.com/francescalb))
- Removed .readthedocs.yml [\#298](https://github.com/emmo-repo/EMMOntoPy/pull/298) ([jesper-friis](https://github.com/jesper-friis))
- Added support for evaluating Manchester expression to owlready2 [\#296](https://github.com/emmo-repo/EMMOntoPy/pull/296) ([jesper-friis](https://github.com/jesper-friis))
- Added functionality for more than one parent in new\_entity [\#295](https://github.com/emmo-repo/EMMOntoPy/pull/295) ([francescalb](https://github.com/francescalb))
- Added test for label name length in ontology.new\_entity [\#291](https://github.com/emmo-repo/EMMOntoPy/pull/291) ([francescalb](https://github.com/francescalb))
- add logo to Readme and doc [\#289](https://github.com/emmo-repo/EMMOntoPy/pull/289) ([m-abdollahi](https://github.com/m-abdollahi))
- Improved representation of blank nodes [\#283](https://github.com/emmo-repo/EMMOntoPy/pull/283) ([jesper-friis](https://github.com/jesper-friis))
- Update method name to avoid overwriting inherited [\#281](https://github.com/emmo-repo/EMMOntoPy/pull/281) ([CasperWA](https://github.com/CasperWA))
- Fixed link to OpenModel logo [\#279](https://github.com/emmo-repo/EMMOntoPy/pull/279) ([francescalb](https://github.com/francescalb))
- Skip FOAF test [\#277](https://github.com/emmo-repo/EMMOntoPy/pull/277) ([CasperWA](https://github.com/CasperWA))
- Added Standard methods to Ontology [\#246](https://github.com/emmo-repo/EMMOntoPy/pull/246) ([francescalb](https://github.com/francescalb))
- Implement `pre-commit` & various tools [\#245](https://github.com/emmo-repo/EMMOntoPy/pull/245) ([CasperWA](https://github.com/CasperWA))

## [v0.1.3](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.3) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.2...v0.1.3)

## [v0.1.2](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.2) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.1...v0.1.2)

## [v0.1.1](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.1) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.1.0...v0.1.1)

## [v0.1.0](https://github.com/emmo-repo/EMMOntoPy/tree/v0.1.0) (2021-10-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.1b...v0.1.0)

**Implemented enhancements:**

- "Warning" Importing from `collections` [\#236](https://github.com/emmo-repo/EMMOntoPy/issues/236)

**Fixed bugs:**

- Loading ontologies that do not import skos fails [\#261](https://github.com/emmo-repo/EMMOntoPy/issues/261)
- Fix documentation build warnings [\#250](https://github.com/emmo-repo/EMMOntoPy/issues/250)
- Fix images in documentation [\#233](https://github.com/emmo-repo/EMMOntoPy/issues/233)
- Circular reference from Owlready2 [\#210](https://github.com/emmo-repo/EMMOntoPy/issues/210)

**Closed issues:**

- Write up transfer from EMMOpython to EMMOntoPy i README.md [\#267](https://github.com/emmo-repo/EMMOntoPy/issues/267)
- Add test to emmocheck for upcoming EMMO [\#257](https://github.com/emmo-repo/EMMOntoPy/issues/257)
- Add packaging as dependency in requirements [\#255](https://github.com/emmo-repo/EMMOntoPy/issues/255)
- Add CI check for building documentation [\#244](https://github.com/emmo-repo/EMMOntoPy/issues/244)
- Add OpenModel as contributing project [\#237](https://github.com/emmo-repo/EMMOntoPy/issues/237)
- Update public documentation to new framework [\#234](https://github.com/emmo-repo/EMMOntoPy/issues/234)
- Automate documentation releases [\#232](https://github.com/emmo-repo/EMMOntoPy/issues/232)
- Update name of EMMO to Elemental Multiperspective Material Ontology [\#230](https://github.com/emmo-repo/EMMOntoPy/issues/230)
- Tidy up unittests [\#220](https://github.com/emmo-repo/EMMOntoPy/issues/220)
- Remove importability of sub-`factpluspluswrapper` folders [\#213](https://github.com/emmo-repo/EMMOntoPy/issues/213)
- Make function that automatically loads emmo [\#209](https://github.com/emmo-repo/EMMOntoPy/issues/209)
- Require rdflib\>5.0.0? [\#206](https://github.com/emmo-repo/EMMOntoPy/issues/206)
- change package name [\#205](https://github.com/emmo-repo/EMMOntoPy/issues/205)
- test\_catalog fails because seraching for .owl in emmo/master [\#203](https://github.com/emmo-repo/EMMOntoPy/issues/203)
- Consider using `mike` for versioned documentation [\#197](https://github.com/emmo-repo/EMMOntoPy/issues/197)
- Add a test that checks that loading of non-EMMO based ontologies work - e.g. do not require skos:prefLabel [\#196](https://github.com/emmo-repo/EMMOntoPy/issues/196)
- Setup Materials for MkDocs framework [\#195](https://github.com/emmo-repo/EMMOntoPy/issues/195)
- Clean up demo, examples and docs [\#193](https://github.com/emmo-repo/EMMOntoPy/issues/193)
- Formalize review process with checklists [\#190](https://github.com/emmo-repo/EMMOntoPy/issues/190)
- funksjon ontology.add\_class\(label, parent\)  [\#183](https://github.com/emmo-repo/EMMOntoPy/issues/183)

**Merged pull requests:**

- Reset version to 0.1.0 [\#271](https://github.com/emmo-repo/EMMOntoPy/pull/271) ([CasperWA](https://github.com/CasperWA))
- Update README with PyPI and deprecation msgs [\#270](https://github.com/emmo-repo/EMMOntoPy/pull/270) ([CasperWA](https://github.com/CasperWA))
- Added option: EMMObased = False in ontology.load\(\) [\#262](https://github.com/emmo-repo/EMMOntoPy/pull/262) ([francescalb](https://github.com/francescalb))
- Added new test "test\_physical\_quantity\_dimension" [\#258](https://github.com/emmo-repo/EMMOntoPy/pull/258) ([jesper-friis](https://github.com/jesper-friis))
- Add `packaging` to list of requirements [\#256](https://github.com/emmo-repo/EMMOntoPy/pull/256) ([CasperWA](https://github.com/CasperWA))
- Fix MkDocs build warnings and CI job [\#254](https://github.com/emmo-repo/EMMOntoPy/pull/254) ([CasperWA](https://github.com/CasperWA))
- Update dependencies [\#252](https://github.com/emmo-repo/EMMOntoPy/pull/252) ([CasperWA](https://github.com/CasperWA))
- Add OpenModel contributing project [\#247](https://github.com/emmo-repo/EMMOntoPy/pull/247) ([francescalb](https://github.com/francescalb))
- Automate documentation releases [\#242](https://github.com/emmo-repo/EMMOntoPy/pull/242) ([CasperWA](https://github.com/CasperWA))
- Import from `collections.abc` when possible [\#240](https://github.com/emmo-repo/EMMOntoPy/pull/240) ([CasperWA](https://github.com/CasperWA))
- Ensure all produced files from tests are in a temp dir [\#239](https://github.com/emmo-repo/EMMOntoPy/pull/239) ([CasperWA](https://github.com/CasperWA))
- Changed EMMO to be acronym for Elemental Multiperspective Material Ontology [\#238](https://github.com/emmo-repo/EMMOntoPy/pull/238) ([francescalb](https://github.com/francescalb))
- Use width in img HTML [\#235](https://github.com/emmo-repo/EMMOntoPy/pull/235) ([CasperWA](https://github.com/CasperWA))
- Added function to load the emmo \(the ontology\) directly [\#226](https://github.com/emmo-repo/EMMOntoPy/pull/226) ([francescalb](https://github.com/francescalb))
- Created pull request template [\#225](https://github.com/emmo-repo/EMMOntoPy/pull/225) ([francescalb](https://github.com/francescalb))
- Setup new documentation framework [\#222](https://github.com/emmo-repo/EMMOntoPy/pull/222) ([CasperWA](https://github.com/CasperWA))
- Remove `__init__.py` files for FaCT++ wrapper \(again\) [\#221](https://github.com/emmo-repo/EMMOntoPy/pull/221) ([CasperWA](https://github.com/CasperWA))
- Unskip test as \#210 has been resolved [\#218](https://github.com/emmo-repo/EMMOntoPy/pull/218) ([CasperWA](https://github.com/CasperWA))
- Remove sub-fact++ modules importability [\#217](https://github.com/emmo-repo/EMMOntoPy/pull/217) ([CasperWA](https://github.com/CasperWA))
- Update requirements [\#216](https://github.com/emmo-repo/EMMOntoPy/pull/216) ([CasperWA](https://github.com/CasperWA))
- Avoid using Owlready2 v0.34 [\#211](https://github.com/emmo-repo/EMMOntoPy/pull/211) ([CasperWA](https://github.com/CasperWA))
- Update package names [\#208](https://github.com/emmo-repo/EMMOntoPy/pull/208) ([CasperWA](https://github.com/CasperWA))
- Added function new\_entitiy to ontology [\#207](https://github.com/emmo-repo/EMMOntoPy/pull/207) ([francescalb](https://github.com/francescalb))
- ttl standard for emmo [\#204](https://github.com/emmo-repo/EMMOntoPy/pull/204) ([francescalb](https://github.com/francescalb))
- Added choice for specifying namespace in get\_by\_label [\#202](https://github.com/emmo-repo/EMMOntoPy/pull/202) ([francescalb](https://github.com/francescalb))

## [v1.0.1b](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.1b) (2021-07-01)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.1...v1.0.1b)

**Closed issues:**

- Correct updating of catalog in ontology.load [\#188](https://github.com/emmo-repo/EMMOntoPy/issues/188)

**Merged pull requests:**

- Update version to 1.0.1 [\#189](https://github.com/emmo-repo/EMMOntoPy/pull/189) ([francescalb](https://github.com/francescalb))

## [v1.0.1](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.1) (2021-07-01)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0...v1.0.1)

**Fixed bugs:**

- Windows paths are not handled properly [\#147](https://github.com/emmo-repo/EMMOntoPy/issues/147)

**Closed issues:**

- Failing tests when lodaing battinfo [\#185](https://github.com/emmo-repo/EMMOntoPy/issues/185)
- Fix dependatbot to 'wider' [\#182](https://github.com/emmo-repo/EMMOntoPy/issues/182)
- Change to get\_label instead of asstring in ontograph, emmodoc, ontodoc, be careful [\#158](https://github.com/emmo-repo/EMMOntoPy/issues/158)
- licence does not work with metadata [\#157](https://github.com/emmo-repo/EMMOntoPy/issues/157)
- ontograph with several roots fails [\#153](https://github.com/emmo-repo/EMMOntoPy/issues/153)
- fix redudant getlabel, get\_preferred\_label, get\_label [\#152](https://github.com/emmo-repo/EMMOntoPy/issues/152)
- add --no-catalog and default as in emmocheck for ontograph [\#150](https://github.com/emmo-repo/EMMOntoPy/issues/150)
- make tests for checking upgrade of Owlready2 [\#137](https://github.com/emmo-repo/EMMOntoPy/issues/137)
- Add periodic\_table to examples [\#130](https://github.com/emmo-repo/EMMOntoPy/issues/130)
- Add support for simple property-based ontology annotations like dcterms:license [\#129](https://github.com/emmo-repo/EMMOntoPy/issues/129)
- Update documentation of tools re reasoner [\#123](https://github.com/emmo-repo/EMMOntoPy/issues/123)
- Ontograph: Include multiple parents/inheritance [\#86](https://github.com/emmo-repo/EMMOntoPy/issues/86)

**Merged pull requests:**

- Fixed updating of catalog in load [\#187](https://github.com/emmo-repo/EMMOntoPy/pull/187) ([francescalb](https://github.com/francescalb))
- Temporarily commented out loading ontologies with error in redirecting link on emmo.info [\#186](https://github.com/emmo-repo/EMMOntoPy/pull/186) ([francescalb](https://github.com/francescalb))
- Changed dependabot to widen [\#181](https://github.com/emmo-repo/EMMOntoPy/pull/181) ([francescalb](https://github.com/francescalb))
- Changed requirements to greater than [\#179](https://github.com/emmo-repo/EMMOntoPy/pull/179) ([francescalb](https://github.com/francescalb))
- Owread2-0.32 not accepted die to error in owlready2 triplelite [\#178](https://github.com/emmo-repo/EMMOntoPy/pull/178) ([francescalb](https://github.com/francescalb))
- Fixed import of defaultstyle in ontograph-tool [\#177](https://github.com/emmo-repo/EMMOntoPy/pull/177) ([francescalb](https://github.com/francescalb))
- Updated pygments req to at least 2.7.4 because of high seq alert [\#168](https://github.com/emmo-repo/EMMOntoPy/pull/168) ([francescalb](https://github.com/francescalb))
- Owlready requirement \>0.28 [\#167](https://github.com/emmo-repo/EMMOntoPy/pull/167) ([francescalb](https://github.com/francescalb))
- WIP: Ipycytoscape [\#163](https://github.com/emmo-repo/EMMOntoPy/pull/163) ([francescalb](https://github.com/francescalb))
- Made it possible to load other ontologies like foaf [\#162](https://github.com/emmo-repo/EMMOntoPy/pull/162) ([jesper-friis](https://github.com/jesper-friis))
- Added get\_label instead of asstring [\#160](https://github.com/emmo-repo/EMMOntoPy/pull/160) ([francescalb](https://github.com/francescalb))
- Added write\_catalog\(\) [\#159](https://github.com/emmo-repo/EMMOntoPy/pull/159) ([jesper-friis](https://github.com/jesper-friis))
- Periodic table example [\#156](https://github.com/emmo-repo/EMMOntoPy/pull/156) ([francescalb](https://github.com/francescalb))
- Make one get label [\#154](https://github.com/emmo-repo/EMMOntoPy/pull/154) ([francescalb](https://github.com/francescalb))
- Issue150 ontograph cannotload emmo inferred directly [\#151](https://github.com/emmo-repo/EMMOntoPy/pull/151) ([francescalb](https://github.com/francescalb))
- Added Fact++ in tools documentation [\#149](https://github.com/emmo-repo/EMMOntoPy/pull/149) ([francescalb](https://github.com/francescalb))
- Improved issue reporting in emmocheck [\#146](https://github.com/emmo-repo/EMMOntoPy/pull/146) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0) (2021-03-25)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-30...v1.0.0)

**Closed issues:**

- Use rdflib in Ontology.save\(\) to support more file formats [\#143](https://github.com/emmo-repo/EMMOntoPy/issues/143)
- Tool for publishing domain ontologies [\#140](https://github.com/emmo-repo/EMMOntoPy/issues/140)

**Merged pull requests:**

- Save to turtle and ontology annotations \(via the metadata attribute\) [\#144](https://github.com/emmo-repo/EMMOntoPy/pull/144) ([jesper-friis](https://github.com/jesper-friis))
- Corrected configuration of exceptions for test\_class\_label test. [\#142](https://github.com/emmo-repo/EMMOntoPy/pull/142) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-30](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-30) (2021-03-18)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-29...v1.0.0-alpha-30)

**Merged pull requests:**

- Load ontology [\#141](https://github.com/emmo-repo/EMMOntoPy/pull/141) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-29](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-29) (2021-03-16)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-28...v1.0.0-alpha-29)

**Implemented enhancements:**

- Add Wu&Palmer measure [\#134](https://github.com/emmo-repo/EMMOntoPy/issues/134)

**Closed issues:**

- Convert-imported update in utils [\#138](https://github.com/emmo-repo/EMMOntoPy/issues/138)

**Merged pull requests:**

- Fixed reading xml as 'rdfxml' [\#139](https://github.com/emmo-repo/EMMOntoPy/pull/139) ([francescalb](https://github.com/francescalb))
- Added wu\_palmer\_measure for semantic similarity [\#135](https://github.com/emmo-repo/EMMOntoPy/pull/135) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-28](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-28) (2021-03-09)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-27...v1.0.0-alpha-28)

**Closed issues:**

- Also use the catalog file to map web URLs, not only local files. [\#109](https://github.com/emmo-repo/EMMOntoPy/issues/109)
- Check Error with Owlready2-0.26 [\#81](https://github.com/emmo-repo/EMMOntoPy/issues/81)

**Merged pull requests:**

- Version updated for rel of v0.28 [\#133](https://github.com/emmo-repo/EMMOntoPy/pull/133) ([francescalb](https://github.com/francescalb))
- Load ontology [\#131](https://github.com/emmo-repo/EMMOntoPy/pull/131) ([jesper-friis](https://github.com/jesper-friis))
- Optimised label lookup in ontology and dir listing. It is now much faster [\#127](https://github.com/emmo-repo/EMMOntoPy/pull/127) ([jesper-friis](https://github.com/jesper-friis))
- Use catalog by default [\#126](https://github.com/emmo-repo/EMMOntoPy/pull/126) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-27](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-27) (2021-02-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-26...v1.0.0-alpha-27)

**Merged pull requests:**

- Ontodoc [\#125](https://github.com/emmo-repo/EMMOntoPy/pull/125) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-26](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-26) (2021-02-26)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-25...v1.0.0-alpha-26)

**Closed issues:**

- Make fact++ reasoner available and default in tools [\#122](https://github.com/emmo-repo/EMMOntoPy/issues/122)
- Use PyPI token in publish workflow [\#118](https://github.com/emmo-repo/EMMOntoPy/issues/118)
- Update publish workflow [\#115](https://github.com/emmo-repo/EMMOntoPy/issues/115)
- do something [\#108](https://github.com/emmo-repo/EMMOntoPy/issues/108)

**Merged pull requests:**

- Added functionality to document domain ontologies [\#124](https://github.com/emmo-repo/EMMOntoPy/pull/124) ([jesper-friis](https://github.com/jesper-friis))
- Made ontoconvert and ontograph tools executable in linux [\#120](https://github.com/emmo-repo/EMMOntoPy/pull/120) ([jesper-friis](https://github.com/jesper-friis))
- Update CI  [\#119](https://github.com/emmo-repo/EMMOntoPy/pull/119) ([CasperWA](https://github.com/CasperWA))
- Update publish workflow + add dependabot [\#116](https://github.com/emmo-repo/EMMOntoPy/pull/116) ([CasperWA](https://github.com/CasperWA))

## [v1.0.0-alpha-25](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-25) (2021-01-17)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-24...v1.0.0-alpha-25)

**Closed issues:**

- Update Dockerfile to install correct pandoc [\#99](https://github.com/emmo-repo/EMMOntoPy/issues/99)
- Correct turtle serialisation [\#97](https://github.com/emmo-repo/EMMOntoPy/issues/97)

**Merged pull requests:**

- Update emmocheck exceptions [\#113](https://github.com/emmo-repo/EMMOntoPy/pull/113) ([jesper-friis](https://github.com/jesper-friis))
- Fix recursion in graph [\#112](https://github.com/emmo-repo/EMMOntoPy/pull/112) ([jesper-friis](https://github.com/jesper-friis))
- Avoid unnessesary/infinite recursion in get\_imported\_ontologies\(\) [\#111](https://github.com/emmo-repo/EMMOntoPy/pull/111) ([jesper-friis](https://github.com/jesper-friis))
- Break recursion error in get\_by\_label\(\) [\#110](https://github.com/emmo-repo/EMMOntoPy/pull/110) ([jesper-friis](https://github.com/jesper-friis))
- Updated the Ontology.sync\_attributes\(\) method. [\#107](https://github.com/emmo-repo/EMMOntoPy/pull/107) ([jesper-friis](https://github.com/jesper-friis))
- Updated pandoc req in Dockerfile [\#106](https://github.com/emmo-repo/EMMOntoPy/pull/106) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-24](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-24) (2021-01-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-23...v1.0.0-alpha-24)

**Merged pull requests:**

- Bumped version number up to 1.0.0-alpha-24  [\#105](https://github.com/emmo-repo/EMMOntoPy/pull/105) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-23](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-23) (2021-01-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-22...v1.0.0-alpha-23)

**Closed issues:**

- Fix loading imported ttl from web such that emmocheck works for crystallography.ttl [\#98](https://github.com/emmo-repo/EMMOntoPy/issues/98)
- Add reasoning with FaCT++ [\#95](https://github.com/emmo-repo/EMMOntoPy/issues/95)
- Correctly load ontologies like crystallography that imports both local and online sub-ontologies [\#91](https://github.com/emmo-repo/EMMOntoPy/issues/91)
- Fix flake8 errors [\#88](https://github.com/emmo-repo/EMMOntoPy/issues/88)
- Remove the .ttl namespace when loading domain-crystallography in EMMO-python [\#83](https://github.com/emmo-repo/EMMOntoPy/issues/83)
- Add option of documenting imported ontologies in ontodoc and ontograph [\#82](https://github.com/emmo-repo/EMMOntoPy/issues/82)
- Emmocheck fails if Physicaluantities and MeaurementsUnits are not imported from emmo. Make sure that it does not fail if whole of EMMO is not imported. [\#80](https://github.com/emmo-repo/EMMOntoPy/issues/80)
- Ontograph: Make default root [\#79](https://github.com/emmo-repo/EMMOntoPy/issues/79)
- Ontodoc: PDF is not generated, produces error. [\#76](https://github.com/emmo-repo/EMMOntoPy/issues/76)
- AttributeError from ontodoc [\#70](https://github.com/emmo-repo/EMMOntoPy/issues/70)
- Import emmo .ttl from emmo-repo.github.io [\#69](https://github.com/emmo-repo/EMMOntoPy/issues/69)
- Unable to use the vertical interoperability demo .py files [\#66](https://github.com/emmo-repo/EMMOntoPy/issues/66)

**Merged pull requests:**

- Release 1.0.0-alpha-23 [\#104](https://github.com/emmo-repo/EMMOntoPy/pull/104) ([jesper-friis](https://github.com/jesper-friis))
- Allow to load turtle ontologies without catalog file. [\#102](https://github.com/emmo-repo/EMMOntoPy/pull/102) ([jesper-friis](https://github.com/jesper-friis))
- Updated README file [\#100](https://github.com/emmo-repo/EMMOntoPy/pull/100) ([jesper-friis](https://github.com/jesper-friis))
- Changed the sync\_reasoner\(\) method to use FaCT++ as the default reasoner [\#94](https://github.com/emmo-repo/EMMOntoPy/pull/94) ([jesper-friis](https://github.com/jesper-friis))
- Add reasoning [\#93](https://github.com/emmo-repo/EMMOntoPy/pull/93) ([jesper-friis](https://github.com/jesper-friis))
- Improve load ontologies [\#92](https://github.com/emmo-repo/EMMOntoPy/pull/92) ([jesper-friis](https://github.com/jesper-friis))
- Remove the '.ttl' in namespace names by monkey patching owlready2.Namespace [\#90](https://github.com/emmo-repo/EMMOntoPy/pull/90) ([jesper-friis](https://github.com/jesper-friis))
- Fix flake8 warnings [\#89](https://github.com/emmo-repo/EMMOntoPy/pull/89) ([jesper-friis](https://github.com/jesper-friis))
- Ontodoc pdf [\#87](https://github.com/emmo-repo/EMMOntoPy/pull/87) ([jesper-friis](https://github.com/jesper-friis))
- Automatically find roots in ontograph  [\#85](https://github.com/emmo-repo/EMMOntoPy/pull/85) ([francescalb](https://github.com/francescalb))
- Automatic import of ttl from GitHub emmo-repo.io [\#84](https://github.com/emmo-repo/EMMOntoPy/pull/84) ([francescalb](https://github.com/francescalb))
- Fixes needed for access ontologies [\#77](https://github.com/emmo-repo/EMMOntoPy/pull/77) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-22](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-22) (2020-12-21)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-21b...v1.0.0-alpha-22)

**Merged pull requests:**

- Loading ttl both locally and importing from iri [\#75](https://github.com/emmo-repo/EMMOntoPy/pull/75) ([francescalb](https://github.com/francescalb))
- Added sync\_python\_names\(\) and corrected handling of individuals in sync\_attributes\(\) [\#73](https://github.com/emmo-repo/EMMOntoPy/pull/73) ([jesper-friis](https://github.com/jesper-friis))
- Add preflabel to individuals declared in python [\#72](https://github.com/emmo-repo/EMMOntoPy/pull/72) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-21b](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-21b) (2020-12-13)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-21...v1.0.0-alpha-21b)

**Merged pull requests:**

- Fix bug introduced in ontoconvert [\#71](https://github.com/emmo-repo/EMMOntoPy/pull/71) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-21](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-21) (2020-12-11)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-20b...v1.0.0-alpha-21)

**Merged pull requests:**

- Use rdflib to load non-supported formats. [\#68](https://github.com/emmo-repo/EMMOntoPy/pull/68) ([jesper-friis](https://github.com/jesper-friis))
- Added a quick fix for vertical demo. [\#67](https://github.com/emmo-repo/EMMOntoPy/pull/67) ([jesper-friis](https://github.com/jesper-friis))
- Updated emmocheck to new 1.0.0-beta. Old version should still work. [\#65](https://github.com/emmo-repo/EMMOntoPy/pull/65) ([jesper-friis](https://github.com/jesper-friis))
- Added ontoconvert tool [\#64](https://github.com/emmo-repo/EMMOntoPy/pull/64) ([jesper-friis](https://github.com/jesper-friis))
- Improved error messages for classes that doesn't define prefLabel [\#63](https://github.com/emmo-repo/EMMOntoPy/pull/63) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-20b](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-20b) (2020-11-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-20...v1.0.0-alpha-20b)

**Merged pull requests:**

- Version1.0.0 alpha20 [\#62](https://github.com/emmo-repo/EMMOntoPy/pull/62) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-20](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-20) (2020-11-04)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-19...v1.0.0-alpha-20)

**Merged pull requests:**

- Improve support for imported ontologies [\#61](https://github.com/emmo-repo/EMMOntoPy/pull/61) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-19](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-19) (2020-11-02)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-18...v1.0.0-alpha-19)

**Merged pull requests:**

- Added --ignore-namespace to emmocheck  [\#60](https://github.com/emmo-repo/EMMOntoPy/pull/60) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-18](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-18) (2020-10-29)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-17...v1.0.0-alpha-18)

**Merged pull requests:**

- Bumped up version number to 1.0.0-alpha-18 [\#59](https://github.com/emmo-repo/EMMOntoPy/pull/59) ([jesper-friis](https://github.com/jesper-friis))
- Added option url\_from\_catalog to ontology.load\(\) [\#58](https://github.com/emmo-repo/EMMOntoPy/pull/58) ([jesper-friis](https://github.com/jesper-friis))
- Added get\_preferred\_label\(\) method to classes, properties and individuals [\#57](https://github.com/emmo-repo/EMMOntoPy/pull/57) ([jesper-friis](https://github.com/jesper-friis))
- Correct default IRI to inferred ontology [\#56](https://github.com/emmo-repo/EMMOntoPy/pull/56) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-17](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-17) (2020-10-21)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-16...v1.0.0-alpha-17)

**Merged pull requests:**

- Added materials.EngineeredMaterial to namespace exception in emmocheck [\#55](https://github.com/emmo-repo/EMMOntoPy/pull/55) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-16](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-16) (2020-10-20)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-15...v1.0.0-alpha-16)

**Closed issues:**

- Include all annotations in .get\_annotations\(\) [\#50](https://github.com/emmo-repo/EMMOntoPy/issues/50)

**Merged pull requests:**

- Update to v1.0.0-alpha-16 for new release [\#54](https://github.com/emmo-repo/EMMOntoPy/pull/54) ([francescalb](https://github.com/francescalb))
- Update dimensionality checks [\#53](https://github.com/emmo-repo/EMMOntoPy/pull/53) ([jesper-friis](https://github.com/jesper-friis))
- Updated to say that pypi realese is automatic in docs [\#52](https://github.com/emmo-repo/EMMOntoPy/pull/52) ([francescalb](https://github.com/francescalb))

## [v1.0.0-alpha-15](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-15) (2020-09-25)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-13...v1.0.0-alpha-15)

**Merged pull requests:**

- Added all labels in get\_class\_annotations in emmo/patch.py including [\#51](https://github.com/emmo-repo/EMMOntoPy/pull/51) ([francescalb](https://github.com/francescalb))
- Support use of skos:prefLabel instead of rdfs:label [\#49](https://github.com/emmo-repo/EMMOntoPy/pull/49) ([jesper-friis](https://github.com/jesper-friis))
- v1.0.0-alpha-14  [\#48](https://github.com/emmo-repo/EMMOntoPy/pull/48) ([jesper-friis](https://github.com/jesper-friis))
- Fix emmocheck to not fail upon use of dcterms and skos [\#47](https://github.com/emmo-repo/EMMOntoPy/pull/47) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-13](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-13) (2020-09-19)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-11...v1.0.0-alpha-13)

**Closed issues:**

- Not immediately installable with pip [\#45](https://github.com/emmo-repo/EMMOntoPy/issues/45)

**Merged pull requests:**

- Fix setup [\#46](https://github.com/emmo-repo/EMMOntoPy/pull/46) ([jesper-friis](https://github.com/jesper-friis))
- Make emmo package pip installable in fresh env [\#44](https://github.com/emmo-repo/EMMOntoPy/pull/44) ([CasperWA](https://github.com/CasperWA))
- Update emmodoc to latest version of emmo-alpha2 [\#43](https://github.com/emmo-repo/EMMOntoPy/pull/43) ([jesper-friis](https://github.com/jesper-friis))
- Ensure that emmocheck exit with non-zero return value if a test is faing [\#42](https://github.com/emmo-repo/EMMOntoPy/pull/42) ([jesper-friis](https://github.com/jesper-friis))
- Installed missing dependencies in pythonpublish deployment workflow [\#41](https://github.com/emmo-repo/EMMOntoPy/pull/41) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-11](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-11) (2020-08-12)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-10...v1.0.0-alpha-11)

**Merged pull requests:**

- Add skip option to emmocheck [\#40](https://github.com/emmo-repo/EMMOntoPy/pull/40) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-10](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-10) (2020-04-27)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-9...v1.0.0-alpha-10)

**Merged pull requests:**

- Added exceptions to emmocheck "test\_number\_of\_labels" [\#39](https://github.com/emmo-repo/EMMOntoPy/pull/39) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-9](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-9) (2020-04-13)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-8...v1.0.0-alpha-9)

**Closed issues:**

- Enhance ontology.sync\_attributes\(\) to also update class names [\#10](https://github.com/emmo-repo/EMMOntoPy/issues/10)
- Add support for the FaCT++ reasoner [\#9](https://github.com/emmo-repo/EMMOntoPy/issues/9)

**Merged pull requests:**

- Set new release version 1.0.0-alpha-9 [\#38](https://github.com/emmo-repo/EMMOntoPy/pull/38) ([francescalb](https://github.com/francescalb))
- Added get\_version\(\) and set\_version\(\) methods to emmo.Ontology. [\#37](https://github.com/emmo-repo/EMMOntoPy/pull/37) ([jesper-friis](https://github.com/jesper-friis))
- Updated example in README file to current version of EMMO. [\#36](https://github.com/emmo-repo/EMMOntoPy/pull/36) ([jesper-friis](https://github.com/jesper-friis))
- Update tools [\#35](https://github.com/emmo-repo/EMMOntoPy/pull/35) ([jesper-friis](https://github.com/jesper-friis))
- Updated simplifed demo\_vertical in compliance with EMMO-1.0.0alpha2 as of 202… [\#34](https://github.com/emmo-repo/EMMOntoPy/pull/34) ([francescalb](https://github.com/francescalb))
- Fixed PyPI badge in README [\#33](https://github.com/emmo-repo/EMMOntoPy/pull/33) ([jesper-friis](https://github.com/jesper-friis))
- Update emmocheck [\#32](https://github.com/emmo-repo/EMMOntoPy/pull/32) ([jesper-friis](https://github.com/jesper-friis))
- Sync attributes [\#31](https://github.com/emmo-repo/EMMOntoPy/pull/31) ([jesper-friis](https://github.com/jesper-friis))
- Cleanup ci workflow [\#28](https://github.com/emmo-repo/EMMOntoPy/pull/28) ([jesper-friis](https://github.com/jesper-friis))
- Added ontoversion tool [\#27](https://github.com/emmo-repo/EMMOntoPy/pull/27) ([jesper-friis](https://github.com/jesper-friis))
- Update emmodoc [\#25](https://github.com/emmo-repo/EMMOntoPy/pull/25) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-8](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-8) (2020-03-22)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-5...v1.0.0-alpha-8)

**Merged pull requests:**

- 1.0.0 alpha 8 [\#30](https://github.com/emmo-repo/EMMOntoPy/pull/30) ([jesper-friis](https://github.com/jesper-friis))
- Updated requirements such that "pip install EMMO" works [\#24](https://github.com/emmo-repo/EMMOntoPy/pull/24) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-5](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-5) (2020-03-18)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-3...v1.0.0-alpha-5)

**Implemented enhancements:**

- Make EMMO-python available on pypi \(installable with pip\) [\#7](https://github.com/emmo-repo/EMMOntoPy/issues/7)

**Merged pull requests:**

- Bumbed up version to 1.0.0-alpha-5 [\#23](https://github.com/emmo-repo/EMMOntoPy/pull/23) ([jesper-friis](https://github.com/jesper-friis))
- Emmocheck [\#22](https://github.com/emmo-repo/EMMOntoPy/pull/22) ([jesper-friis](https://github.com/jesper-friis))
- Reworked the generation of graphs - using the graphviz Python package [\#21](https://github.com/emmo-repo/EMMOntoPy/pull/21) ([jesper-friis](https://github.com/jesper-friis))
- 1.0.0 [\#19](https://github.com/emmo-repo/EMMOntoPy/pull/19) ([jesper-friis](https://github.com/jesper-friis))

## [v1.0.0-alpha-3](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-3) (2020-02-16)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-2...v1.0.0-alpha-3)

## [v1.0.0-alpha-2](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-2) (2020-01-11)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha-1...v1.0.0-alpha-2)

## [v1.0.0-alpha-1](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha-1) (2020-01-11)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v1.0.0-alpha...v1.0.0-alpha-1)

**Closed issues:**

- Missing https://emmc.info/emmo-inferred [\#16](https://github.com/emmo-repo/EMMOntoPy/issues/16)
- setup.py [\#15](https://github.com/emmo-repo/EMMOntoPy/issues/15)
- Fix emmodoc [\#6](https://github.com/emmo-repo/EMMOntoPy/issues/6)

## [v1.0.0-alpha](https://github.com/emmo-repo/EMMOntoPy/tree/v1.0.0-alpha) (2020-01-08)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/v0.9.9...v1.0.0-alpha)

**Closed issues:**

- Update the user case ontology [\#3](https://github.com/emmo-repo/EMMOntoPy/issues/3)

**Merged pull requests:**

- Fixed a typo in the title [\#14](https://github.com/emmo-repo/EMMOntoPy/pull/14) ([blokhin](https://github.com/blokhin))
- Fixed \#5 - homogenised call to reasoner [\#13](https://github.com/emmo-repo/EMMOntoPy/pull/13) ([francescalb](https://github.com/francescalb))

## [v0.9.9](https://github.com/emmo-repo/EMMOntoPy/tree/v0.9.9) (2019-07-14)

[Full Changelog](https://github.com/emmo-repo/EMMOntoPy/compare/34866fa72fea0b178cabbe21dfee06f735bbf373...v0.9.9)

**Closed issues:**

- Homogenise call to reasoner in emmo.Ontology.sync\_reasoner\(\) [\#5](https://github.com/emmo-repo/EMMOntoPy/issues/5)

**Merged pull requests:**

- \#3 update usercase ontology [\#12](https://github.com/emmo-repo/EMMOntoPy/pull/12) ([jesper-friis](https://github.com/jesper-friis))
- Fixed 3 [\#8](https://github.com/emmo-repo/EMMOntoPy/pull/8) ([jesper-friis](https://github.com/jesper-friis))
- Dockerdevel [\#2](https://github.com/emmo-repo/EMMOntoPy/pull/2) ([francescalb](https://github.com/francescalb))
- Fix by lukas [\#1](https://github.com/emmo-repo/EMMOntoPy/pull/1) ([jesper-friis](https://github.com/jesper-friis))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
