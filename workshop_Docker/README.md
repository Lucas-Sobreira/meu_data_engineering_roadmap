# Workshop Docker 

## Primeiro passo é clonar o repositório na sua máquina
```bash 
git clone <repo>
cd <folder>
```

## Após feito o clone para a sua máquina, buildar a imagem e rodar o container
```
docker build -t <container_name> .

docker run -d -p 8501:8501 --name <container_name> <image_name>
```