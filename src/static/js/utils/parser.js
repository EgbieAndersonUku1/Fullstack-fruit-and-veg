export function splitStringByDelimiter(string, delimiter = "-") {
    if (typeof string !== "string") {
        throw new Error("The object to split must be a string");
    }

    if (typeof delimiter !== "string" || delimiter.length === 0) {
        throw new Error("The delimiter must be a non-empty string");
    }

    if (string === "") {
        return [""]; 
    }

    return string.split(delimiter);
};


export default splitStringByDelimiter;