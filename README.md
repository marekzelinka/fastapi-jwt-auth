# Secure User Authentication in FastAPI using JWT Tokens and Neon Postgres

Implemented a secure user authentication system in FastAPI using JWT tokens (with PyJWT) and Neon Postgres.

## The Process of Using JWTs

The overall process of using JWTs for authentication and authorization typically involves the following steps:

1.  **User Authentication**:

    - The process begins when a user logs in with their credentials (e.g., username and password).
    - The server verifies these credentials against the stored user information.

2.  **JWT Creation**:

    - Upon successful authentication, the server creates a JWT.
    - It generates the header and payload, encoding the necessary information.
    - Using a secret key (kept secure on the server), it creates the signature.
    - The three parts (header, payload, signature) are combined to form the complete JWT.

3.  **Sending the Token**:

    - The server sends this token back to the client in the response.
    - The client stores this token, often in local storage or a secure cookie.

4.  **Subsequent Requests**:

    - For any subsequent requests to protected routes or resources, the client includes this token in the Authorization header.
    - The format is: `Authorization: Bearer <token>`

5.  **Server-side Token Validation**:

    - When the server receives a request with a JWT, it first splits the token into its three parts.
    - It base64 decodes the header and payload.
    - The server then recreates the signature using the header, payload, and its secret key.
    - If this newly created signature matches the signature in the token, the server knows the token is valid and hasn't been tampered with.
    
6.  **Accessing Protected Resources**:

    - If the token is valid, the server can use the information in the payload without needing to query the database.
    - This allows the server to authenticate the user and know their permissions for each request without needing to store session data.
    
7.  **Token Expiration**:

    - JWTs typically have an expiration time specified in the payload.
    - The server checks this expiration time with each request.
    - If the token has expired, the server will reject the request, requiring the client to authenticate again.

## API Endpoints

1. The `/register` endpoint allows new users to create an account. It checks if the username is already taken, hashes the password, and stores the new user in the database.

2. The `/token` endpoint handles user login. It verifies the username and password, and if correct, issues a JWT access token.

3. The `get_current_user` function is a dependency that verifies the JWT token and retrieves the current user. This is used to protect routes that require authentication.

4. The `/users/me` endpoint is an example of a protected route. It returns the current user's information, but only if a valid JWT token is provided.
