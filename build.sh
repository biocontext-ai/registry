# sudo curl -L "https://github.com/mikefarah/yq/releases/download/v4.28.2/yq_linux_amd64" > /usr/local/bin/yq
# sudo chmod +x /usr/local/bin/yq

curl -L "https://github.com/mikefarah/yq/releases/download/v4.28.2/yq_linux_amd64" -o ./yq
chmod +x ./yq

mkdir build
touch build/.nojekyll
cat servers/**/meta.yaml

./yq ea -o=json '[.]' servers/**/meta.yaml > build/registry.json
cat build/registry.json
