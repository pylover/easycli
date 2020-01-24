#!/usr/bin/env bash
set -e # Exit with nonzero exit code if anything fails

# Save some useful information
REPO="git@github.com:${TRAVIS_REPO_SLUG}.git"
SHA=`git rev-parse --verify HEAD`
DOC="project-gh-pages"
SSH_PRIVATEKEY=".githubdeploy-rsa"

openssl aes-256-cbc \
	-K $encrypted_110aca95eb88_key \
	-iv $encrypted_110aca95eb88_iv \
	-in .githubdeploy-rsa.enc \
	-out $SSH_PRIVATEKEY \
	-d

chmod 600 $SSH_PRIVATEKEY
eval `ssh-agent -s`
ssh-add $SSH_PRIVATEKEY

# Clone/checkout the gh-pages branch from Github alongside the master branch working copy directory :
rm -rf ../${DOC}
git -C .. clone -b gh-pages ${REPO} ${DOC}
GIT="git -C ../${DOC}"
${GIT} config user.name "pylover"
${GIT} config user.email "vahid.mardani@gmail.com"

# Installing dependencies
pip install -r requirements-doc.txt

cd sphinx
make doctest
make html
cd ..

# Deploy
$GIT rm \*.\*
cp -r sphinx/_build/html/* ../${DOC}
cp -r sphinx/_build/html/.buildinfo ../${DOC}
touch ../${DOC}/.nojekyll 
echo "easycli.dobisel.com" > ../${DOC}/CNAME
$GIT add .

# Commit & push
${GIT} commit -am "Deploy to GitHub Pages: ${SHA}"
${GIT} push origin gh-pages

