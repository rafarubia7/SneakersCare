# Cadastro Flask + MySQL + Docker Compose

## Subir a aplicação

```bash
docker compose up --build -d
```

Acesse: http://localhost:5000

## Verificar os serviços

```bash
docker compose ps
docker compose logs -f
```

## Verificar a tabela criada automaticamente

```bash
docker compose exec db mysql -ucadastro_user -pcadastro123 cadastro_db -e "SHOW TABLES; DESCRIBE usuarios; SELECT * FROM usuarios;"
```

## Parar sem apagar os dados

```bash
docker compose down
```

## Reinicializar do zero (APAGA o volume e os cadastros)

```bash
docker compose down -v
docker compose up --build -d
```

A tabela `usuarios` é criada automaticamente pelo arquivo `db/init.sql`, montado em `/docker-entrypoint-initdb.d/01-init.sql` no container MySQL. O script de inicialização é executado quando o MySQL inicializa um diretório de dados novo.
