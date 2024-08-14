/**
 * Merges multiple objects into one.
 * 
 * This function takes any number of objects as arguments and combines them into a single object.
 * If a property exists in multiple objects, the value from the last object with that property will be used.
 * The merge is a shallow copy, and what this means is that nested objects or arrays will not be deeply merged.
 * 
 * It can also accept an array of objects using the spread operator.
 * 
 * @param {...Object} objects - The objects to be merged.
 * @returns {Object} The resulting object after merging all input objects.
 * 
 * @example
 * const obj1 = { a: 1, b: 2 };
 * const obj2 = { b: 3, c: 4 };
 * const obj3 = { d: 5 };
 * 
 * const combinedObj = mergeObjects(obj1, obj2, obj3);
 * console.log(combinedObj); // { a: 1, b: 3, c: 4, d: 5 }
 * 
 * @example
 * const objectList = [
 *   { a: 1, b: 2 },
 *   { b: 3, c: 4 },
 *   { d: 5 }
 * ];
 * 
 * const combinedObj = mergeObjects(...objectList);
 * console.log(combinedObj); // { a: 1, b: 3, c: 4, d: 5 }
 */
function mergeObjects(...objects) {
    const result = {};
  
    for (const obj of objects) {
      for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
          result[key] = obj[key];
        }
      }
    }
  
    return result;
  }
  
  export default mergeObjects;