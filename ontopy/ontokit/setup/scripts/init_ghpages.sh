#!/bin/bash

#set -x

help() {
    cat <<EOF
Usage: init_ghpages.sh [OPTIONS]
Initialise GitHub Pages branch.

Options:
  -h, --help                    Print this help and exit.
  -g, --ghpages BRANCH          Name of GitHub Pages branch. Default: gh-pages
  -n, --ontology-name NAME      Name of ontology.
  -p, --ontology-prefix PREFIX  Ontology prefix.
  -n, --ontology-iri IRI        Ontology IRI.
  -r, --remote                  Remote git repository. Default: origin

EOF
}

## Defaults
GHPAGES=gh-pages
ONTOLOGY_NAME=
ONTOLOGY_PREFIX=
ONTOLOGY_IRI=
REMOTE=origin

## Parse options
TEMP=$(getopt -o hg: --long help,ghpages:,ontology: -- "$@")
[ $? != 0 ] && exit 1
eval set -- "$TEMP"
while true; do
    case "$1" in
        -h|--help)             help; exit 0;;
        -g|--ghpages)          GHPAGES=$2; shift 2;;
        -n|--ontology-name)    ONTOLOGY_NAME=$2; shift 2;;
        -p|--ontology-prefix)  ONTOLOGY_PREFIX=$2; shift 2;;
        -i|--ontology-iri)     ONTOLOGY_IRI=$2; shift 2;;
        -r|--remote)           REMOTE=$2; shift 2;;
        --)                    shift; break;;
    esac
done

current_branch="$(git branch --show-current)"
rootdir="$(git rev-parse --show-toplevel)"
reponame="${rootdir##*/}"

# Ensure that all changes are comitted
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    echo "There exist uncomitted changes"
    exit 1
fi

# Set defaults
if [ -z "$ONTOLOGY_NAME" ]; then
    ONTOLOGY_NAME="$reponame"
    ONTOLOGY_NAME="${ONTOLOGY_NAME#domain-}"
    ONTOLOGY_NAME="${ONTOLOGY_NAME#application-}"
fi
if [ ! -f "$rootdir/${ONTOLOGY_NAME}.ttl" ]; then
    echo "Missing ontology file: $rootdir/${ONTOLOGY_NAME}.ttl"
    exit 1
fi

if [ -z "$ONTOLOGY_IRI" ]; then
    ONTOLOGY_IRI="$(sed -n  's/^@prefix :  *<\([^>]*\)>.*/\1/p' $rootdir/${ONTOLOGY_NAME}.ttl)"
    ONTOLOGY_IRI=${ONTOLOGY_IRI%#}
    ONTOLOGY_IRI=${ONTOLOGY_IRI%/}
fi

if [ -z "${ONTOLOGY_IRI}" ]; then
    echo "Empty ONTOLOGY_IRI"
    exit 1
fi

if [ -z "$ONTOLOGY_PREFIX" ]; then
    ONTOLOGY_PREFIX="$(sed -n 's|^@prefix  *\([^:]*\):  *<${ONTOLOGY_IRI}>.*|\1|p' $rootdir/${ONTOLOGY_NAME}.ttl)"
fi

have_deps=$([ -f "${rootdir}/${ONTOLOGY_NAME}-dependencies.ttl" ] && echo true || echo false)


# Show settings
echo "-- Settings:"
echo "   - current_branch=$current_branch"
echo "   - rootdir=$rootdir"
echo "   - reponame=$reponame"
echo "   - have_deps=$have_deps"
echo "   - GHPAGES=$GHPAGES"
echo "   - ONTOLOGY_NAME=$ONTOLOGY_NAME"
echo "   - ONTOLOGY_PREFIX=$ONTOLOGY_PREFIX"
echo "   - ONTOLOGY_IRI=$ONTOLOGY_IRI"
echo "   - REMOTE=$REMOTE"


# Squashed ontology
echo -n "-- Checking for squashed ${ONTOLOGY_NAME}.ttl "
if git show "${GHPAGES}:${ONTOLOGY_NAME}.ttl" > "/tmp/${ONTOLOGY_NAME}.ttl" 2>/dev/null; then
    echo "- exists"
else
    echo "- creating"
    ontoconvert \
        -sawe \
        --namespace="emmo:https://w3id.org/emmo#" \
        --namespace="${ONTOLOGY_PREFIX}:${ONTOLOGY_IRI}#" \
        --base-iri="${ONTOLOGY_IRI}#" \
        --iri="${ONTOLOGY_IRI}" \
        "$rootdir/${ONTOLOGY_NAME}.ttl" \
        "/tmp/${ONTOLOGY_NAME}.ttl"
fi

# Squashed dependencies
echo -n "-- Checking for dependencies "
if $have_deps; then
    if git show "${GHPAGES}:${ONTOLOGY_NAME}-dependencies.ttl" >"/tmp/${ONTOLOGY_NAME}-dependencies.ttl" 2>/dev/null; then
        echo "- exists"
    else
        echo "- creating"
        ontoconvert \
            -saw \
            --namespace="emmo:https://w3id.org/emmo#" \
            --namespace="${ONTOLOGY_PREFIX}:${ONTOLOGY_IRI}#" \
            "${ONTOLOGY_NAME}-dependencies.ttl" \
            "/tmp/${ONTOLOGY_NAME}-dependencies.ttl"
    fi
else
    echo "- missing ${ONTOLOGY_NAME}-dependencies.ttl (skipping)"
fi

# Switch to gh-pages branch (creating it if it doesn't exists)
if [ -z $(git branch --list "$GHPAGES") ]; then
    git switch --orphan "$GHPAGES"
else
    git switch "$GHPAGES"
fi

# Pull from remote
git pull $REMOTE $GHPAGES 2>/dev/null

# Add generated files to gh-pages branch
mv -f "/tmp/${ONTOLOGY_NAME}.ttl" "$rootdir/."
git add "$rootdir/${ONTOLOGY_NAME}.ttl"
if $have_deps; then
     mv -f "/tmp/${ONTOLOGY_NAME}-dependencies.ttl" "$rootdir/."
     git add "$rootdir/${ONTOLOGY_NAME}-dependencies.ttl"
fi

# Commit gh-pages branch (if needed)
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    git commit -m "Added squashed ontology and dependencies"
fi

# Push to remote repository
git push $REMOTE $GHPAGES || exit 1

# Change back to original branch
git checkout "$current_branch"
