%%
%% This file
%% This is Markdown file, except of lines starting with %% will
%% be stripped off.
%%

%HEADER "EMMO Classes"    level=1

*emmo* is a class representing the collection of all the individuals
(signs) that are used in the ontology. Individuals are declared by the
EMMO users when they want to apply the EMMO to represent the world.


%BRANCHHEAD EMMO
The root of all classes used to represent the world.  It has two children;
*collection* and *item*.

*collection* is the class representing the collection of all the
individuals (signs) that represents a collection of non-connected real world
objects.

*item* Is the class that collects all the individuals that are members
of a set (it's the most comprehensive set individual).  It is the
branch of mereotopology.

%% - based on *has_part* mereological relation that can be axiomatically defined
%% - a fusion is the sum of its parts (e.g. a car is made of several
%%   mechanical parts, an molecule is made of nuclei and electrons)
%% - a fusion is of the same entity type as its parts (e.g. a physical
%%   entity is made of physical entities parts)
%% - a fusion can be partitioned in more than one way
%BRANCH EMMO


%BRANCHDOC Physical
%BRANCHDOC Elementary


%BRANCHDOC Holistic
%BRANCHDOC Semiotic
%BRANCHDOC Conventional
%BRANCHDOC Icon
%BRANCHDOC Process


%BRANCHDOC Perceptual
%BRANCHDOC Graphical
%BRANCHDOC Geometrical
%BRANCHDOC Symbol
%BRANCHDOC Metrological
%BRANCHDOC Mathematical
%BRANCHDOC Number
%BRANCHDOC MathematicalOperator
%BRANCHDOC MeasurementUnit
%BRANCHDOC SIBaseUnit
%BRANCHDOC SpecialSIDerivedUnit
%BRANCHDOC PrefixedUnit
%BRANCHDOC MetricPrefix
%BRANCHDOC Quantity
%BRANCHDOC BaseQuantity
%BRANCHDOC DerivedQuantity
%BRANCHDOC PhysicalConstant


%BRANCHDOC Reductionistic
%BRANCHDOC Expression
%BRANCHDOC Formula

%BRANCHDOC Physicalistic
%BRANCHDOC ElementaryParticle
%BRANCHDOC MaterialState
%BRANCHDOC Continuum
%BRANCHDOC Mesoscopic
%BRANCHDOC Atomic
%BRANCHDOC Subatomic
