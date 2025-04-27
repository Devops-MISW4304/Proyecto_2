# Proyecto 2 entrega 1 proyecto CI

**Integrantes:**
* Juan Andrés Bernal
* Juan Sebastián Urrea
* Johan Alexis Bautista
* Juan Camilo Ibáñez 

1.  **Levantar Servicios:**
    ```
    docker-compose -f local-dev-docker-compose.yml up --build -d
    ```

2.  **Inicializar Base de Datos (una vez apenas se hayan buildeado los servicios):**
    ```
    docker-compose -f local-dev-docker-compose.yml exec web flask init_db
    ```

Se maneja un token bearer de 1234


1.  **Enviar Request   (POST a Blacklist):**
    ```
    curl -X POST http://localhost:5000/api/v1/blacklists \
         -H "Content-Type: application/json" \
         -H "Authorization: Bearer 1234" \
         -d '{
               "email": "test@example.com",
               "app_uuid": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
               "blocked_reason": "Testeo"
             }'
    ```

2.  **Consultar email   (GET por email a Blacklist):**
    ```
    curl -X GET http://localhost:5000/api/v1/blacklists/test@example.com \
        -H "Authorization: Bearer 1234"
    ```

    **Comando para correr los tests:**
    ```
    python -m unittest tests/test_blacklist_endpoints.py
    ```


