// import jwt from "jsonwebtoken"



/**
 * This is a temporary JWT class that will be used until the backend is created.
 * The reason is that this application is running on GitHub Pages, and if
 * `jsonwebtoken` is imported, GitHub Pages won't have access to it, which
 * means the part of the application that needs it won't work. Instead, this
 * temporary JWT will be used. Once the backend is created and moved to a site
 * that can handle it, this will be replaced with `createJWTToken` below which uses
 * the imported 'jwt' to handle the token.
 */
class JWT {
    /**
     * Base64 URL encode function
     * @param {string} str - The string to encode.
     * @returns {string} The Base64 URL encoded string.
     */
    _base64UrlEncode(str) {
        return btoa(str)
            .replace(/=/g, '')    
            .replace(/\+/g, '-')  
            .replace(/\//g, '_'); 
    }

    /**
     * HMAC SHA-256 hash function using the Web Crypto API
     * @param {string} message - The message to hash.
     * @param {string} secret - The secret key.
     * @returns {Promise<string>} The Base64 URL encoded hash.
     */
    async _hmacSha256(message, secret) {
        const encoder = new TextEncoder();
        const msgData = encoder.encode(message); 
        const keyData = encoder.encode(secret); 

        const key = await crypto.subtle.importKey(
            'raw', keyData, { name: 'HMAC', hash: { name: 'SHA-256' } }, false, ['sign']
        );

        // Sign the message with the imported key
        const signature = await crypto.subtle.sign('HMAC', key, msgData);

        const byteArray = new Uint8Array(signature);
        return this._byteArrayToBase64Url(byteArray)
    }

    /**
     * Converts a byte array to a Base64 URL encoded string.
     * @param {Uint8Array} byteArray - The byte array to convert.
     * @returns {string} The Base64 URL encoded string.
     */
    _byteArrayToBase64Url(byteArray) {

        if (!(byteArray instanceof Uint8Array)) {
            throw new Error("The byteArray must be an instance of Uint8Array");
        }
        let str = '';
        for (let byte of byteArray) {
            str += String.fromCharCode(byte);
        }
        return this._base64UrlEncode(str);
    }
    /**
     * Create a JWT token with the given payload and secret key.
     *
     * @param {Object} payload - The data to be included in the token.
     * @param {string} secretKey - The secret key to sign the token.
     * @param {string|number|null} [expiresIn=null] - Token expiration time (e.g., '1h', '2d', 3600).
     *                                                If null or omitted, token won't expire.
     * @returns {Promise<string>} The generated JWT token.
     * @throws {Error} If any of the arguments are invalid.
     */
    async createJWTToken(payload, secretKey, expiresIn = null) {
        if (typeof payload !== "object" || payload === null) {
            throw new Error(`The payload must be a non-null object, not a ${typeof payload}.`);
        }

        if (typeof secretKey !== "string") {
            throw new Error(`The secret key must be a string, not a ${typeof secretKey}.`);
        }

        if (expiresIn !== null && typeof expiresIn !== "string" && typeof expiresIn !== "number") {
            throw new Error(`The expiresIn must be a string, number, or null, not a ${typeof expiresIn}.`);
        }

        // Create the header
        const header = {
            alg: "HS256",
            typ: "JWT"
        };

        // Add expiration time to payload if provided
        if (expiresIn !== null) {
            payload.exp = Math.floor(Date.now() / 1000) + (typeof expiresIn === 'number' ? expiresIn : (parseInt(expiresIn) * 60));
        }

        const [encodedHeader, encodedPayload] = this._encode(header, payload);

        const signature = await this._createSignature(encodedHeader, encodedPayload, secretKey);

        // Combine the encoded header, payload, and signature into the final JWT
        return `${encodedHeader}.${encodedPayload}.${signature}`;
    }

    /**
     * Encode header and payload
     * @param {Object} header - The JWT header.
     * @param {Object} payload - The JWT payload.
     * @returns {Array<string>} The encoded header and payload.
     */
    _encode(header, payload) {
        const encodedHeader  = this._base64UrlEncode(JSON.stringify(header));
        const encodedPayload = this._base64UrlEncode(JSON.stringify(payload));
        return [encodedHeader, encodedPayload];
    }

    /**
     * Create a signature for the JWT
     * @param {string} encodedHeader - The Base64 URL encoded header.
     * @param {string} encodedPayload - The Base64 URL encoded payload.
     * @param {string} secretKey - The secret key.
     * @returns {Promise<string>} The Base64 URL encoded signature.
     */
    async _createSignature(encodedHeader, encodedPayload, secretKey) {
        return await this._hmacSha256(`${encodedHeader}.${encodedPayload}`, secretKey);
    }
}


// Function to be used when the backend is built

/**
 * Create a JWT token with the given payload and secret key.
 *
 * @param {Object} payload - The data to be included in the token.
 * @param {string} secretKey - The secret key to sign the token.
 * @param object |null} [expiresIn=null] - Token expiration time (e.g., '1h', '2d', 3600).
 *                                                If null or omitted, token won't expire.
 * @returns {string} The generated JWT token.
 * @throws {Error} If any of the arguments are invalid.
 */
function createJWTToken(payload, secretKey, expiresIn = null) {
    if (typeof payload !== "object" || payload === null) {
        throw new Error(`The payload must be a non-null object, not a ${typeof payload}.`);
    }

    if (typeof secretKey !== "string") {
        throw new Error(`The secret key must be a string, not a ${typeof secretKey}.`);
    }

    if (expiresIn !== null && typeof expiresIn !== "object") {
        throw new Error(`The expiresIn must be an object or null, not a ${typeof expiresIn}.`);
    }

    // commented out to advoid error because of the fact import jwt from "jsonwebtoken" is commented out
    // will uncomment the if-statement below once the backend is built 
    // if (expiresIn === null) {
    //     return jwt.sign(payload, secretKey);
    // }

    // return jwt.sign(payload, secretKey, expiresIn );
}







export {
   JWT
}


