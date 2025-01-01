export default async function fetchData({ url, csrfToken = null, body = null, method = "POST" }) {

    try {

        const allowedMethods = ["POST", "GET"];
        if (!allowedMethods.includes(method)) {
            throw new Error(`Invalid method: ${method}. Allowed methods are ${allowedMethods.join(", ")}`);
        };

        if (method === "POST" && typeof body !== "object" || body === null) {
            throw new Error(`Body must be a non-null object for POST requests, received: ${typeof body}`);
        };
      
        const headers = {
            "Content-Type": "application/json",
        };

        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        };

        const options = {
            method,
            headers,
        };


         if (method === "POST" && body) {
            options.body = JSON.stringify(body);
        };

        const response = await fetch(url, options);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();

    } catch (error) {

        console.error("Fetch error:", error);
        return null;
    }
}



