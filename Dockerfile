# Usa a imagem oficial e leve do Nginx
FROM nginx:alpine

# Remove o arquivo de configuração padrão do Nginx
RUN rm /etc/nginx/nginx.conf

# Copia o seu novo arquivo de configuração personalizado para dentro do container
COPY nginx.conf /etc/nginx/nginx.conf

# Copia o seu arquivo HTML principal (ajuste o nome se o seu arquivo se chamar diferente de index.html)
COPY index.html /usr/share/nginx/html/index.html

# Expõe a porta 80 para acesso local
EXPOSE 80

# Inicia o Nginx em primeiro plano
CMD ["nginx", "-g", "daemon off;"]